#!/usr/bin/env python3
"""
Audio Transkription Tool mit Groq Whisper API
Nutzt: whisper-large-v3-turbo
Erstellt von: Truthseeker (Kimi Claw)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Config laden
def load_config():
    """Lädt API Key aus der Config-Datei"""
    env_path = Path(__file__).parent.parent / "config" / "groq.env"
    if env_path.exists():
        load_dotenv(env_path)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Fehler: GROQ_API_KEY nicht gefunden!")
        print(f"   Erwartet in: {env_path}")
        sys.exit(1)
    return api_key

def transcribe_audio(audio_path, model="whisper-large-v3-turbo", temperature=0):
    """
    Transkribiert eine Audio-Datei mit Groq Whisper
    
    Args:
        audio_path: Pfad zur Audio-Datei
        model: Whisper-Modell (default: whisper-large-v3-turbo)
        temperature: Sampling-Temperatur (0 = deterministisch)
    
    Returns:
        Transkriptionstext oder None bei Fehler
    """
    api_key = load_config()
    client = Groq(api_key=api_key)
    
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"❌ Fehler: Datei nicht gefunden: {audio_path}")
        return None
    
    print(f"🎙️  Transkribiere: {audio_file.name}")
    print(f"   Modell: {model}")
    print(f"   Größe: {audio_file.stat().st_size / 1024:.1f} KB")
    print("-" * 50)
    
    try:
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file.name, file.read()),
                model=model,
                temperature=temperature,
                response_format="verbose_json",
                language="de"  # Deutsch als Default
            )
        
        return transcription.text
        
    except Exception as e:
        print(f"❌ Transkriptions-Fehler: {e}")
        return None

def main():
    """CLI Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audio-Transkription mit Groq Whisper"
    )
    parser.add_argument(
        "audio_file",
        help="Pfad zur Audio-Datei (.m4a, .mp3, .wav, etc.)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output-Datei (optional, sonst stdout)"
    )
    parser.add_argument(
        "--lang", "-l",
        default="de",
        help="Sprache (default: de)"
    )
    
    args = parser.parse_args()
    
    result = transcribe_audio(args.audio_file)
    
    if result:
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result, encoding="utf-8")
            print(f"\n✅ Gespeichert in: {output_path}")
        else:
            print("\n" + "=" * 50)
            print("TRANSKRIPTION:")
            print("=" * 50)
            print(result)
            print("=" * 50)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
