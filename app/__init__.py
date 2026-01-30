from flask import Flask, render_template
from app.webhook.routes import webhook
from app.extensions import init_extensions, collection  # MongoDB setup

def create_app():
    app = Flask(__name__, template_folder="../templates")  # templates folder in repo root

    # Initialize MongoDB extensions
    init_extensions(app)

    # Register webhook blueprint
    app.register_blueprint(webhook)

    # Root route for dashboard
    @app.route("/")
    def dashboard():
        events = list(collection.find().sort("timestamp", -1))
        return render_template("index.html", events=events)

    return app
