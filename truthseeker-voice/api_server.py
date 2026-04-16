"""
Truthseeker Voice - IPC/API Server
Erlaubt externe Trigger (z.B. von OpenClaw/Kimi Claw)
"""

import asyncio
import json
import logging
from typing import Optional
from dataclasses import asdict
from datetime import datetime

from aiohttp import web
import aiohttp

from bot import TruthseekerVoiceBot, TTSRequest

logger = logging.getLogger('truthseeker-api')


class TruthseekerAPI:
    """
    HTTP API für externe Steuerung des Voice Bots
    """
    
    def __init__(self, bot: TruthseekerVoiceBot, host: str = 'localhost', port: int = 8742):
        self.bot = bot
        self.host = host
        self.port = port
        self.app = web.Application()
        self.runner = None
        
        # Routes
        self.app.router.add_post('/speak', self.handle_speak)
        self.app.router.add_post('/join', self.handle_join)
        self.app.router.add_post('/leave', self.handle_leave)
        self.app.router.add_get('/status', self.handle_status)
        self.app.router.add_get('/health', self.handle_health)
        
    async def start(self):
        """Starte den API-Server"""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        logger.info(f"🌐 API Server läuft auf http://{self.host}:{self.port}")
        
    async def stop(self):
        """Stoppe den API-Server"""
        if self.runner:
            await self.runner.cleanup()
            
    async def handle_speak(self, request: web.Request) -> web.Response:
        """
        POST /speak
        Body: {"text": "...", "guild_id": 123, "channel_id": 456}
        """
        try:
            data = await request.json()
            
            text = data.get('text')
            guild_id = data.get('guild_id')
            channel_id = data.get('channel_id')
            
            if not text or not guild_id:
                return web.json_response(
                    {"error": "text und guild_id erforderlich"}, 
                    status=400
                )
                
            # Erstelle TTS Request
            tts_request = TTSRequest(
                text=text,
                guild_id=int(guild_id),
                channel_id=int(channel_id) if channel_id else None
            )
            
            # Füge zur Queue hinzu
            await self.bot.tts_queue.put(tts_request)
            
            return web.json_response({
                "status": "queued",
                "text": text[:100],
                "queue_position": self.bot.tts_queue.qsize(),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"API Fehler bei /speak: {e}")
            return web.json_response({"error": str(e)}, status=500)
            
    async def handle_join(self, request: web.Request) -> web.Response:
        """
        POST /join
        Body: {"guild_id": 123, "channel_id": 456}
        """
        try:
            data = await request.json()
            guild_id = int(data['guild_id'])
            channel_id = int(data['channel_id'])
            
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return web.json_response({"error": "Guild nicht gefunden"}, status=404)
                
            channel = guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                return web.json_response({"error": "Voice Channel nicht gefunden"}, status=404)
                
            # Verbinde
            voice_client = await channel.connect()
            self.bot._voice_connections[guild_id] = voice_client
            
            return web.json_response({
                "status": "connected",
                "guild": guild.name,
                "channel": channel.name
            })
            
        except Exception as e:
            logger.error(f"API Fehler bei /join: {e}")
            return web.json_response({"error": str(e)}, status=500)
            
    async def handle_leave(self, request: web.Request) -> web.Response:
        """
        POST /leave
        Body: {"guild_id": 123}
        """
        try:
            data = await request.json()
            guild_id = int(data['guild_id'])
            
            voice_client = self.bot._voice_connections.get(guild_id)
            if voice_client:
                await voice_client.disconnect()
                del self.bot._voice_connections[guild_id]
                
            return web.json_response({"status": "disconnected"})
            
        except Exception as e:
            logger.error(f"API Fehler bei /leave: {e}")
            return web.json_response({"error": str(e)}, status=500)
            
    async def handle_status(self, request: web.Request) -> web.Response:
        """
        GET /status
        """
        try:
            voice_status = {}
            for guild_id, vc in self.bot._voice_connections.items():
                guild = self.bot.get_guild(guild_id)
                voice_status[guild_id] = {
                    "guild_name": guild.name if guild else "Unknown",
                    "channel_name": vc.channel.name if vc.channel else "Unknown",
                    "is_connected": vc.is_connected(),
                    "is_playing": vc.is_playing()
                }
                
            return web.json_response({
                "bot_user": str(self.bot.user) if self.bot.user else "Not ready",
                "is_ready": self.bot.is_ready(),
                "is_speaking": self.bot.is_speaking,
                "queue_size": self.bot.tts_queue.qsize(),
                "voice_connections": voice_status,
                "dave_protocol": "active",
                "voice_config": {
                    "name": "Aoede",
                    "language": "de-DE"
                }
            })
            
        except Exception as e:
            logger.error(f"API Fehler bei /status: {e}")
            return web.json_response({"error": str(e)}, status=500)
            
    async def handle_health(self, request: web.Request) -> web.Response:
        """
        GET /health - Healthcheck
        """
        return web.json_response({
            "status": "healthy",
            "service": "truthseeker-voice",
            "timestamp": datetime.now().isoformat()
        })


async def trigger_tts_via_api(text: str, guild_id: int, channel_id: Optional[int] = None, api_url: str = "http://localhost:8742") -> dict:
    """
    Hilfsfunktion für OpenClaw/Kimi Claw um TTS zu triggern
    """
    async with aiohttp.ClientSession() as session:
        payload = {
            "text": text,
            "guild_id": guild_id,
            "channel_id": channel_id
        }
        
        async with session.post(f"{api_url}/speak", json=payload) as resp:
            return await resp.json()


# Beispiel-Nutzung für Integration
if __name__ == '__main__':
    # Test: API ist standalone nicht nutzbar, braucht laufenden Bot
    print("Dieses Modul wird von bot.py importiert")
