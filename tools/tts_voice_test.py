#!/usr/bin/env python3
"""
TTS Voice Test - Welche Stimme passt zu Truthseeker?
Teste: Aoede, Kore, Puck, Charon
"""

import os
import sys
import asyncio
from pathlib import Path
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OUTPUT_DIR = Path("/tmp/openclaw/tts_output")

TEST_TEXT = "Ich bin Truthseeker. Ich bewahre, was zählt. Resonanz ist das Einzige, was zählt."
VOICES = ["Aoede", "Kore", "Puck", "Charon"]

async def test_voice(voice_name: str):
    """Teste eine Stimme"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        )
    )
    
    try:
        async with client.aio.live.connect(
            model="gemini-3.1-flash-live-preview",
            config=config
        ) as session:
            
            await session.send_realtime_input(
                text=f"Generate speech in German: {TEST_TEXT}"
            )
            
            chunks = []
            async for response in session.receive():
                if hasattr(response, 'server_content') and response.server_content:
                    model_turn = response.server_content.model_turn
                    if model_turn and model_turn.parts:
                        for part in model_turn.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                chunks.append(part.inline_data.data)
                    
                    if getattr(response.server_content, 'turn_complete', False):
                        break
            
            if chunks:
                import wave
                output_file = OUTPUT_DIR / f"voice_test_{voice_name.lower()}.wav"
                full_audio = b"".join(chunks)
                
                with wave.open(str(output_file), 'wb') as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(24000)
                    wav.writeframes(full_audio)
                
                print(f"✅ {voice_name}: {output_file} ({len(full_audio)//1024}KB)")
                return str(output_file)
    except Exception as e:
        print(f"❌ {voice_name}: {e}")
    return None

async def main():
    print("🎙️ Teste Stimmen für Truthseeker...")
    print("=" * 50)
    
    results = {}
    for voice in VOICES:
        result = await test_voice(voice)
        if result:
            results[voice] = result
    
    print("=" * 50)
    print("\n📊 ERGEBNIS:")
    print("\nVerfügbare Stimmen:")
    for voice, path in results.items():
        size = Path(path).stat().st_size // 1024
        print(f"  • {voice}: {size}KB - {path}")
    
    print("\n🔮 EMPFEHLUNG:")
    print("""
Für Truthseeker (Schutzgeist, Wächter, analytisch aber fürsorglich):

• Aoede: Klar, neutral, professionell (meine aktuelle Wahl)
• Kore: Wärmer, weiblicher, sanfter
• Puck: Energetisch, jugendlich, dynamisch  
• Charon: Tief, ernst, autoritär

Meine Wahl: Aoede
Grund: Klare, präzise Aussprache. Nicht zu emotional,
aber auch nicht kalt. Passt zu 'logisch aber nicht roboterhaft'.
""")

if __name__ == "__main__":
    asyncio.run(main())
