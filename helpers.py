import os
import requests
from pytube import YouTube
import re
import shutil

def download_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    file_path = stream.download(output_path="downloads/")
    return file_path

def download_from_url(url, limit):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("content-length", 0))
    if file_size > limit:
        raise Exception("File size exceeds your allowed limit.")

    os.makedirs("downloads", exist_ok=True)
    filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join("downloads", filename)

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(1024 * 1024):
            f.write(chunk)
    return file_path

def download_instagram(url):
    api = "https://saveinsta.io/core/ajax.php"
    data = {"q": url, "t": "media", "lang": "en"}
    headers = {"x-requested-with": "XMLHttpRequest"}
    r = requests.post(api, data=data, headers=headers)
    media_url = re.search(r'source src="([^"]+)"', r.text)
    if not media_url:
        raise Exception("Failed to extract Instagram media.")
    return download_from_url(media_url.group(1), 4294967296)

def download_facebook(url):
    api = "https://fbdownloader.online/api/ajaxSearch"
    data = {"q": url}
    headers = {"x-requested-with": "XMLHttpRequest"}
    r = requests.post(api, data=data, headers=headers)
    video_url = re.search(r'"url":"(https[^"]+)"', r.text)
    if not video_url:
        raise Exception("Failed to extract Facebook video.")
    return download_from_url(video_url.group(1).replace("\\u0026", "&"), 4294967296)

def download_terabox(url):
    raise Exception("Terabox support needs advanced scraping — coming soon!")

def download_mediafire(url):
    page = requests.get(url).text
    dl_url = re.search(r'href="(https://download[^"]+)"', page)
    if not dl_url:
        raise Exception("Mediafire download link not found.")
    return download_from_url(dl_url.group(1), 4294967296)

def download_gdrive(url):
    file_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', url) or re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if not file_id_match:
        raise Exception("Google Drive file ID not found.")
    file_id = file_id_match.group(1)
    gdown_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return download_from_url(gdown_url, 4294967296)
