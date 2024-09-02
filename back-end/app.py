from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import re

app = Flask(__name__)

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(new_filename):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1
    return new_filename

OUTPUT_DIR = 'downloads'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format = data.get('format', 'mp4')

    if not url:
        return jsonify({"error": "URL is required"}), 400
    if format not in ['mp4', 'mp3']:
        return jsonify({"error": "Invalid format. Supported formats: mp4, mp3"}), 400

    try:
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'video')
            filename = f"{clean_filename(title)}.mp3" if format == 'mp3' else f"{clean_filename(title)}.mp4"
            unique_filename = get_unique_filename(os.path.join(OUTPUT_DIR, filename))

        ydl_opts_download = {
            'format': 'bestaudio/best' if format == 'mp3' else 'best',
            'outtmpl': unique_filename,
            'ffmpeg_location': 'path_to_ffmpeg',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }] if format == 'mp3' else [],
            'postprocessor_args': ['-ar', '16000'] if format == 'mp3' else [],
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])

        return send_file(unique_filename, as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
