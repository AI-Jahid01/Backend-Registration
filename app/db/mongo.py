# import os
# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# DATABASE_NAME = os.getenv("DATABASE_NAME", "face_attendance")

# _client = AsyncIOMotorClient(MONGO_URI)
# _db = _client[DATABASE_NAME]

# def get_database():
#     return _db

# # below code is for local testing purpose, using synchronous pymongo instead of motor
# # backend/app/db/mongo.py
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("DATABASE_NAME")

# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]

# students_col = db["students"]

# # Ensure index
# students_col.create_index("student_id", unique=True)


# below code is for deployment purpose, using asynchronous motor

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    tls=True,
)

db = client[DATABASE_NAME]
students_col = db["students"]
