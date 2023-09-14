from fastapi import FastAPI
from pymongo import MongoClient
import traceback  # Import the traceback module

app = FastAPI()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fetch']
collection = db['collections']

@app.post("/store_profile_data/")
async def store_profile_data(profile_data: dict):
    try:
        # Insert the profile data into MongoDB
        result = collection.insert_one(profile_data)
        return {"message": "Profile data saved successfully", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        traceback.print_exc()  # Log the exception traceback
        return {"error": f"Error occurred while saving profile data: {str(e)}"}
