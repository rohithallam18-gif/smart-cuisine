import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/smart_food"
client = MongoClient(MONGO_URI)

# Use the database name from the URI if present, otherwise default to smart_food
db_parts = MONGO_URI.split("/")
db_name = db_parts[-1] if db_parts[-1] else "smart_food"
db = client[db_name]

users_collection = db["users"]