#!/usr/bin/env python3
"""
Discord TTS Uploader
Sendet TTS-Audio direkt an Discord
Usage: discord_tts_upload.py <channel_id> <audio_file> [text]
"""

import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: discord_tts_upload.py <channel_id> <audio_file> [text]")
        sys.exit(1)
    
    channel_id = sys.argv[1]
    audio_file = sys.argv[2]
    text = sys.argv[3] if len(sys.argv) > 3 else "🎙️ TTS Audio"
    
    if not Path(audio_file).exists():
        print(f"❌ Datei nicht gefunden: {audio_file}")
        sys.exit(1)
    
    # Discord Action JSON ausgeben (für OpenClaw)
    action = {
        "action": "sendMessage",
        "to": f"channel:{channel_id}",
        "content": f"🎙️ **Truthseeker TTS**\n\\"{text[:100]}{'...' if len(text) > 100 else ''}\\"",
        "mediaUrl": f"file://{audio_file}"
    }
    
    print(json.dumps(action, indent=2))
    print("\n✅ Discord Action bereit. Kann an OpenClaw discord tool übergeben werden.")

if __name__ == "__main__":
    main()
