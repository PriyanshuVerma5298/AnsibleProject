#!/usr/bin/env bash
set -e

# === CONFIG ===
RG="rg-aitsm"
LOC="centralindia"
VNET="vnet-aitsm"
SUBNET="subnet-aitsm"
ADMIN="azureuser"
SSH_PUB_KEY="$HOME/.ssh/id_rsa.pub"

MONITOR_VM="monitor-vm"
CONTROL_VM="control-vm"
TEST_VM="test-vm"
IMAGE="UbuntuLTS"
SIZE="Standard_B2s"

# === SCRIPT ===
echo "[1/6] Creating resource group..."
az group create -n $RG -l $LOC

echo "[2/6] Creating VNet..."
az network vnet create -g $RG -n $VNET --address-prefix 10.0.0.0/16 \
  --subnet-name $SUBNET --subnet-prefix 10.0.0.0/24

echo "[3/6] Creating monitor-vm..."
az vm create -g $RG -n $MONITOR_VM --image $IMAGE --size $SIZE \
  --admin-username $ADMIN --ssh-key-value "$SSH_PUB_KEY" \
  --vnet-name $VNET --subnet $SUBNET \
  --custom-data ./azure/cloud-init-monitor.yaml

az vm open-port -g $RG -n $MONITOR_VM --port 22
az vm open-port -g $RG -n $MONITOR_VM --port 3000 # Grafana
az vm open-port -g $RG -n $MONITOR_VM --port 9090 # Prometheus
az vm open-port -g $RG -n $MONITOR_VM --port 9093 # Alertmanager

echo "[4/6] Creating control-vm..."
az vm create -g $RG -n $CONTROL_VM --image $IMAGE --size $SIZE \
  --admin-username $ADMIN --ssh-key-value "$SSH_PUB_KEY" \
  --vnet-name $VNET --subnet $SUBNET \
  --custom-data ./azure/cloud-init-control.yaml

az vm open-port -g $RG -n $CONTROL_VM --port 22
az vm open-port -g $RG -n $CONTROL_VM --port 5000 # webhook receiver

echo "[5/6] Creating test-vm..."
az vm create -g $RG -n $TEST_VM --image $IMAGE --size $SIZE \
  --admin-username $ADMIN --ssh-key-value "$SSH_PUB_KEY" \
  --vnet-name $VNET --subnet $SUBNET \
  --custom-data ./azure/cloud-init-test.yaml

az vm open-port -g $RG -n $TEST_VM --port 22
az vm open-port -g $RG -n $TEST_VM --port 9100 # node-exporter

echo "[6/6] Done!"
echo "Use 'az vm list-ip-addresses -g $RG -o table' to see public IPs."
