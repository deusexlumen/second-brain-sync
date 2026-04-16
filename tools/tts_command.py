#!/usr/bin/env python3
"""
TTS Command Tool für Discord
Usage: !tts [text]
Generiert Audio via Gemini 3.1 Flash Live und gibt Dateipfad zurück
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

# Füge workspace/tools zum Pfad hinzu
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from tts_31live import Gemini31LiveTTS

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def tts_command(text: str, language: str = "German") -> str:
    """
    Generiert TTS für Discord
    
    Returns:
        Dateipfad zur WAV-Datei oder Fehlermeldung
    """
    if not text or not text.strip():
        return "❌ Fehler: Kein Text angegeben. Usage: !tts [Text]"
    
    if not GEMINI_API_KEY:
        return "❌ Fehler: GEMINI_API_KEY nicht gesetzt"
    
    try:
        # TTS generieren
        tts = Gemini31LiveTTS()
        result = asyncio.run(tts.generate_speech(text, language))
        
        if result and Path(result).exists():
            # Kurze Antwort für Discord
            file_size = Path(result).stat().st_size
            return f"🎙️ TTS erstellt: `{Path(result).name}` ({file_size//1024}KB)\n📎 Datei: `{result}`"
        else:
            return "❌ TTS Generierung fehlgeschlagen"
            
    except Exception as e:
        return f"❌ Fehler: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Alle Argumente als Text zusammenführen
        text = " ".join(sys.argv[1:])
        print(tts_command(text))
    else:
        print("Usage: !tts [Text]")
        print("Beispiel: !tts Hallo zusammen!")
