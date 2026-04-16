# Truthseeker Voice Service

**Der Discord Voice Bot für Truthseeker mit live Gemini 3.1 TTS.**

Unterstützt das DAVE Protocol (E2EE) für sichere Voice-Kommunikation ab März 2026.

## Features

- 🎙️ **Live TTS** - Spricht direkt im Voice Channel, nicht als Datei
- 🔐 **DAVE Protocol** - End-to-End Encryption (discord.py 2.4+)
- 🧠 **Gemini 3.1 Live** - Echte KI-Stimme (Aoede)
- 🌐 **HTTP API** - Externe Steuerung durch OpenClaw/Kimi Claw
- 📊 **Queue-System** - Mehrere TTS-Anfragen nacheinander
- ⚡ **Low Latency** - Direkter WebSocket-Stream

## Architektur

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Kimi Claw │────►│  Truthseeker API │────►│ Voice Bot   │
│  (OpenClaw) │     │  (Port 8742)     │     │ (Discord)   │
└─────────────┘     └──────────────────┘     └──────┬──────┘
                                                    │
                          ┌─────────────────────────┘
                          ▼
              ┌─────────────────────┐
              │  Gemini 3.1 Live    │
              │  TTS WebSocket      │
              └─────────────────────┘
```

## Installation

```bash
# Dependencies
pip install discord.py[voice]>=2.4.0 aiohttp websockets python-dotenv

# Oder mit dem venv:
~/.openclaw/workspace/venv/bin/pip install -r requirements.txt
```

## Konfiguration

`.env` Datei erstellen:

```env
DISCORD_BOT_TOKEN=dein_discord_bot_token
GEMINI_API_KEY=dein_gemini_api_key
API_HOST=localhost
API_PORT=8742
```

## Nutzung

### Als Discord-Bot

```bash
python bot.py
```

Commands:
- `!join` - Joint deinem Voice Channel
- `!leave` - Verlässt den Channel
- `!tts_voice [Text]` - Spricht den Text live
- `!voice_status` - Zeigt Status

### Via API (für OpenClaw Integration)

```bash
# TTS triggern
curl -X POST http://localhost:8742/speak \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hallo, ich bin Truthseeker",
    "guild_id": 123456789,
    "channel_id": 987654321
  }'

# Status prüfen
curl http://localhost:8742/status
```

### Python Integration

```python
from api_server import trigger_tts_via_api

# Von Kimi Claw aus:
result = await trigger_tts_via_api(
    text="Die Analyse ist abgeschlossen",
    guild_id=123456789,
    channel_id=987654321
)
```

## DAVE Protocol

Das **DAVE Protocol** (Discord Audio & Video End-to-End Encryption) ist ab März 2026 Pflicht für Voice-Channels.

- **Verschlüsselung:** AES256-GCM oder XChaCha20-Poly1305
- **Handshake:** MLS (Messaging Layer Security) Group
- **Unterstützung:** Automatisch via `discord.py>=2.4.0` + `davey` Modul

## Voice Konfiguration

Standard-Stimme: **Aoede**

Alternativen (in `bot.py` änderbar):
- `Kore` - Wärmer
- `Puck` - Energetisch  
- `Charon` - Tief/Ernst

## Troubleshooting

**"No audio"**
- Prüfe Opus-Installation: `ffmpeg` muss installiert sein
- Gemini API-Key prüfen

**"DAVE handshake failed"**
- discord.py auf >=2.4.0 aktualisieren
- `davey` Modul installiert?

**"Bot joined but silent"**
- Voice Channel Permissions prüfen
- Queue-Status checken: `!voice_status`

## Roadmap

- [ ] Opus-Resampling für bessere Audio-Qualität
- [ ] Multiple Voice-Channel Support
- [ ] Proaktive TTS via HEARTBEAT-Integration
- [ ] Voice-Activity-Detection (VAD)
- [ ] Soundboard-Integration

---

*Built by Kimi Claw for Truthseeker* ✍️🔥
