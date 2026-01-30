# app/__init__.py
from flask import Flask, render_template, jsonify
from app.webhook.routes import webhook
from app.extensions import init_extensions, collection
from bson import ObjectId
import datetime

def create_app():
    # Create a Flask app instance and set the folder where templates are stored
    app = Flask(__name__, template_folder="../templates")

    # Initialize any extensions like database connections, etc.
    init_extensions(app)
    # Register the webhook blueprint so its routes are accessible
    app.register_blueprint(webhook)

    # -----------------------------
    # Dashboard Route
    # -----------------------------
    @app.route("/")
    def dashboard():
        # Fetch the latest 50 events from the database, newest first
        events = list(collection.find().sort("timestamp", -1).limit(50))

        # Convert MongoDB ObjectId to string and format timestamps
        for e in events:
            e["_id"] = str(e["_id"])
            if "timestamp" in e and isinstance(e["timestamp"], datetime.datetime):
                e["timestamp"] = e["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        # Render the 'index.html' template and pass the events to it
        return render_template("index.html", events=events)

    # -----------------------------
    # API Route to get events as JSON
    # -----------------------------
    @app.route("/events")
    def get_events():
        # Fetch the latest 50 events from the database
        events = list(collection.find().sort("timestamp", -1).limit(50))

        # Convert ObjectId and format timestamps for JSON-friendly output
        for e in events:
            e["_id"] = str(e["_id"])
            if "timestamp" in e and isinstance(e["timestamp"], datetime.datetime):
                e["timestamp"] = e["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        # Return the events in JSON format
        return jsonify({"events": events})

    # -----------------------------
    # Favicon Route
    # -----------------------------
    @app.route("/favicon.ico")
    def favicon():
        # Serve the favicon from the static folder
        return app.send_static_file("favicon.ico")

    # Return the fully configured Flask app
    return app
