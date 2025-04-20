import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# File size limits
MAX_FILE_SIZE_FREE = 4 * 1024 * 1024 * 1024        # 4GB
MAX_FILE_SIZE_PREMIUM = 20 * 1024 * 1024 * 1024     # 20GB (or set as needed)

# Premium users (add your Telegram user IDs as strings)
PREMIUM_USERS = os.getenv("PREMIUM_USERS", "").split(",")

# Optional: Log channel ID (e.g., -1001234567890)
LOG_CHANNEL = os.getenv("LOG_CHANNEL")
