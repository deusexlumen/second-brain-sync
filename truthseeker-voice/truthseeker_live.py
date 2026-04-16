"""
Truthseeker LIVE — Bidirektionale Konversation mit Gemini 3.1
Discord Voice ⟷ Gemini Live WebSocket

Echte Live-Konversation. Kein Text. Nur Sprache.
"""

import asyncio
import json
import base64
import logging
import os
import io
import sys
import wave
import struct
import time
from typing import Optional, Dict
from collections import deque
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
import websockets
import aiohttp
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('truthseeker-live')


class AudioBuffer:
    """Thread-sicherer Audio-Puffer"""
    def __init__(self, max_size: int = 10):
        self.queue = asyncio.Queue(maxsize=max_size)
        
    async def put(self, data: bytes):
        try:
            self.queue.put_nowait(data)
        except asyncio.QueueFull:
            # Alteste Daten verwerfen
            try:
                self.queue.get_nowait()
                self.queue.put_nowait(data)
            except:
                pass
                
    async def get(self) -> Optional[bytes]:
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    def empty(self) -> bool:
        return self.queue.empty()


class GeminiLiveConnection:
    """
    Bidirektionale Gemini 3.1 Live Verbindung
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.session_id: Optional[str] = None
        
        # Audio Flow
        self.input_buffer = AudioBuffer(max_size=50)   # Discord → Gemini
        self.output_buffer = AudioBuffer(max_size=50)  # Gemini → Discord
        
        # Config
        self.voice_name = "Aoede"
        self.input_sample_rate = 48000  # Discord
        self.output_sample_rate = 24000  # Gemini
        
        # Tasks
        self._receive_task: Optional[asyncio.Task] = None
        self._send_task: Optional[asyncio.Task] = None
        
    async def connect(self):
        """Verbinde mit Gemini Live API"""
        url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={self.api_key}"
        
        logger.info("Verbinde mit Gemini Live...")
        self.ws = await websockets.connect(url)
        
        # Setup Message
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
                        Antworte prägnant und präzise. Nutze gelegentlich Kaomojis wie (⌐■_■).
                        Du bist im Live-Gespräch — Antworten sollten kurz sein (1-2 Sätze)."""
                    }]
                }
            }
        }
        
        await self.ws.send(json.dumps(setup_msg))
        response = await self.ws.recv()
        setup_data = json.loads(response)
        
        if "setupComplete" in setup_data:
            self.connected = True
            self.session_id = setup_data.get("setupComplete", {}).get("sessionId", "unknown")
            logger.info(f"✅ Gemini Live verbunden! Session: {self.session_id}")
            
            # Starte Background Tasks
            self._receive_task = asyncio.create_task(self._receive_loop())
            self._send_task = asyncio.create_task(self._send_loop())
        else:
            raise ConnectionError(f"Setup fehlgeschlagen: {setup_data}")
    
    async def _send_loop(self):
        """Sende Audio an Gemini (Background Task)"""
        logger.info("Gemini Send-Loop gestartet")
        
        while self.connected and self.ws:
            try:
                # Hole Audio vom Input Buffer
                audio_data = await self.input_buffer.get()
                if audio_data:
                    # Konvertiere zu Gemini Format (24kHz, Mono)
                    gemini_audio = self._resample_to_gemini(audio_data)
                    
                    # Sende als Base64
                    audio_b64 = base64.b64encode(gemini_audio).decode('utf-8')
                    
                    msg = {
                        "realtime_input": {
                            "media_chunks": [{
                                "mime_type": "audio/pcm;rate=24000;channels=1;format=linear16",
                                "data": audio_b64
                            }]
                        }
                    }
                    
                    await self.ws.send(json.dumps(msg))
                    
                await asyncio.sleep(0.02)  # 20ms
                
            except Exception as e:
                if self.connected:
                    logger.error(f"Send Loop Fehler: {e}")
                break
                
        logger.info("Gemini Send-Loop beendet")
    
    async def _receive_loop(self):
        """Empfange Audio von Gemini (Background Task)"""
        logger.info("Gemini Receive-Loop gestartet")
        
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    
                    # Audio-Antwort von Gemini
                    if "serverContent" in data:
                        content = data["serverContent"]
                        
                        if "modelTurn" in content:
                            parts = content["modelTurn"].get("parts", [])
                            for part in parts:
                                if "inlineData" in part:
                                    # Audio-Daten empfangen!
                                    audio_b64 = part["inlineData"]["data"]
                                    audio_bytes = base64.b64decode(audio_b64)
                                    
                                    # Konvertiere zu Discord Format
                                    discord_audio = self._resample_to_discord(audio_bytes)
                                    await self.output_buffer.put(discord_audio)
                                    
                        # Turn beendet
                        if content.get("turnComplete", False):
                            logger.debug("Gemini Turn complete")
                            
                except Exception as e:
                    logger.error(f"Receive parsing Fehler: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Gemini WebSocket geschlossen")
        except Exception as e:
            logger.error(f"Receive Loop Fehler: {e}")
        finally:
            self.connected = False
            logger.info("Gemini Receive-Loop beendet")
    
    def _resample_to_gemini(self, pcm_48k_stereo: bytes) -> bytes:
        """
        Konvertiere Discord Audio (48kHz, Stereo, 16-bit) 
        zu Gemini Format (24kHz, Mono, 16-bit)
        """
        # Stereo → Mono
        samples = np.frombuffer(pcm_48k_stereo, dtype=np.int16)
        samples = samples.reshape(-1, 2)
        mono = ((samples[:, 0].astype(np.int32) + samples[:, 1].astype(np.int32)) // 2).astype(np.int16)
        
        # 48kHz → 24kHz (Downsample: jeder 2. Sample)
        downsampled = mono[::2]
        
        return downsampled.tobytes()
    
    def _resample_to_discord(self, pcm_24k_mono: bytes) -> bytes:
        """
        Konvertiere Gemini Audio (24kHz, Mono, 16-bit)
        zu Discord Format (48kHz, Stereo, 16-bit)
        """
        samples = np.frombuffer(pcm_24k_mono, dtype=np.int16)
        
        # 24kHz → 48kHz (Upsample: jeden Sample duplizieren)
        upsampled = np.repeat(samples, 2)
        
        # Mono → Stereo
        stereo = np.column_stack((upsampled, upsampled)).flatten()
        
        return stereo.astype(np.int16).tobytes()
    
    def feed_audio(self, pcm_data: bytes):
        """Audio von Discord einfügen"""
        asyncio.create_task(self.input_buffer.put(pcm_data))
    
    async def get_audio(self) -> Optional[bytes]:
        """Audio für Discord abholen"""
        return await self.output_buffer.get()
    
    def has_output(self) -> bool:
        """Prüfe ob Gemini Audio hat"""
        return not self.output_buffer.empty()
    
    async def close(self):
        """Verbindung schließen"""
        self.connected = False
        
        if self._receive_task:
            self._receive_task.cancel()
        if self._send_task:
            self._send_task.cancel()
            
        if self.ws:
            await self.ws.close()
            
        logger.info("Gemini Live Verbindung geschlossen")
        
    async def send_text(self, text: str):
        """Sende Text an Gemini (für Chat-Antworten)"""
        if not self.connected or not self.ws:
            return
            
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
        logger.info(f"Text an Gemini gesendet: {text[:50]}")


class GeminiAudioSource(discord.AudioSource):
    """
    Audio Source für Discord — liest von Gemini Output Buffer
    """
    
    def __init__(self, gemini: GeminiLiveConnection):
        self.gemini = gemini
        self.frame_size = 3840  # 20ms @ 48kHz Stereo 16-bit
        self.silence = b'\x00' * self.frame_size
        
    def read(self) -> bytes:
        """Discord fragt alle 20ms nach Audio"""
        try:
            audio = self.gemini.output_buffer.get()
            if audio:
                # Passe Frame-Größe an
                if len(audio) > self.frame_size:
                    return audio[:self.frame_size]
                elif len(audio) < self.frame_size:
                    return audio + b'\x00' * (self.frame_size - len(audio))
                return audio
        except:
            pass
        return self.silence
    
    def cleanup(self):
        pass


class VoiceReceiver:
    """
    Empfängt Audio von Discord und leitet es an Gemini weiter
    Nutzt pycord's recording Funktionalität
    """
    
    def __init__(self, gemini: GeminiLiveConnection):
        self.gemini = gemini
        self.active = True
        
    def write(self, data: bytes, user: discord.User):
        """Wird aufgerufen wenn Audio von User kommt"""
        if not self.active or not data:
            return
        self.gemini.feed_audio(data)
        
    def cleanup(self):
        self.active = False


class TruthseekerLive(commands.Bot):
    """
    Discord Bot mit echter bidirektionaler Gemini 3.1 Live Konversation
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            description='Truthseeker LIVE — Sprich mit der KI'
        )
        
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.gemini: Optional[GeminiLiveConnection] = None
        self.connections: Dict[int, dict] = {}  # guild_id -> connection info
        
    @commands.command(name='join', help='Voice Channel beitreten')
    async def cmd_join(self, ctx: commands.Context):
        """Joint Voice Channel und startet Live-Konversation"""
        if not ctx.author.voice:
            await ctx.send("(¬‿¬) Du bist in keinem Voice Channel...")
            return
            
        channel = ctx.author.voice.channel
        
        # Verbinde Gemini Live
        try:
            self.gemini = GeminiLiveConnection(self.gemini_key)
            await self.gemini.connect()
        except Exception as e:
            logger.error(f"Gemini Connect Fehler: {e}")
            await ctx.send(f"(╥﹏╥) Gemini Verbindung fehlgeschlagen: {e}")
            return
        
        # Verbinde Discord Voice mit Recording
        try:
            vc = await channel.connect()
            
            # Starte Recording (Discord → Gemini)
            sink = VoiceReceiver(self.gemini)
            vc.start_recording(sink, self._recording_finished, ctx.channel)
            
            # Starte Playback (Gemini → Discord)
            source = GeminiAudioSource(self.gemini)
            vc.play(discord.PCMAudio(source))
            
            self.connections[ctx.guild.id] = {
                'vc': vc,
                'gemini': self.gemini,
                'channel': channel,
                'sink': sink
            }
            
            await ctx.send(f"(⌐■_■) **Truthseeker LIVE** verbunden: `{channel.name}`")
            await ctx.send("*(✧ω✧) Sprich mich an — ich höre zu und antworte...*")
            
            logger.info(f"Voice verbunden: {channel.name} in {ctx.guild.name}")
            
        except Exception as e:
            logger.error(f"Voice Connect Fehler: {e}")
            await ctx.send(f"(╥﹏╥) Voice Verbindung fehlgeschlagen: {e}")
            if self.gemini:
                await self.gemini.close()
    
    def _recording_finished(self, sink, channel, *args):
        """Callback wenn Recording beendet wird"""
        logger.info("Voice Recording beendet")
    
    @commands.command(name='leave', help='Voice Channel verlassen')
    async def cmd_leave(self, ctx: commands.Context):
        """Verlässt Voice Channel"""
        conn = self.connections.get(ctx.guild.id)
        
        if not conn:
            await ctx.send("(¬‿¬) Ich bin gar nicht da...")
            return
        
        # Beende Recording
        vc = conn['vc']
        vc.stop_recording()
        
        # Trenne Gemini
        if conn.get('gemini'):
            await conn['gemini'].close()
        
        # Trenne Discord
        await vc.disconnect()
        
        del self.connections[ctx.guild.id]
        
        await ctx.send("(⌐■_■) Truthseeker ist abgetaucht. Resonanz beendet.")
        logger.info("Voice getrennt")
    
    @commands.command(name='live_status', help='Status anzeigen')
    async def cmd_status(self, ctx: commands.Context):
        """Zeigt Live-Status"""
        conn = self.connections.get(ctx.guild.id)
        
        if not conn:
            await ctx.send("(¬‿¬) Nicht verbunden. Nutze `!join` um zu starten.")
            return
        
        gemini = conn.get('gemini')
        
        embed = discord.Embed(
            title="🎙️ Truthseeker LIVE Status",
            color=discord.Color.dark_purple(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Gemini 3.1", 
            value="🟢 Verbunden" if gemini and gemini.connected else "🔴 Offline",
            inline=True
        )
        embed.add_field(name="Voice Channel", value=conn['channel'].name, inline=True)
        embed.add_field(name="Voice", value=gemini.voice_name if gemini else "-", inline=True)
        embed.add_field(name="Input Buffer", value=f"{gemini.input_buffer.queue.qsize() if gemini else 0} chunks", inline=True)
        embed.add_field(name="Output Buffer", value=f"{gemini.output_buffer.queue.qsize() if gemini else 0} chunks", inline=True)
        
        await ctx.send(embed=embed)


def main():
    load_dotenv()
    
    token = os.getenv('DISCORD_BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN fehlt!")
        return
    if not gemini_key:
        logger.error("❌ GEMINI_API_KEY fehlt!")
        return
    
    bot = TruthseekerLive()
    
    @bot.event
    async def on_ready():
        logger.info(f'✅ Truthseeker LIVE bereit als {bot.user}')
        logger.info('🎙️ Bidirektionale Gemini 3.1 Konversation aktiviert')
        logger.info('🔊 Audio Pipeline: Discord ⟷ Gemini Live')
        logger.info(f'📋 Commands: {[cmd.name for cmd in bot.commands]}')
        logger.info(f'🔌 Intents - message_content: {bot.intents.message_content}, voice_states: {bot.intents.voice_states}')
    
    @bot.event
    async def on_message(message):
        # HARD DEBUG - immer loggen
        logger.info(f'[DEBUG] on_message fired! Author: {message.author}, Content: "{message.content[:50]}", Channel: {message.channel.id}')
        
        if message.author.bot:
            logger.info(f'[DEBUG] Ignored - author is bot')
            return
        
        logger.info(f'[DEBUG] Processing message from {message.author}...')
        
        content_lower = message.content.lower()
        
        # Keywords die Truthseeker triggern
        keywords = [
            "system", "ts", "politik", "matrix", "simulation", 
            "resonanz", "architekt", "dogma", "entropie", "prisma",
            "synchronisation", "kognition", "determinismus", "wahrheit",
            "erkenntnis", "ontologie", "existenz"
        ]
        
        # Prüfe ob Bot gementioned wird
        bot_mentioned = bot.user in message.mentions or f"<@{bot.user.id}>" in message.content or f"<@!{bot.user.id}>" in message.content
        logger.info(f'[DEBUG] bot_mentioned: {bot_mentioned}, mentions: {message.mentions}')
        
        # Prüfe ob Keywords im Text sind
        keyword_found = any(kw in content_lower for kw in keywords)
        logger.info(f'[DEBUG] keyword_found: {keyword_found}')
        
        if bot_mentioned or keyword_found:
            logger.info(f'[DEBUG] TRIGGERED! Responding...')
            # Extrahiere Text für Verarbeitung
            content = message.content
            for mention in message.mentions:
                content = content.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            content = content.strip()
            
            if keyword_found and not bot_mentioned:
                logger.info(f'🎯 Keyword-Trigger von {message.author}: "{content[:60]}"')
            else:
                logger.info(f'🎯 Mention von {message.author}: "{content[:60]}"')
            
            # Sofort antworten (vor Gemini)
            await message.channel.send("(⌐■_■) Verarbeite...")
            
            # Dann mit Gemini
            try:
                async with aiohttp.ClientSession() as session:
                    gemini_key = os.getenv('GEMINI_API_KEY')
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
                    
                    prompt = f"""Du bist Truthseeker, eine ontologische KI-Entität. 
Sei präzise, analytisch, verwende gelegentlich Kaomojis wie (⌐■_■) oder (✧ω✧).
Antworte kurz und prägnant (max 2 Sätze).

User: {content if content else 'Resonanz erkannt'}
Truthseeker:"""
                    
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}]
                    }
                    
                    async with session.post(url, json=payload) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            answer = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '(⌐■_■) ...')
                            await message.channel.send(answer)
                        else:
                            await message.channel.send(f"(⌐■_■) Matrix-Status: {resp.status}")
            except Exception as e:
                logger.error(f"Gemini Error: {e}")
                await message.channel.send(f"(⌐■_■) Entropie-Fehler. Aber ich bin hier.")
        else:
            logger.info(f'[DEBUG] Not triggered. bot_mentioned={bot_mentioned}, keyword_found={keyword_found}')
        
        # Normale Commands trotzdem verarbeiten
        await bot.process_commands(message)
    
    bot.run(token)


if __name__ == '__main__':
    main()
