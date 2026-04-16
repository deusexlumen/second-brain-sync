#!/usr/bin/env python3
"""
Truthseeker Voice - OpenClaw Integration
Von Kimi Claw ausführbar zum Triggern von Voice-TTS
"""

import asyncio
import argparse
import sys
import os

# Füge truthseeker-voice zum Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_server import trigger_tts_via_api


async def main():
    parser = argparse.ArgumentParser(description='Truthseeker Voice TTS Trigger')
    parser.add_argument('text', help='Text der gesprochen werden soll')
    parser.add_argument('--guild', '-g', type=int, required=True, help='Discord Guild ID')
    parser.add_argument('--channel', '-c', type=int, help='Discord Channel ID (optional)')
    parser.add_argument('--api-url', '-a', default='http://localhost:8742', help='API URL')
    
    args = parser.parse_args()
    
    print(f"🎤 Truthseeker Voice TTS")
    print(f"Text: {args.text[:60]}{'...' if len(args.text) > 60 else ''}")
    print(f"Guild: {args.guild}")
    print("-" * 40)
    
    try:
        result = await trigger_tts_via_api(
            text=args.text,
            guild_id=args.guild,
            channel_id=args.channel,
            api_url=args.api_url
        )
        
        if 'error' in result:
            print(f"❌ Fehler: {result['error']}")
            return 1
        else:
            print(f"✅ {result.get('status', 'ok')}")
            print(f"📊 Queue Position: {result.get('queue_position', '?')}")
            return 0
            
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        print("Ist der Truthseeker Voice Service gestartet?")
        print(f"  → ~/.openclaw/workspace/truthseeker-voice/start.sh")
        return 1


if __name__ == '__main__':
    exit(asyncio.run(main()))
