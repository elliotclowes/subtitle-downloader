import re
from flask import Flask, request, jsonify
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def convert_webvtt_to_text(webvtt_content):
    webvtt_content = re.sub(r'^WEBVTT\n', '', webvtt_content)
    plain_text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', webvtt_content)
    plain_text = plain_text.replace('\n\n', ' ')
    plain_text = plain_text.replace('\n', ' ')
    plain_text = re.sub(r'(\w+)<\s*\1', r'\1', plain_text)
    plain_text = ' '.join(plain_text.split())
    return plain_text


@app.route('/download_subtitles', methods=['POST'])
def download_subtitles():
    logger.debug("Starting download_subtitles function...")
    url = request.json['url']

    video_id = url.split('=')[-1]
    subtitle_file = f"{video_id}.en.vtt"

    command = ["yt-dlp", "--write-auto-sub", "--sub-lang", "en", "--skip-download", "-o", f"{video_id}.%(ext)s", url]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if result.returncode != 0:
        return jsonify({'error': 'youtube-dl failed', 'details': result.stderr.decode()}), 500

    # Read the subtitle file
    try:
        with open(subtitle_file, 'r') as file:
            subtitles_webvtt = file.read()
    except FileNotFoundError:
        return jsonify({'error': 'Subtitle file not found'}), 500

    # Convert subtitles to plain text
    subtitles_plain_text = convert_webvtt_to_text(subtitles_webvtt)

    # Clean up
    subprocess.run(["rm", subtitle_file])

    return jsonify({'subtitles': subtitles_plain_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
