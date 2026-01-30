import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from a .env file
# This lets us keep sensitive info like database URLs out of your code
load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB using the URI
client = MongoClient(MONGO_URI)
# Select the database to use
db = client["webhook_db"]
# Select the collection within the database
collection = db["events"]

def init_extensions(app):
    """
    Attach MongoDB client, database, and collection to the Flask app instance.
    This makes it easy to access the database from anywhere in the app.
    """
    app.mongo_client = client
    app.mongo_db = db
    app.mongo_collection = collection
