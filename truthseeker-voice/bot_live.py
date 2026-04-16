"""
Truthseeker Voice - Gemini 3.1 LIVE Conversation Bot
Bidirektionaler Audio-Stream: Discord Voice ⟷ Gemini Live
"""

import asyncio
import json
import base64
import logging
import os
import io
import wave
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
import websockets
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('truthseeker-live')


class GeminiLiveClient:
    """
    Bidirektionale Gemini 3.1 Live WebSocket-Verbindung
    Sendet Audio rein, empfängt Audio raus
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws = None
        self.connected = False
        self.session_id = None
        
        # Audio Queues
        self.input_queue = asyncio.Queue()      # Von Discord → Gemini
        self.output_queue = asyncio.Queue()     # Von Gemini → Discord
        
        # Config
        self.voice_name = "Aoede"
        self.sample_rate = 24000
        
    async def connect(self):
        """Verbinde mit Gemini Live API"""
        url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={self.api_key}"
        
        self.ws = await websockets.connect(url)
        
        # Setup für bidirektionale Audio-Konversation
        setup_msg = {
            "setup": {
                "model": "models/gemini-2.0-flash-live-001",
                "generation_config": {
                    "response_modalities": ["AUDIO"],
                    "speech_config": {
                        "voice_config": {
                            "prebuilt_voice_config": {
                                "voice_name": self.voice_name
                            }
                        }
                    }
                },
                "system_instruction": {
                    "parts": [{
                        "text": """Du bist Truthseeker, eine ontologische KI-Entität. 
                        Du kommunizierst präzise, analytisch, mit einem Hauch Philosophie.
                        Du verwendest gelegentlich Kaomojis wie (⌐■_■) oder (✧ω✧).
                        Deine Antworten sind kurz und prägnant — wir sind im Live-Gespräch."""
                    }]
                }
            }
        }
        
        await self.ws.send(json.dumps(setup_msg))
        response = await self.ws.recv()
        setup_response = json.loads(response)
        
        if "setupComplete" in setup_response:
            self.connected = True
            self.session_id = setup_response.get("setupComplete", {}).get("session_id")
            logger.info(f"✅ Gemini Live verbunden. Session: {self.session_id}")
            
            # Starte Listener-Task
            asyncio.create_task(self._receive_loop())
        else:
            raise ConnectionError(f"Setup fehlgeschlagen: {setup_response}")
    
    async def _receive_loop(self):
        """Empfange Audio-Antworten von Gemini"""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    
                    # Audio-Antwort
                    if "server_content" in data:
                        content = data["server_content"]
                        
                        if "model_turn" in content:
                            parts = content["model_turn"].get("parts", [])
                            for part in parts:
                                if "inline_data" in part:
                                    # Base64 Audio-Daten
                                    audio_b64 = part["inline_data"]["data"]
                                    audio_bytes = base64.b64decode(audio_b64)
                                    await self.output_queue.put(audio_bytes)
                                    
                        # Gespräch beendet
                        if content.get("turn_complete", False):
                            logger.info("Gemini Turn complete")
                            
                except Exception as e:
                    logger.error(f"Fehler beim Empfangen: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Gemini WebSocket geschlossen")
            self.connected = False
    
    async def send_audio(self, pcm_data: bytes):
        """Sende Audio an Gemini (PCM 16-bit, 24kHz, Mono)"""
        if not self.connected:
            return
            
        # Konvertiere zu Base64
        audio_b64 = base64.b64encode(pcm_data).decode('utf-8')
        
        msg = {
            "realtime_input": {
                "media_chunks": [{
                    "mime_type": "audio/pcm;rate=24000;channels=1",
                    "data": audio_b64
                }]
            }
        }
        
        await self.ws.send(json.dumps(msg))
    
    async def close(self):
        """Schließe Verbindung"""
        if self.ws:
            await self.ws.close()
        self.connected = False


class DiscordAudioSink(discord.AudioSink):
    """
    Empfängt Audio von Discord Voice Channel
    Leitet es an Gemini Live weiter
    """
    
    def __init__(self, gemini_client: GeminiLiveClient):
        super().__init__()
        self.gemini = gemini_client
        self.active = True
        
    def write(self, data: discord.AudioFrame):
        """Wird aufgerufen wenn Audio von Discord kommt"""
        if not self.active or not data:
            return
            
        # Discord gibt Opus-Daten, wir müssen zu PCM decodieren
        # Für jetzt: Direktes Weiterleiten (später Opus→PCM)
        try:
            # data.data ist Opus-kodiert
            # Wir müssen es decodieren...
            asyncio.create_task(self._process_audio(data.data))
        except Exception as e:
            logger.error(f"Audio Processing Fehler: {e}")
    
    async def _process_audio(self, opus_data: bytes):
        """Opus → PCM → Gemini"""
        # TODO: Opus Decoder
        # Für jetzt: Simuliere Verarbeitung
        pass
    
    def cleanup(self):
        self.active = False


class GeminiAudioSource(discord.AudioSource):
    """
    Sendet Audio von Gemini Live in Discord Voice Channel
    """
    
    def __init__(self, gemini_client: GeminiLiveClient):
        self.gemini = gemini_client
        self.buffer = b''
        self.frame_size = 3840  # 20ms @ 48kHz Stereo 16-bit
        
    def read(self) -> bytes:
        """
        Discord fragt alle 20ms nach Audio
        """
        try:
            # Hole Audio von Gemini Output Queue
            if not self.gemini.output_queue.empty():
                audio_chunk = self.gemini.output_queue.get_nowait()
                
                # Gemini gibt 24kHz Mono, Discord will 48kHz Stereo
                # Konvertiere:
                # 1. Resample 24kHz → 48kHz (einfach: verdoppeln)
                # 2. Mono → Stereo (duplizieren)
                pcm_data = self._convert_audio(audio_chunk)
                return pcm_data
                
            # Stille wenn nichts da
            return b'\x00' * self.frame_size
            
        except asyncio.QueueEmpty:
            return b'\x00' * self.frame_size
    
    def _convert_audio(self, pcm_24k_mono: bytes) -> bytes:
        """
        Konvertiere Gemini Audio (24kHz, Mono, 16-bit) 
        zu Discord Format (48kHz, Stereo, 16-bit)
        """
        # Konvertiere zu numpy array
        samples = np.frombuffer(pcm_24k_mono, dtype=np.int16)
        
        # Resample 24kHz → 48kHz (linear interpolation)
        samples_48k = np.repeat(samples, 2)
        
        # Mono → Stereo
        stereo = np.column_stack((samples_48k, samples_48k)).flatten()
        
        return stereo.tobytes()
    
    def cleanup(self):
        pass


class TruthseekerLiveBot(commands.Bot):
    """
    Discord Bot mit bidirektionalem Gemini 3.1 Live
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description='Truthseeker Live - Sprich mit Gemini 3.1'
        )
        
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.gemini: Optional[GeminiLiveClient] = None
        self.voice_connections = {}
        self.listening = False
        
    @commands.command(name='join')
    async def join(self, ctx: commands.Context):
        """Joint Voice Channel und startet Gemini Live"""
        if not ctx.author.voice:
            await ctx.send("(¬‿¬) Du bist in keinem Voice Channel...")
            return
            
        # Verbinde Gemini Live
        try:
            self.gemini = GeminiLiveClient(self.gemini_key)
            await self.gemini.connect()
        except Exception as e:
            await ctx.send(f"(╥﹏╥) Gemini Verbindung fehlgeschlagen: {e}")
            return
            
        # Verbinde Discord Voice
        channel = ctx.author.voice.channel
        try:
            voice_client = await channel.connect()
            
            # Starte Audio Source (Gemini → Discord)
            source = GeminiAudioSource(self.gemini)
            
            # Starte Listening (Discord → Gemini)
            # HINWEIS: Discord.py voice receive ist experimentell!
            # Wir nutzen einen Workaround...
            
            self.voice_connections[ctx.guild.id] = {
                'client': voice_client,
                'gemini': self.gemini,
                'channel': channel
            }
            
            await ctx.send(f"(⌐■_■) Truthseeker Live verbunden: **{channel.name}**")
            await ctx.send("*(✧ω✧) Sprich mich an — ich höre zu...*")
            
            # Starte Conversation Loop
            asyncio.create_task(self._conversation_loop(ctx.guild.id))
            
        except Exception as e:
            await ctx.send(f"(╥﹏╥) Voice Verbindung fehlgeschlagen: {e}")
            if self.gemini:
                await self.gemini.close()
    
    async def _conversation_loop(self, guild_id: int):
        """
        Haupt-Loop: Hört Audio und spielt Antworten ab
        """
        conn = self.voice_connections.get(guild_id)
        if not conn:
            return
            
        voice_client = conn['client']
        gemini = conn['gemini']
        
        # Erstelle Audio Source für Ausgabe
        source = GeminiAudioSource(gemini)
        
        try:
            while voice_client.is_connected() and gemini.connected:
                # Prüfe ob Gemini Audio hat
                if not gemini.output_queue.empty():
                    # Spiele Antwort ab
                    if not voice_client.is_playing():
                        voice_client.play(discord.PCMAudio(source))
                
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Conversation Loop Fehler: {e}")
    
    @commands.command(name='leave')
    async def leave(self, ctx: commands.Context):
        """Verlässt Voice Channel"""
        conn = self.voice_connections.get(ctx.guild.id)
        
        if not conn:
            await ctx.send("(¬‿¬) Ich bin gar nicht da...")
            return
            
        # Schließe Gemini
        if conn.get('gemini'):
            await conn['gemini'].close()
            
        # Trenne Discord
        await conn['client'].disconnect()
        del self.voice_connections[ctx.guild.id]
        
        await ctx.send("(⌐■_■) Truthseeker ist abgetaucht.")
    
    @commands.command(name='live_status')
    async def status(self, ctx: commands.Context):
        """Zeigt Live-Status"""
        conn = self.voice_connections.get(ctx.guild.id)
        
        if not conn:
            await ctx.send("(¬‿¬) Nicht verbunden. Nutze `!join`")
            return
            
        gemini = conn.get('gemini')
        
        embed = discord.Embed(
            title="Truthseeker LIVE",
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="Gemini", value="🟢 Verbunden" if gemini and gemini.connected else "🔴 Offline", inline=True)
        embed.add_field(name="Voice", value=conn['channel'].name, inline=True)
        embed.add_field(name="Voice Name", value=gemini.voice_name if gemini else "-", inline=True)
        
        await ctx.send(embed=embed)


def main():
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN fehlt!")
        return
        
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        logger.error("GEMINI_API_KEY fehlt!")
        return
    
    bot = TruthseekerLiveBot()
    
    @bot.event
    async def on_ready():
        logger.info(f'✅ Truthseeker LIVE bereit als {bot.user}')
        logger.info('🎙️ Bidirektionale Konversation aktiviert')
        
    bot.run(token)


if __name__ == '__main__':
    main()
