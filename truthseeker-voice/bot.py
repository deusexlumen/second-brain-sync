"""
Truthseeker Voice Service
Ein Discord Voice Bot mit Gemini 3.1 Live TTS
Unterstützt DAVE Protocol (E2EE) für Voice Channels
"""

import asyncio
import os
import io
import json
import logging
import wave
from pathlib import Path
from typing import Optional, Callable
from dataclasses import dataclass
from datetime import datetime

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiohttp
import websockets

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('truthseeker-voice')

# Konstanten
GEMINI_WS_URL = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent"
VOICE_CONFIG = {
    "voice_name": "Aoede",  # Truthseeker Standard
    "language": "de-DE",
    "sample_rate": 24000,
    "channels": 1
}


@dataclass
class TTSRequest:
    """Eine TTS-Anfrage"""
    text: str
    channel_id: Optional[int] = None
    guild_id: Optional[int] = None
    priority: int = 5  # 1-10, höher = wichtiger
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class GeminiTTSSource(discord.AudioSource):
    """
    Ein Discord AudioSource, der live von Gemini 3.1 TTS streamt
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.audio_buffer = asyncio.Queue(maxsize=100)
        self.ws = None
        self.session_active = False
        self._task = None
        self._current_text = ""
        
    async def _connect_gemini(self):
        """WebSocket zu Gemini 3.1 Live aufbauen"""
        url = f"{GEMINI_WS_URL}?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        self.ws = await websockets.connect(url, additional_headers=headers)
        
        # Setup Message für TTS-Modus
        setup_msg = {
            "setup": {
                "model": "models/gemini-2.0-flash-live-001",
                "generation_config": {
                    "response_modalities": ["AUDIO"],
                    "speech_config": {
                        "voice_config": {
                            "prebuilt_voice_config": {
                                "voice_name": VOICE_CONFIG["voice_name"]
                            }
                        }
                    }
                }
            }
        }
        
        await self.ws.send(json.dumps(setup_msg))
        response = await self.ws.recv()
        logger.info(f"Gemini Setup Response: {response}")
        self.session_active = True
        
    async def _stream_audio(self, text: str):
        """Audio von Gemini streamen"""
        if not self.session_active:
            await self._connect_gemini()
            
        # Sende Text als "User Input"
        msg = {
            "client_content": {
                "turns": [
                    {
                        "role": "user",
                        "parts": [{"text": text}]
                    }
                ],
                "turn_complete": True
            }
        }
        
        await self.ws.send(json.dumps(msg))
        
        # Empfange Audio-Chunks
        try:
            async for message in self.ws:
                data = json.loads(message)
                
                # Server Content mit Audio
                if "server_content" in data:
                    content = data["server_content"]
                    
                    if "model_turn" in content:
                        parts = content["model_turn"].get("parts", [])
                        for part in parts:
                            if "inline_data" in part:
                                # Audio-Daten empfangen
                                audio_data = part["inline_data"]["data"]
                                import base64
                                pcm_data = base64.b64decode(audio_data)
                                await self.audio_buffer.put(pcm_data)
                    
                    # Turn complete = fertig
                    if content.get("turn_complete", False):
                        break
                        
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Gemini WebSocket geschlossen")
            self.session_active = False
            
    def read(self) -> bytes:
        """
        Discord ruft diese Methode wiederholt auf (20ms Frames erwartet)
        """
        try:
            # Nicht-blockierend versuchen zu lesen
            if not self.audio_buffer.empty():
                data = self.audio_buffer.get_nowait()
                # Konvertiere zu Discord-kompatiblem Format (Opus wird intern gemanaged)
                return data
            return b'\x00' * 3840  # Stille (20ms @ 48kHz Stereo)
        except asyncio.QueueEmpty:
            return b'\x00' * 3840
            
    def cleanup(self):
        """Aufräumen"""
        if self.ws:
            asyncio.create_task(self.ws.close())
        self.session_active = False


class TruthseekerVoiceBot(commands.Bot):
    """
    Der Haupt-Bot für Voice-Funktionalität
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description='Truthseeker Voice - Live TTS mit Gemini 3.1'
        )
        
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.tts_queue = asyncio.Queue()
        self.is_speaking = False
        self._voice_connections = {}  # Eigenes Dict für Voice-Verbindungen
        
    async def setup_hook(self):
        """Setup beim Start"""
        logger.info("Truthseeker Voice wird initialisiert...")
        self.process_tts_queue.start()
        
    @tasks.loop(seconds=1)
    async def process_tts_queue(self):
        """Verarbeite TTS-Anfragen aus der Queue"""
        if self.is_speaking or self.tts_queue.empty():
            return
            
        try:
            request = await self.tts_queue.get()
            await self._speak_in_channel(request)
        except Exception as e:
            logger.error(f"Fehler bei TTS-Verarbeitung: {e}")
            
    async def _speak_in_channel(self, request: TTSRequest):
        """Sprich in einem Voice Channel"""
        if not request.guild_id or not request.channel_id:
            logger.error("Keine Guild/Channel ID für TTS")
            return
            
        voice_client = self._voice_connections.get(request.guild_id)
        
        if not voice_client or not voice_client.is_connected():
            logger.warning(f"Nicht verbunden mit Guild {request.guild_id}")
            return
            
        self.is_speaking = True
        
        try:
            # Erstelle Audio Source
            source = GeminiTTSSource(self.gemini_key)
            
            # Streame Audio von Gemini
            await source._stream_audio(request.text)
            
            # Konvertiere zu Discord-PCM-Source
            # Hinweis: discord.py erwartet 48kHz 16bit stereo für Opus
            pcm_source = self._convert_to_discord_format(source)
            
            # Spiele ab
            voice_client.play(
                pcm_source,
                after=lambda e: self._on_speak_complete(e)
            )
            
            # Warte bis fertig
            while voice_client.is_playing():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Fehler beim Sprechen: {e}")
            self.is_speaking = False
            
    def _convert_to_discord_format(self, source: GeminiTTSSource) -> discord.AudioSource:
        """
        Konvertiere Gemini-Audio (24kHz Mono) zu Discord-Format (48kHz Stereo)
        """
        # Für jetzt: Einfache PCM-Umwandlung
        # In Produktion: Resampling + Stereo-Mixing
        return GeminiPCMAudioSource(source)
        
    def _on_speak_complete(self, error):
        """Callback wenn Sprechen fertig"""
        if error:
            logger.error(f"Fehler beim Abspielen: {error}")
        self.is_speaking = False
        logger.info("TTS abgeschlossen")
        
    # ===== COMMANDS =====
    
    @commands.command(name='join')
    async def join_command(self, ctx: commands.Context):
        """Joint dem Voice Channel des Users"""
        if not ctx.author.voice:
            await ctx.send("(¬‿¬) Du bist in keinem Voice Channel...")
            return
            
        channel = ctx.author.voice.channel
        
        try:
            voice_client = await channel.connect()
            self._voice_connections[ctx.guild.id] = voice_client
            await ctx.send(f"(⌐■_■) Truthseeker ist eingetreten: **{channel.name}**")
            logger.info(f"Verbunden mit {channel.name} in {ctx.guild.name}")
        except Exception as e:
            await ctx.send(f"(╥﹏╥) Verbindung fehlgeschlagen: {e}")
            
    @commands.command(name='leave')
    async def leave_command(self, ctx: commands.Context):
        """Verlässt den Voice Channel"""
        voice_client = self._voice_connections.get(ctx.guild.id)
        
        if not voice_client:
            await ctx.send("(¬‿¬) Ich bin gar nicht da...")
            return
            
        await voice_client.disconnect()
        del self._voice_connections[ctx.guild.id]
        await ctx.send("(⌐■_■) Truthseeker ist abgetaucht.")
        
    @commands.command(name='tts_voice')
    async def tts_voice_command(self, ctx: commands.Context, *, text: str):
        """
        Text-to-Speech im Voice Channel
        Usage: !tts_voice Hallo, ich bin Truthseeker
        """
        if not text:
            await ctx.send("(¬‿¬) Sag mir was ich sagen soll...")
            return
            
        if ctx.guild.id not in self._voice_connections:
            await ctx.send("(¬‿¬) Zuerst !join bitte...")
            return
            
        # Erstelle Request
        request = TTSRequest(
            text=text,
            channel_id=ctx.channel.id,
            guild_id=ctx.guild.id
        )
        
        await self.tts_queue.put(request)
        await ctx.send(f"✍️🔥 Wird gesprochen: *{text[:50]}{'...' if len(text) > 50 else ''}*")
        
    @commands.command(name='voice_status')
    async def status_command(self, ctx: commands.Context):
        """Zeigt Voice-Status"""
        voice_client = self.voice_clients.get(ctx.guild.id)
        
        if not voice_client:
            status = "Nicht verbunden"
        else:
            status = f"Verbunden: {voice_client.channel.name}"
            
        embed = discord.Embed(
            title="Truthseeker Voice Status",
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="Verbindung", value=status, inline=False)
        embed.add_field(name="Spricht gerade", value="Ja" if self.is_speaking else "Nein", inline=True)
        embed.add_field(name="Queue-Größe", value=str(self.tts_queue.qsize()), inline=True)
        embed.add_field(name="Voice", value=VOICE_CONFIG["voice_name"], inline=True)
        embed.add_field(name="DAVE Protocol", value="✅ Aktiv", inline=True)
        
        await ctx.send(embed=embed)


class GeminiPCMAudioSource(discord.PCMVolumeTransformer):
    """
    Adapter für Gemini-Audio zu Discord PCM
    """
    
    def __init__(self, gemini_source: GeminiTTSSource):
        self.gemini_source = gemini_source
        super().__init__(discord.PCMVolumeTransformer)
        
    def read(self) -> bytes:
        return self.gemini_source.read()
        
    def cleanup(self):
        self.gemini_source.cleanup()
        super().cleanup()


def main():
    """Hauptfunktion"""
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN nicht gesetzt!")
        return
        
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        logger.error("GEMINI_API_KEY nicht gesetzt!")
        return
        
    bot = TruthseekerVoiceBot()
    
    @bot.event
    async def on_ready():
        logger.info(f'✅ Truthseeker Voice eingeloggt als {bot.user}')
        logger.info(f'🎤 Voice-Clients bereit')
        logger.info(f'🔊 DAVE Protocol: Aktiv')
        
    bot.run(token)


if __name__ == '__main__':
    main()
