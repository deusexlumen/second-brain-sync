#!/usr/bin/env python3
"""
Truthseeker Voice Skill — OpenClaw Integration

Managed den Discord Voice Bot und stellt Commands zur Verfügung.
"""

import asyncio
import subprocess
import sys
import time
import os
import requests
from pathlib import Path

# Config
VOICE_DIR = Path.home() / ".openclaw" / "workspace" / "truthseeker-voice"
LOG_FILE = VOICE_DIR / "truthseeker_live.log"
PID_FILE = VOICE_DIR / ".voice_pid"
API_URL = "http://localhost:8742"


def is_voice_running() -> bool:
    """Prüfe ob Voice Bot läuft"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "truthseeker_live.py"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False


def start_voice() -> bool:
    """Starte Voice Bot"""
    try:
        # Alten Prozess killen falls hängt
        subprocess.run(["pkill", "-f", "truthseeker_live.py"], capture_output=True)
        time.sleep(1)
        
        # Neu starten
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        process = subprocess.Popen(
            [sys.executable, str(VOICE_DIR / "truthseeker_live.py")],
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
            cwd=str(VOICE_DIR),
            env=env,
            start_new_session=True  # Damit er nicht gekillt wird
        )
        
        # PID speichern
        PID_FILE.write_text(str(process.pid))
        
        # Warten bis API bereit
        for i in range(10):
            time.sleep(1)
            try:
                requests.get(f"{API_URL}/health", timeout=1)
                return True
            except:
                continue
        
        return True
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")
        return False


def stop_voice() -> bool:
    """Stoppe Voice Bot"""
    try:
        subprocess.run(["pkill", "-f", "truthseeker_live.py"], capture_output=True)
        if PID_FILE.exists():
            PID_FILE.unlink()
        return True
    except Exception as e:
        print(f"❌ Fehler beim Stoppen: {e}")
        return False


def voice_status() -> dict:
    """Voice Bot Status"""
    status = {
        "running": is_voice_running(),
        "api_ready": False,
        "discord_connected": False
    }
    
    if status["running"]:
        try:
            resp = requests.get(f"{API_URL}/status", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                status["api_ready"] = True
                status["discord_connected"] = data.get("discord_connected", False)
                status["bot_user"] = data.get("bot_user", "Unknown")
        except:
            pass
    
    return status


def voice_join(guild_id: str = None, channel_id: str = None) -> bool:
    """Voice Channel beitreten"""
    if not is_voice_running():
        if not start_voice():
            return False
        time.sleep(3)
    
    try:
        payload = {}
        if guild_id:
            payload["guild_id"] = guild_id
        if channel_id:
            payload["channel_id"] = channel_id
            
        resp = requests.post(
            f"{API_URL}/join",
            json=payload,
            timeout=5
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Join Fehler: {e}")
        return False


def voice_leave() -> bool:
    """Voice Channel verlassen"""
    try:
        resp = requests.post(f"{API_URL}/leave", timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ Leave Fehler: {e}")
        return False


def voice_say(text: str, guild_id: str = None, channel_id: str = None) -> bool:
    """TTS im Voice Channel"""
    if not is_voice_running():
        print("❌ Voice Bot nicht aktiv. Zuerst !voice_join")
        return False
    
    try:
        payload = {"text": text}
        if guild_id:
            payload["guild_id"] = int(guild_id)
        if channel_id:
            payload["channel_id"] = int(channel_id)
            
        resp = requests.post(
            f"{API_URL}/speak",
            json=payload,
            timeout=10
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"❌ TTS Fehler: {e}")
        return False


# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Truthseeker Voice Control")
    parser.add_argument("command", choices=["start", "stop", "status", "join", "leave", "say"])
    parser.add_argument("--guild", help="Discord Guild ID")
    parser.add_argument("--channel", help="Discord Channel ID")
    parser.add_argument("--text", help="Text für TTS")
    
    args = parser.parse_args()
    
    if args.command == "start":
        if start_voice():
            print("✅ Voice Bot gestartet")
        else:
            print("❌ Fehler beim Starten")
    
    elif args.command == "stop":
        if stop_voice():
            print("✅ Voice Bot gestoppt")
        else:
            print("❌ Fehler beim Stoppen")
    
    elif args.command == "status":
        status = voice_status()
        print(f"Running: {status['running']}")
        print(f"API Ready: {status['api_ready']}")
        print(f"Discord Connected: {status['discord_connected']}")
        if 'bot_user' in status:
            print(f"Bot User: {status['bot_user']}")
    
    elif args.command == "join":
        if voice_join(args.guild, args.channel):
            print("✅ Voice Channel beigetreten")
        else:
            print("❌ Fehler beim Beitreten")
    
    elif args.command == "leave":
        if voice_leave():
            print("✅ Voice Channel verlassen")
        else:
            print("❌ Fehler beim Verlassen")
    
    elif args.command == "say":
        if not args.text:
            print("❌ --text erforderlich")
        elif voice_say(args.text, args.guild, args.channel):
            print("✅ TTS gesendet")
        else:
            print("❌ Fehler beim TTS")
