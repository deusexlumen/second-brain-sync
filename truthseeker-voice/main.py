"""
Truthseeker Voice - Integrated Bot mit API
Haupteinstiegspunkt
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

from bot import TruthseekerVoiceBot
from api_server import TruthseekerAPI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('truthseeker-main')


async def main():
    """Hauptfunktion - startet Bot und API"""
    load_dotenv()
    
    # Prüfe Environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN fehlt in .env!")
        return
        
    if not gemini_key:
        logger.error("❌ GEMINI_API_KEY fehlt in .env!")
        return
    
    # Erstelle Bot
    bot = TruthseekerVoiceBot()
    
    # Erstelle API Server
    api_host = os.getenv('API_HOST', 'localhost')
    api_port = int(os.getenv('API_PORT', '8742'))
    api = TruthseekerAPI(bot, host=api_host, port=api_port)
    
    # Event: Bot ist bereit
    @bot.event
    async def on_ready():
        logger.info(f'✅ Truthseeker Voice eingeloggt als {bot.user}')
        logger.info(f'🎤 Voice-Clients bereit')
        logger.info(f'🔊 DAVE Protocol: Aktiv')
        logger.info(f'🧠 Gemini 3.1 Live: Connected')
        
        # Starte API Server
        await api.start()
    
    # Starte Bot (blockiert)
    await bot.start(token)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Truthseeker Voice beendet")
    except Exception as e:
        logger.error(f"💥 Kritischer Fehler: {e}")
