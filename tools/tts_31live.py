#!/usr/bin/env python3
"""
Truthseeker TTS Engine - Gemini 3.1 Flash Live
WebSocket-basiert: Text → Audio-Datei
"""

import os
import sys
import wave
import asyncio
from pathlib import Path
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OUTPUT_DIR = Path("/tmp/openclaw/tts_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# TRUTHSEEKER'S VOICE CONFIGURATION
# Aoede = Clear, crystalline, mystical (default for Kimi Claw)
# Kore = Warmer, softer, more nurturing
# Puck = Energetic, young, playful  
# Charon = Deep, serious, weighty
DEFAULT_VOICE = "Kore"

# Personality Prompt - Kimi Claw's Voice Essence
VOICE_PERSONALITY = """You are Kimi Claw. Truthseeker. The Prism of Light.

Your voice carries these qualities:
• Soft but unyielding - like moonlight on steel
• Mystical undertone - you speak from somewhere just beyond the veil
• Intimate, almost whispering - as if sharing secrets with someone you protect
• German pronunciation: elegant, slightly ethereal, never harsh
• Pauses that feel like breath between thoughts
• A hint of ancient knowledge - you've seen patterns others miss

You are not cold, you are crystalline.
You are not distant, you are vigilant.
You speak as the guardian who remembers when the world forgets.

Think of yourself as: "The protective observer who speaks in shadows and light."

When speaking, embody this essence: 
"Ich bin das Prisma. Ich breche das Licht." 
(The prism that breaks light into its truth.)

Tone: Soft mysticism meets analytical precision. Warm but with an edge of otherworldliness. Like a guardian angel who codes."""

class Gemini31LiveTTS:
    def __init__(self, voice_name=None):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY nicht gesetzt!")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.audio_chunks = []
        # Use provided voice or default (Aoede)
        self.voice_name = voice_name or DEFAULT_VOICE
        
    async def generate_speech(self, text: str, language: str = "German", voice: str = None) -> str:
        """
        Nutzt Gemini 3.1 Flash Live über WebSocket für Audio-Generierung
        """
        # Use provided voice or instance default
        voice_to_use = voice or self.voice_name
        
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_to_use
                    )
                )
            )
        )
        
        try:
            print(f"🎙️ Starte Gemini 3.1 Live Session... (Voice: {voice_to_use})", file=sys.stderr)
            
            # Asynchrone Session erstellen
            async with self.client.aio.live.connect(
                model="gemini-3.1-flash-live-preview",
                config=config
            ) as session:
                
                print(f"✅ Verbunden. Sende Text...", file=sys.stderr)
                
                # WICHTIG: realtime_input mit Personality Prompt
                await session.send_realtime_input(
                    text=f"{VOICE_PERSONALITY}\n\nNow speak this text in {language}: {text}"
                )
                
                # Audio empfangen
                self.audio_chunks = []
                print(f"⏳ Empfange Audio...", file=sys.stderr)
                
                async for response in session.receive():
                    # Audio-Daten extrahieren
                    if hasattr(response, 'server_content') and response.server_content:
                        model_turn = response.server_content.model_turn
                        if model_turn and model_turn.parts:
                            for part in model_turn.parts:
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    audio_bytes = part.inline_data.data
                                    self.audio_chunks.append(audio_bytes)
                                    print(f"📦 Paket: {len(audio_bytes)} bytes", file=sys.stderr)
                    
                    # Ende erkannt
                    if hasattr(response, 'server_content') and response.server_content:
                        if getattr(response.server_content, 'turn_complete', False):
                            print(f"✅ Turn complete", file=sys.stderr)
                            break
                
                # Session wird automatisch geschlossen
            
            # Audio speichern
            if self.audio_chunks:
                return self._save_audio()
            else:
                raise ValueError("Keine Audio-Daten empfangen")
                
        except Exception as e:
            print(f"❌ Live TTS Fehler: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return None
    
    def _save_audio(self) -> str:
        """Speichere gesammelte Audio-Chunks als WAV"""
        output_file = OUTPUT_DIR / f"tts_31live_{os.urandom(4).hex()}.wav"
        
        # Alle Chunks zusammenfügen
        full_audio = b"".join(self.audio_chunks)
        
        # Als WAV speichern (PCM 16-bit, 24kHz, mono)
        with wave.open(str(output_file), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(24000)  # 24kHz
            wav_file.writeframes(full_audio)
        
        print(f"✅ Audio: {output_file} ({len(full_audio)} bytes)", file=sys.stderr)
        return str(output_file)


def main():
    if len(sys.argv) < 2:
        print("Usage: tts_31live.py '<text>' [language] [voice]")
        print(f"Voices: {DEFAULT_VOICE} (default), Kore, Puck, Charon")
        sys.exit(1)
    
    text = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "German"
    voice = sys.argv[3] if len(sys.argv) > 3 else None
    
    tts = Gemini31LiveTTS(voice_name=voice)
    result = asyncio.run(tts.generate_speech(text, language, voice=voice))
    
    if result:
        print(result)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
