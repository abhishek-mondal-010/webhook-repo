from flask import Blueprint, request, jsonify
from app.extensions import collection
from datetime import datetime

# Webhook endpoints for GitHub
webhook = Blueprint("webhook", __name__, url_prefix="/webhook")

@webhook.route("/receiver", methods=["POST"])
def receiver():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json or {}

    # Extract basic info depending on event type
    doc = {
        "request_id": payload.get("id") or payload.get("pull_request", {}).get("id"),
        "author": payload.get("sender", {}).get("login"),
        "action": event_type.upper() if event_type else "UNKNOWN",
        "from_branch": payload.get("pull_request", {}).get("head", {}).get("ref") if event_type=="pull_request" else None,
        "to_branch": payload.get("pull_request", {}).get("base", {}).get("ref") if event_type=="pull_request" else payload.get("ref"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Save to MongoDB
    collection.insert_one(doc)
    print(f"Event saved: {doc}")

    return jsonify({"status": "received"}), 200
