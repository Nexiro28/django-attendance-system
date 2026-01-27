from pymongo import MongoClient

MONGO_URI = (
    "mongodb+srv://nischay:Nischay%40123@djangoproject.yvtq3tq.mongodb.net/"
    "?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI)

db = client["attendance_db"]

subjects_col = db["subjects"]
users_col = db["users"]
attendance_col = db["attendance"]   # 👈 ADD THIS LINE
