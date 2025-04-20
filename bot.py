from pyrogram import Client, filters
from pyrogram.types import Message
import os
from helpers import download_from_url, download_youtube, download_instagram, download_facebook, download_terabox, download_mediafire, download_gdrive
from config import *

app = Client("url_uploader_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("Welcome to the URL Uploader Bot!\n\nSend /upload <url> to begin.")

@app.on_message(filters.command("upload") & filters.private)
async def upload_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /upload <url>")
    
    url = message.command[1]
    user_id = str(message.from_user.id)
    is_premium = user_id in PREMIUM_USERS
    limit = MAX_FILE_SIZE_PREMIUM if is_premium else MAX_FILE_SIZE_FREE

    try:
        if "youtube.com" in url or "youtu.be" in url:
            file_path = download_youtube(url)

        elif "instagram.com" in url:
            file_path = download_instagram(url)

        elif "facebook.com" in url:
            file_path = download_facebook(url)

        elif "terabox" in url or "1024tera.com" in url:
            file_path = download_terabox(url)

        elif "drive.google.com" in url:
            file_path = download_gdrive(url)

        elif "mediafire.com" in url:
            file_path = download_mediafire(url)

        else:
            file_path = download_from_url(url, limit)

        await message.reply_document(file_path)
        os.remove(file_path)

    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{e}`")

app.run()
