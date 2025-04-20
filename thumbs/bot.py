import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import *
from db import log_user, is_premium, set_premium, log_file
from helpers import *
from datetime import datetime

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log_user(user)
    await update.message.reply_text(
        f"Hello {user.first_name},\nI can upload files from Direct Links, YouTube, Instagram, Facebook and more.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Join Updates Channel", url="https://t.me/YourChannel")
        ]])
    )

async def addpremium(update: Update, context: CallbackContext):
    if update.effective_user.id != 123456789:  # Replace with your Telegram ID
        return await update.message.reply_text("Unauthorized.")
    try:
        user_id = int(context.args[0])
        days = int(context.args[1])
        set_premium(user_id, days)
        await update.message.reply_text(f"Premium added to {user_id} for {days} days.")
    except:
        await update.message.reply_text("Usage: /addpremium <user_id> <days>")

async def handle_url(update: Update, context: CallbackContext):
    user = update.effective_user
    log_user(user)
    url = update.message.text.strip()
    is_prem = is_premium(user.id)
    size_limit = MAX_FILE_SIZE_PREMIUM if is_prem else MAX_FILE_SIZE_FREE

    try:
        msg = await update.message.reply_text("Downloading...")

        if "youtube.com" in url or "youtu.be" in url:
            file_path = download_youtube(url)
        elif "instagram.com" in url:
            file_path = download_instagram(url)
        elif "facebook.com" in url:
            file_path = download_facebook(url)
        elif "terabox" in url:
            file_path = download_terabox(url)
        elif "drive.google.com" in url:
            file_path = download_gdrive(url)
        elif "mediafire.com" in url:
            file_path = download_mediafire(url)
        else:
            file_path = download_from_url(url, size_limit)

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        if file_size > size_limit:
            os.remove(file_path)
            return await msg.edit_text("File is too large for your account type.")

        await msg.edit_text("Uploading...")

        with open(file_path, "rb") as f:
            await update.message.reply_document(f, filename=filename)

        log_file(user.id, url, filename, file_size)
        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpremium", addpremium))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
