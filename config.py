import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

MAX_FILE_SIZE_FREE = 4 * 1024 * 1024 * 1024  # 4 GB
MAX_FILE_SIZE_PREMIUM = 100 * 1024 * 1024 * 1024  # 100 GB (adjustable)
