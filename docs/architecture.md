# Architecture (diagram text)
[Prometheus + Alertmanager + Grafana]  <--scrapes--  [test-node: node-exporter, demo-app]
         |
         v
  Alertmanager -> Webhook -> Control VM (webhook_receiver)
       control VM runs ansible-playbook -> remediation -> call Jira API

