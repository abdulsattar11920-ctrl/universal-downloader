
# man.py
import sys
import os
import json
import yt_dlp
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

if len(sys.argv) < 2:
    sys.exit(1)

url = sys.argv[1]


def write_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


write_progress({
    "status": "downloading",
    "percent": 5,
    "message": "Starting download...",
    "download_url": ""
})


ydl_opts = {
    "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),  # mobile safe
    "merge_output_format": "mp4",
    "quiet": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mp4")]

if not files:
    write_progress({
        "status": "error",
        "percent": 100,
        "message": "MP4 file not found",
        "download_url": ""
    })
    sys.exit(1)

latest = max(
    files,
    key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_DIR, f))
)

write_progress({
    "status": "done",
    "percent": 100,
    "message": "Video ready",
    "download_url": f"/video/{latest}"
})
