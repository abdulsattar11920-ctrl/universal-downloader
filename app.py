from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    url = request.form.get("url")
    if not url:
        return jsonify({"status": "error", "msg": "No URL"})

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True
    }

    try:
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

    except Exception as e:
        return jsonify({
            "status": "error",
            "msg": "Link not supported or blocked"
        })


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    quality = request.form.get("quality", "best")

    if not url:
        return jsonify({"status": "error", "msg": "No URL"})

    # yt-dlp direct link extraction (CLOUD SAFE)
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # If multiple formats (YouTube)
            if "url" in info:
                direct_url = info["url"]
            else:
                # pick best video+audio merged
                formats = info.get("formats", [])
                formats = [f for f in formats if f.get("url")]
                direct_url = formats[-1]["url"]

        return jsonify({
            "status": "success",
            "direct_url": direct_url
        })

    except Exception:
        return jsonify({
            "status": "error",
            "msg": "Unable to generate download link"
        })


if __name__ == "__main__":
    app.run(debug=True)
