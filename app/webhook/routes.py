from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import collection

# Create a Flask Blueprint for the webhook routes.
# This allows us to organize the webhook-related endpoints separately.
webhook = Blueprint("webhook", __name__)

# -----------------------------
# GitHub Webhook Receiver
# -----------------------------
@webhook.route("/webhook/receiver", methods=["POST"])
def github_webhook():
    # Grab the JSON payload sent by GitHub.
    payload = request.json
    # Identify the type of event, like 'push' or 'pull_request'.
    event_type = request.headers.get("X-GitHub-Event")

    # Get the GitHub username of the person who triggered the event.
    # Default to "Unknown" if not found.
    author = payload.get("sender", {}).get("login", "Unknown")
    # Capture the current UTC time in a readable format.
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M:%S %p UTC")

    # Initialize branch variables, will fill them depending on the event type.
    from_branch = "-"
    to_branch = "-"

    # Handle a push event.
    if event_type == "push":
        # Extract the branch name from the ref string.
        to_branch = payload["ref"].split("/")[-1]
        action = "PUSH"
        # Create a simple human-readable message.
        message = f'{author} pushed to "{to_branch}" on {timestamp}'

    # Handle a pull request event.
    elif event_type == "pull_request":
        pr = payload["pull_request"]
        # Identify the source and target branches of the PR.
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]

        # Check if the PR was merged.
        if pr["merged"]:
            action = "MERGE"
            message = (
                f'{author} merged branch "{from_branch}" '
                f'to "{to_branch}" on {timestamp}'
            )
        else:
            action = "PULL_REQUEST"
            message = (
                f'{author} submitted a pull request from '
                f'"{from_branch}" to "{to_branch}" on {timestamp}'
            )

    # If the event is not push or pull_request, just ignore it.
    else:
        return jsonify({"status": "ignored"}), 200

    # Store the event details in the database.
    collection.insert_one({
        "action": action,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp,
        "message": message
    })

    # Respond back to GitHub confirming that the event was stored.
    return jsonify({"status": "stored"}), 200


# -----------------------------
# Events API for Dashboard
# -----------------------------
@webhook.route("/events", methods=["GET"])
def get_events():
    # Fetch the latest 20 events from the database, sorted by timestamp descending.
    # Exclude the MongoDB default '_id' field for cleaner output.
    events = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(20)
    )
    # Return the events as a JSON response.
    return jsonify(events)
