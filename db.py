from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["UploaderBot"]
users_col = db["users"]
files_col = db["files"]

def log_user(user):
    if not users_col.find_one({"_id": user.id}):
        users_col.insert_one({
            "_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "is_premium": False
        })

def log_file(user_id, url, file_name, size):
    files_col.insert_one({
        "user_id": user_id,
        "url": url,
        "file_name": file_name,
        "size": size
    })

def is_premium(user_id):
    user = users_col.find_one({"_id": user_id})
    return user and user.get("is_premium", False)
