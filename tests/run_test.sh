#!/usr/bin/env bash
set -xe
echo "Stopping nginx-demo..."
docker stop nginx-demo || true
echo "Wait 90s for Prometheus alert + Alertmanager webhook + automation to act"
sleep 90
docker ps --filter "name=nginx-demo" -a
echo "Check Prometheus UI: http://localhost:9090 (on VM/forwarded port)"
echo "Check Grafana: http://localhost:3000 (if created data sources manually)"
