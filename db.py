from pymongo import MongoClient
from datetime import datetime, timedelta
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["url_uploader_bot"]
users_col = db["users"]
files_col = db["files"]

# Log new user
def log_user(user):
    if not users_col.find_one({"_id": user.id}):
        users_col.insert_one({
            "_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "is_premium": False,
            "premium_expiry": None,
            "joined": datetime.utcnow()
        })

# Check premium status
def is_premium(user_id):
    user = users_col.find_one({"_id": user_id})
    if user:
        expiry = user.get("premium_expiry")
        if expiry:
            expiry = datetime.strptime(expiry, "%Y-%m-%d")
            if datetime.utcnow() < expiry:
                return True
            else:
                users_col.update_one({"_id": user_id}, {
                    "$set": {"is_premium": False, "premium_expiry": None}
                })
    return False

# Set premium for user
def set_premium(user_id, days):
    expiry_date = datetime.utcnow() + timedelta(days=days)
    users_col.update_one({"_id": user_id}, {
        "$set": {
            "is_premium": True,
            "premium_expiry": expiry_date.strftime("%Y-%m-%d")
        }
    })

# Log uploaded file
def log_file(user_id, url, filename, size):
    files_col.insert_one({
        "user_id": user_id,
        "url": url,
        "filename": filename,
        "size": size,
        "uploaded_at": datetime.utcnow()
    })
