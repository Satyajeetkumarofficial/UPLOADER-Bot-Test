from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pyrogram.types import Message
import os
from helpers import (
    download_from_url, download_youtube, download_instagram,
    download_facebook, download_terabox, download_mediafire,
    download_gdrive
)
from config import *
from db import log_user, log_file, is_premium, set_premium
from datetime import datetime

ADMIN_USERS = [123456789]  # Replace with your Telegram user ID

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

        thumb_path = f"thumbs/{user.id}.jpg"
        thumbnail = thumb_path if os.path.exists(thumb_path) else None

        await message.reply_document(
            file_path,
            thumb=thumbnail
        )

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


@app.on_message(filters.photo & filters.private)
async def save_thumbnail(client, message: Message):
    user_id = message.from_user.id
    log_user(message.from_user)
    thumb_path = f"thumbs/{user_id}.jpg"
    await message.download(file_name=thumb_path)
    await message.reply_text("✅ Thumbnail saved successfully!")


@app.on_message(filters.command("clearthumb") & filters.private)
async def clear_thumbnail(client, message: Message):
    thumb_path = f"thumbs/{message.from_user.id}.jpg"
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
        await message.reply_text("❌ Thumbnail removed.")
    else:
        await message.reply_text("No thumbnail was set.")


@app.on_message(filters.command("addpremium") & filters.private)
async def add_premium(client, message: Message):
    if message.from_user.id not in ADMIN_USERS:
        return await message.reply_text("You are not authorized.")

    try:
        _, user_id_str, days_str = message.text.split()
        user_id = int(user_id_str)
        days = int(days_str)

        set_premium(user_id, days)
        await message.reply_text(f"✅ User `{user_id}` granted premium for {days} days.")
    except Exception:
        await message.reply_text("Usage: /addpremium <user_id> <days>")


app.run()
