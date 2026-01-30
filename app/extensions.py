import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["webhook_db"]        # Database
collection = db["events"]        # Collection

def init_extensions(app):
    # Optional: store in app for easy access
    app.mongo_client = client
    app.mongo_db = db
    app.mongo_collection = collection
