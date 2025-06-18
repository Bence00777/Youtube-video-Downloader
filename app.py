from flask import Flask, request, render_template
import os
import uuid
import subprocess
import yt_dlp

app = Flask(__name__)

FFMPEG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg", "bin", "ffmpeg.exe")

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

def convert_file(input_path, target_format):
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.{target_format}"

    # ffmpeg command
    cmd = [
        FFMPEG_PATH,
        '-i', input_path,
    ]

    if target_format == "mp3":
        cmd += ['-vn', '-ab', '192k', '-ar', '44100', '-y', output_path]
    elif target_format == "mp4":
        cmd += ['-c:v', 'copy', '-c:a', 'aac', '-y', output_path]
    else:
        raise ValueError("Unsupported format")

    subprocess.run(cmd, check=True)
    return output_path

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        target_format = request.form.get("format_choice")
    else:  # GET
        youtube_url = request.args.get("youtube_url")
        target_format = request.args.get("format_choice")

    if not youtube_url or target_format not in ["mp3", "mp4"]:
        return render_template("index.html", error="Invalid input!")

    try:
        downloaded_file = download_video(youtube_url)
        converted_file = convert_file(downloaded_file, target_format)
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)

        success_msg = f"Succes Download and Conversion: {converted_file}"
        return render_template("index.html", success=success_msg)
    except Exception as e:
        return render_template("index.html", error=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
