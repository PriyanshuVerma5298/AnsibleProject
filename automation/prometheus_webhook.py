#!/usr/bin/env python3
import logging
from flask import Flask, request, jsonify
import json, os
import docker
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Add /jira folder to Python path
sys.path.append("/jira")
from jira_create_issue import create_issue

app = Flask(__name__)
client = docker.from_env()

def restart_nginx_container():
    try:
        container = client.containers.get("nginx-demo")
        if container.status != "running":
            container.restart()
            logging.info("🔄 Restarted nginx-demo container")
            return True, "restarted"
        else:
            logging.info("ℹ️ nginx-demo already running")
            return False, "already running"
    except docker.errors.NotFound:
        logging.error("❌ nginx-demo container not found")
        return False, "container not found"
    except Exception as e:
        logging.error("❌ Error restarting nginx-demo: %s", e)
        return False, str(e)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info("📩 Received alert payload: %s", json.dumps(data))
    alerts = data.get("alerts", [])
    created = []
    for alert in alerts:
        summary = alert.get("annotations", {}).get("summary", "alert")
        description = alert.get("annotations", {}).get("description", "")
        ok, msg = restart_nginx_container()
        # create JIRA ticket
        try:
            res = create_issue(
                summary=f"[Auto] {summary}",
                description=f"{description}\nRemediation: {msg}"
            )
            created.append(res.get("key"))
            logging.info("✅ Created Jira issue: %s", res.get("key"))
        except Exception as e:
            logging.error("❌ JIRA create failed: %s", e)
    return jsonify({"ok": True, "created": created})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

