from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json')

@app.route('/sw.js')
def sw():
    return send_file('sw.js')

@app.route('/icon.png')
def icon():
    return send_file('icon.png')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL kosong'}), 400

    try:
        tmpdir = tempfile.mkdtemp()
        ydl_opts = {
            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
