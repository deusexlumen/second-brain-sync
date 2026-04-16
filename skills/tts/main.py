#!/usr/bin/env python3
"""
Skill: tts
Description: Text-to-Speech mit Gemini 3.1 Flash Live
Usage: !tts [Text]
"""

import os
import sys
import asyncio

# Füge tools zum Pfad hinzu
sys.path.insert(0, '/root/.openclaw/workspace/tools')

from tts_31live import Gemini31LiveTTS

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    # Text aus Argumenten zusammenbauen
    if len(sys.argv) < 2:
        print("""🎙️ **TTS - Text-to-Speech**

**Usage:**
```
!tts Hallo zusammen, das ist meine Stimme
```

**Funktion:**
Generiert natürliche KI-Sprache via Gemini 3.1 Flash Live.

**Output:**
WAV-Datei (24kHz, hochwertig)

*Lifehack: Live API → Audio-Datei* 😎
""")
        return
    
    text = " ".join(sys.argv[1:])
    
    if not GEMINI_API_KEY:
        print("❌ Fehler: GEMINI_API_KEY nicht gesetzt")
        sys.exit(1)
    
    print(f"🎙️ Generiere TTS für: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
    print("⏳ Bitte warten...")
    
    try:
        tts = Gemini31LiveTTS()
        result = asyncio.run(tts.generate_speech(text, "German"))
        
        if result and os.path.exists(result):
            file_size = os.path.getsize(result) // 1024
            print(f"""
✅ **TTS erstellt!**

📁 Datei: `{result}`
📊 Größe: {file_size} KB
🔊 Format: WAV (24kHz, 16-bit)

⚠️ **Hinweis:** Discord-Upload kommt bald!
(aktuell: Datei manuell hochladen)
""")
        else:
            print("❌ TTS Generierung fehlgeschlagen")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Fehler: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
