from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format = data.get('format', 'mp4')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if format not in ['mp4', 'mp3']:
        return jsonify({'error': 'Invalid format. Only "mp4" or "mp3" is allowed.'}), 400

    download_folder = 'downloads'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # ydl_opts = {
    #     'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
    #     'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }] if format == 'mp3' else [],
    #     'quiet': True,
    # }
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best' if format == 'mp4' else 'bestaudio/best',
        'merge_output_format': 'mp4' if format == 'mp4' else None,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }] if format == 'mp4' else [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    def remove_file(file_url):
        try:
            os.remove(file_url)
        except OSError as e:
            print(f"Error: {file_url} : {e.strerror}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path  = os.path.join(download_folder, f"{info_dict['title']}.{format}")
            # return jsonify({
            #     'message': 'Download successful',
            #     'title': info_dict['title'],
            #     'file_url': file_url
            # }), 200
            return send_file(file_path, as_attachment=True, download_name=f"{info_dict['title']}.{format}")
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': 'Failed to download video'}), 500
    # finally:
    #     os.remove(file_url)

@app.route('/video-info', methods=['GET'])
def get_video_info():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info_dict.get('title', 'Unknown Title')
            })
    except Exception as e:
        print(f"Error retrieving video info: {e}")
        return jsonify({'error': 'Failed to retrieve video information'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
