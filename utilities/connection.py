from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DB_URL")

def create_mongo_connection(url=db_url):
    try:        
        client = MongoClient(url)
        print("Connected to MongoDB successfully")
        return client
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {str(e)}")