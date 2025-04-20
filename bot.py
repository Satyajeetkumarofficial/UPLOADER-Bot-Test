from pyrogram import Client, filters
from pyrogram.types import Message
import os
from helpers import (
    download_from_url, download_youtube, download_instagram,
    download_facebook, download_terabox, download_mediafire,
    download_gdrive
)
from config import *
from db import log_user, log_file, is_premium

app = Client("url_uploader_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.command("start"))
async def start(client, message: Message):
    log_user(message.from_user)
    await message.reply_text("Welcome to the URL Uploader Bot!\n\nSend /upload <url> to begin.")


@app.on_message(filters.command("upload") & filters.private)
async def upload_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /upload <url>")

    url = message.command[1]
    user = message.from_user
    log_user(user)

    premium = is_premium(user.id)
    limit = MAX_FILE_SIZE_PREMIUM if premium else MAX_FILE_SIZE_FREE

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

        file_size = os.path.getsize(file_path)
        if file_size > limit:
            os.remove(file_path)
            raise Exception("File exceeds your limit.")

        log_file(user.id, url, os.path.basename(file_path), file_size)
        await message.reply_document(file_path)

        # Send log to log channel
        if LOG_CHANNEL:
            await app.send_message(
                int(LOG_CHANNEL),
                f"📥 File Uploaded by [{user.first_name}](tg://user?id={user.id})\n"
                f"**URL:** `{url}`\n"
                f"**File:** `{os.path.basename(file_path)}`\n"
                f"**Size:** `{round(file_size / (1024 * 1024), 2)} MB`"
            )

        os.remove(file_path)

    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{e}`")


app.run()
