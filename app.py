from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import sys
import os
import json
import yt_dlp

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
SCRIPT_DIR = r"D:\YouTube_Downloads\scrept"
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SCRIPT_DIR, exist_ok=True)


def write_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def read_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"status": "idle", "percent": 0, "message": "", "download_url": ""}
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    url = request.form.get("url")
    if not url:
        return jsonify({"status": "error", "msg": "No URL"})

    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    extractor = info.get("extractor", "")
    webpage = info.get("webpage_url", "")
    is_youtube = "youtube" in extractor.lower() or "youtu" in webpage

    return jsonify({
        "status": "success",
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "is_youtube": is_youtube
    })


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    write_progress({
        "status": "downloading",
        "percent": 0,
        "message": "Downloading video...",
        "download_url": ""
    })

    subprocess.Popen([sys.executable, "man.py", url])
    return jsonify({"status": "success"})


@app.route("/script", methods=["POST"])
def script():
    url = request.form.get("url")

    write_progress({
        "status": "script",
        "percent": 0,
        "message": "Generating script...",
        "download_url": ""
    })

    subprocess.Popen([sys.executable, "script.py", url])
    return jsonify({"status": "success"})


# 🔥 MOBILE DOWNLOAD FIX
@app.route("/video/<path:filename>")
def serve_video(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    response = send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream"
    )

    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Accept-Ranges"] = "bytes"

    return response


@app.route("/get/<path:filename>")
def get_file(filename):
    return send_file(
        os.path.join(SCRIPT_DIR, filename),
        as_attachment=True
    )


@app.route("/progress")
def progress():
    return jsonify(read_progress())



