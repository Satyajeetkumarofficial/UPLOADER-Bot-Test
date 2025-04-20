import os
import requests
import yt_dlp
import shutil
import uuid
import tempfile

def generate_temp_file(name="file"):
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f"{name}_{uuid.uuid4().hex}")

# Download from direct link
def download_from_url(url, size_limit):
    local_filename = generate_temp_file("direct")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = 0
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                total_size += len(chunk)
                if total_size > size_limit:
                    f.close()
                    os.remove(local_filename)
                    raise Exception("File exceeds limit.")
                f.write(chunk)
    return local_filename

# YouTube Download
def download_youtube(url):
    output = generate_temp_file("yt")
    ydl_opts = {
        'outtmpl': output + '.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for ext in ['mp4', 'mkv', 'webm']:
        file = output + f'.{ext}'
        if os.path.exists(file):
            return file
    raise Exception("YouTube download failed.")

# Instagram Download
def download_instagram(url):
    output = generate_temp_file("insta")
    ydl_opts = {
        'outtmpl': output + '.%(ext)s',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir(tempfile.gettempdir()):
        if file.startswith(os.path.basename(output)):
            return os.path.join(tempfile.gettempdir(), file)
    raise Exception("Instagram download failed.")

# Facebook Download
def download_facebook(url):
    return download_instagram(url)  # Same yt_dlp logic

# Terabox Dummy (replace with real logic later)
def download_terabox(url):
    raise Exception("Terabox download not implemented yet.")

# Google Drive Dummy (replace with real logic later)
def download_gdrive(url):
    raise Exception("Google Drive download not implemented yet.")

# MediaFire Dummy (replace with real logic later)
def download_mediafire(url):
    raise Exception("MediaFire download not implemented yet.")
