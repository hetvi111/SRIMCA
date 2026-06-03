from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Get database
db = client[DB_NAME]

# Define collections
users_collection = db["users"]
notices_collection = db["notices"]
events_collection = db["events"]
visitors_collection = db["visitors"]
notifications_collection = db["notifications"]
chat_history_collection = db["chat_history"]


def get_db():
    """Get database instance"""
    return db


def get_collection(name):
    """Get specific collection"""
    return db[name]
