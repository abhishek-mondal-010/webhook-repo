# Dev Assessment - Webhook Receiver

Dev Assessment - Webhook Receiver & Dashboard

This repository contains a Flask-based webhook receiver integrated with MongoDB. It listens for GitHub events (push, pull request, and merge) and shows them in a live dashboard that updates every 15 seconds.

Features

Receives GitHub webhook events:

Push: {author} pushed to {to_branch} on {timestamp}

Pull Request: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}

Merge: {author} merged branch {from_branch} to {to_branch} on {timestamp}

Stores events in MongoDB

Displays events on a live dashboard that updates every 15 seconds

Simple, responsive HTML dashboard.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

Configure MongoDB

In app/extensions.py, configure MongoDB and the collection variable

Example:

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

```bash
POST http://127.0.0.1:5000
```

webhook-repo/
│
├── app/
│   ├── __init__.py           # create_app() initializes Flask app, MongoDB, and blueprints
│   ├── extensions.py         # MongoDB setup (collection)
│   └── webhook/
│       ├── __init__.py
│       └── routes.py         # webhook route: /webhook, handles push/pull/merge
│
├── templates/
│   └── index.html            # dashboard showing events
│
├── run.py                    # entry point for Flask app
├── requirements.txt
└── README.md



