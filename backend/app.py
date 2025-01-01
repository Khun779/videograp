from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import logging
from download_video import download_video

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    logging.debug(f"Request payload: {data}")
    url = data.get('url')
    logging.debug(f"Received URL: {url}")
    output_path = 'downloads'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        logging.debug(f"Attempting to download video from URL: {url}")
        video_path = download_video(url, output_path)
        logging.debug(f"Video downloaded to: {video_path}")
        return send_file(video_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Error downloading video: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_video():
    data = request.json
    video_path = data.get('video_path')
    if video_path and os.path.exists(video_path):
        os.remove(video_path)
        return jsonify({"message": "Video deleted"})
    return jsonify({"error": "Video path not found"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)