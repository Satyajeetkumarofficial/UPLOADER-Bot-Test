from pyrogram import Client, filters
from pyrogram.types import Message
import os
from config import BOT_TOKEN, LOG_CHANNEL, FREE_LIMIT
from db import add_user, is_premium
from helpers import (
    download_youtube, download_direct, download_mediafire,
    download_instagram, download_facebook, download_terabox,
    download_gdrive, get_platform
)

bot = Client("UploaderBot", bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(c, m: Message):
    add_user(m.from_user.id)
    await m.reply_text("Hi! Send me a direct or supported link to upload. Use /upload <url>")

@bot.on_message(filters.command("upload"))
async def upload_handler(c, m: Message):
    user_id = m.from_user.id
    add_user(user_id)

    if len(m.command) < 2:
        return await m.reply_text("Please send a link: `/upload <url>`", quote=True)

    url = m.command[1]
    platform = get_platform(url)
    await m.reply_text(f"Downloading from {platform}...", quote=True)

    if platform == "youtube":
        file_path = download_youtube(url)
    elif platform == "mediafire":
        file_path = download_mediafire(url)
    elif platform == "instagram":
        file_path = download_instagram(url)
    elif platform == "facebook":
        file_path = download_facebook(url)
    elif platform == "terabox":
        file_path = download_terabox(url)
    elif platform == "gdrive":
        file_path = download_gdrive(url)
    else:
        file_path = download_direct(url)

    if not os.path.exists(file_path):
        return await m.reply_text(f"Failed to download: {file_path}", quote=True)

    size = os.path.getsize(file_path)
    premium = is_premium(user_id)

    if not premium and size > FREE_LIMIT:
        os.remove(file_path)
        return await m.reply_text("Only premium users can upload files larger than 4GB.")

    try:
        await m.reply_document(document=file_path, caption="Here's your file!")
        await c.send_message(LOG_CHANNEL, f"User: `{user_id}` uploaded a file from `{platform}`")
    except Exception as e:
        await m.reply_text(f"Upload failed: {e}")
    finally:
        os.remove(file_path)

bot.run()
