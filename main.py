from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests
import subprocess
import os
import tempfile

app = Flask(__name__)
CORS(app)

openai.api_key = "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"

# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#     return response

# app.after_request(add_cors_headers)


@app.route("/transcribe", methods=["POST"])
#@cross_origin
def transcribe():
    video_url = request.json["videoUrl"]

    # Download the video file
    video_data = requests.get(video_url).content
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_file:
        video_path = video_file.name
        video_file.write(video_data)

    # Convert video to audio
    audio_path = tempfile.mktemp(suffix=".mp3")
    command = ["ffmpeg", "-i", video_path, "-vn", "-q:a", "0", "-map", "a", audio_path]
    subprocess.run(command, check=True)

    # Transcribe the audio using OpenAI's Whisper API
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # Clean up temporary files
    os.remove(video_path)
    os.remove(audio_path)

    return jsonify({"transcription": transcript})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
