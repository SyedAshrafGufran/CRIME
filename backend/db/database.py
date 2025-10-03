# db/database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# MongoDB connection URL
load_dotenv() 

# MongoDB Atlas connection string is loaded from the environment variable
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
client = MongoClient(MONGO_DB_URL)

# Access the database and collection
db = client.criminal_records_db
fir_collection = db.fir_records

def add_fir_record(record: dict):
    """Inserts a new FIR record into the MongoDB collection."""
    try:
        fir_collection.insert_one(record)
        return {"status": "success", "message": "Record added to MongoDB."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_fir_by_case_id(case_id: str):
    """Retrieves a single FIR record from the MongoDB collection."""
    return fir_collection.find_one({"case_id": case_id})

def update_fir_record(case_id: str, updates: dict):
    """Updates an existing FIR record."""
    fir_collection.update_one({"case_id": case_id}, {"$set": updates})