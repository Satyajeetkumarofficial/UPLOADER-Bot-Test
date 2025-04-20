# Telegram URL Uploader Bot

A bot to upload/download files from YouTube, Instagram, Facebook, Direct Links, etc.

### Features:
- Free user: Max 4GB
- Premium: Max 100GB (adjustable)
- Log channel, MongoDB, thumbnail support

### Deploy on Koyeb:
1. Fork repo or upload files
2. Set these ENV vars:
   - BOT_TOKEN
   - API_ID
   - API_HASH
   - MONGO_URI
   - LOG_CHANNEL
3. Click “Deploy Now” on Koyeb and link your GitHub repo

### Run Locally:
```bash
pip install -r requirements.txt
python bot.py
