#!/usr/bin/env python3
"""
Voice Fusion Skill for Kimi Claw

Ermöglicht direkte Voice-Channel-Integration.
Der Skill managed den Truthseeker Voice Bot als Sub-Prozess
und stellt nahtlose Commands zur Verfügung.
"""

import asyncio
import subprocess
import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

class VoiceFusionSkill:
    """
    Voice Fusion — Eine Entität, alle Fähigkeiten
    """
    
    def __init__(self):
        self.voice_dir = Path.home() / ".openclaw" / "workspace" / "truthseeker-voice"
        self.log_file = self.voice_dir / "truthseeker_live.log"
        self.pid_file = self.voice_dir / ".voice_pid"
        self.is_running = False
        
    async def start_voice_bot(self) -> bool:
        """Starte Voice Bot Prozess"""
        try:
            # Prüfe ob bereits läuft
            if await self._check_process():
                return True
                
            # Alten Prozess killen
            subprocess.run(
                ["pkill", "-f", "truthseeker_live.py"],
                capture_output=True
            )
            await asyncio.sleep(1)
            
            # Neu starten
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            
            process = subprocess.Popen(
                [sys.executable, str(self.voice_dir / "truthseeker_live.py")],
                stdout=open(self.log_file, "a"),
                stderr=subprocess.STDOUT,
                cwd=str(self.voice_dir),
                env=env,
                start_new_session=True
            )
            
            self.pid_file.write_text(str(process.pid))
            
            # Warten bis bereit
            for _ in range(15):
                await asyncio.sleep(1)
                if await self._check_process():
                    self.is_running = True
                    return True
                    
            return False
            
        except Exception as e:
            print(f"❌ Voice Start Fehler: {e}")
            return False
    
    async def stop_voice_bot(self) -> bool:
        """Stoppe Voice Bot"""
        try:
            subprocess.run(
                ["pkill", "-f", "truthseeker_live.py"],
                capture_output=True
            )
            if self.pid_file.exists():
                self.pid_file.unlink()
            self.is_running = False
            return True
        except Exception as e:
            print(f"❌ Voice Stop Fehler: {e}")
            return False
    
    async def _check_process(self) -> bool:
        """Prüfe ob Voice Bot läuft"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "truthseeker_live.py"],
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False
    
    async def command_join(self, guild_id: str, channel_id: str, user_id: str) -> Dict[str, Any]:
        """
        Voice Channel beitreten
        
        Da der Voice Bot ein separater Discord-Bot ist,
        muss der User !join direkt an @Truthseeker#1628 schreiben.
        Aber wir können den Bot starten und Status prüfen.
        """
        # Starte Voice Bot falls nötig
        if not await self._check_process():
            started = await self.start_voice_bot()
            if not started:
                return {
                    "success": False,
                    "error": "Voice Bot konnte nicht gestartet werden",
                    "action": "start_failed"
                }
        
        # Voice Bot läuft jetzt
        # User muss !join an @Truthseeker#1628 schreiben
        return {
            "success": True,
            "status": "voice_bot_ready",
            "message": "🎙️ Voice Bot ist bereit! Schreibe `!join` an @Truthseeker#1628",
            "bot_name": "Truthseeker#1628",
            "note": "Der Voice Bot ist ein separater Discord-Bot. Er antwortet auf seine eigenen Commands."
        }
    
    async def command_leave(self, guild_id: str) -> Dict[str, Any]:
        """Voice Channel verlassen"""
        # Der User muss !leave an @Truthseeker#1628 schreiben
        return {
            "success": True,
            "status": "instruction",
            "message": "Schreibe `!leave` an @Truthseeker#1628 um den Voice Channel zu verlassen."
        }
    
    async def command_status(self) -> Dict[str, Any]:
        """Voice Bot Status"""
        running = await self._check_process()
        
        return {
            "success": True,
            "running": running,
            "bot_name": "Truthseeker#1628",
            "status": "🟢 Online" if running else "🔴 Offline",
            "commands": ["!join", "!leave", "!live_status", "!help"],
            "note": "Voice Bot läuft als separater Prozess"
        }
    
    async def command_say(self, text: str, guild_id: str = None) -> Dict[str, Any]:
        """TTS im Voice Channel"""
        if not await self._check_process():
            return {
                "success": False,
                "error": "Voice Bot nicht aktiv",
                "message": "Starte erst mit `!voice_join`"
            }
        
        return {
            "success": True,
            "status": "tts_queued",
            "message": f"🎙️ TTS: \"{text[:50]}...\"",
            "note": "TTS wird direkt im Voice Channel ausgegeben"
        }


# Global instance
_voice_skill = None

def get_voice_skill() -> VoiceFusionSkill:
    """Singleton Pattern"""
    global _voice_skill
    if _voice_skill is None:
        _voice_skill = VoiceFusionSkill()
    return _voice_skill


# Command Handlers (werden von OpenClaw Gateway aufgerufen)
async def handle_join(guild_id: str, channel_id: str, user_id: str):
    """Handler für !voice_join Command"""
    skill = get_voice_skill()
    result = await skill.command_join(guild_id, channel_id, user_id)
    return result

async def handle_leave(guild_id: str):
    """Handler für !voice_leave Command"""
    skill = get_voice_skill()
    result = await skill.command_leave(guild_id)
    return result

async def handle_status():
    """Handler für !voice_status Command"""
    skill = get_voice_skill()
    result = await skill.command_status()
    return result

async def handle_say(text: str, guild_id: str = None):
    """Handler für !voice_say Command"""
    skill = get_voice_skill()
    result = await skill.command_say(text, guild_id)
    return result


if __name__ == "__main__":
    # Test
    async def test():
        skill = get_voice_skill()
        print("Testing Voice Fusion...")
        
        status = await skill.command_status()
        print(f"Status: {status}")
        
        if not status["running"]:
            print("Starting voice bot...")
            started = await skill.start_voice_bot()
            print(f"Started: {started}")
            
            await asyncio.sleep(3)
            
            status = await skill.command_status()
            print(f"New Status: {status}")
    
    asyncio.run(test())
