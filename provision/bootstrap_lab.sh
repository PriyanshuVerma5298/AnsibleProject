#!/usr/bin/env bash
set -xe

# run as root in vagrant provisioner
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release python3 python3-pip git

# Install Docker using official convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker vagrant

# Install docker-compose (python package, simple)
pip3 install docker-compose

# Ensure docker running
systemctl enable docker
systemctl start docker

# Move to synced folder and start compose (will be created by user)
cd /vagrant

# Give a moment for Docker to be ready
sleep 3

# pull and start (if files already present)
docker-compose pull || true
docker-compose up -d || true

# Install ansible on the VM (optional for manual runs)
pip3 install ansible

echo "Provision finished."
