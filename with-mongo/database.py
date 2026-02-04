from pymongo import MongoClient
import os

# --- MongoDB Connection ---
# Load the MongoDB connection string from an environment variable if it exists,
# otherwise use a default value for local development.
# This is a good practice for managing configuration secrets.
MONGO_CONNECTION_STRING = os.getenv("MONGO_URL", "mongodb://localhost:27017/")

# Create a MongoDB client, database, and collection.
# These will be shared across the application.
client = MongoClient(MONGO_CONNECTION_STRING)
db = client["fastapi_mongo_crud"]
collection = db["items"]

def get_db():
    """
    Returns the default MongoDB database instance.
    """
    return db

def get_collection():
    """
    Returns the default MongoDB collection instance.
    """
    return collection
