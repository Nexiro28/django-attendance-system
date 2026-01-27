from pymongo import MongoClient

import os

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["attendance_db"]

subjects_col = db["subjects"]
users_col = db["users"]
attendance_col = db["attendance"]   # 👈 ADD THIS LINE
