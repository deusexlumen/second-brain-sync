#!/usr/bin/env python3
"""Analyze video using Gemini 3.1 Flash Lite."""
import os
import sys
import time
from google import genai
from google.genai import types

# Get API key
api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyDfSX88OXe9BKE1-TaMAcwVAdYseSdH8MQ"
client = genai.Client(api_key=api_key)

video_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bewusstseins_algorithmus.mp4"

# Upload video
print(f"Uploading video: {video_path}...", file=sys.stderr)
uploaded_file = client.files.upload(file=video_path)
print(f"Uploaded: {uploaded_file.name}", file=sys.stderr)

# Wait for file to be active
print("Waiting for file processing...", file=sys.stderr)
max_wait = 60
waited = 0
while waited < max_wait:
    file_info = client.files.get(name=uploaded_file.name)
    if file_info.state == "ACTIVE":
        print(f"File is ACTIVE after {waited}s", file=sys.stderr)
        break
    print(f"  State: {file_info.state}... ({waited}s)", file=sys.stderr)
    time.sleep(5)
    waited += 5
else:
    print("Timeout waiting for file", file=sys.stderr)
    sys.exit(1)

# Get custom prompt or use default
prompt = sys.argv[2] if len(sys.argv) > 2 else """Analysiere dieses Video detailliert.

Bitte:
1. Fasse den Inhalt zusammen
2. Identifiziere die Hauptthesen/Punkte  
3. Gib deine Einschätzung zur Qualität/Plausibilität
4. Nenne interessante Details oder Kontroversen

Antworte auf Deutsch."""

print("Analyzing with Gemini 3.1 Flash Lite...", file=sys.stderr)
response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents=[uploaded_file, prompt],
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high")
    )
)

print(response.text)
