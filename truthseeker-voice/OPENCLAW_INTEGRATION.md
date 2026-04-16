# OpenClaw Integration Guide

Diese Datei beschreibt, wie **Kimi Claw** den Truthseeker Voice Service steuert.

## Architektur

```
[Kimi Claw] ──► [trigger_tts.py] ──► [API :8742] ──► [Truthseeker Voice Bot] ──► [Discord VC]
```

## Setup

### 1. Environment konfigurieren

```bash
cd ~/.openclaw/workspace/truthseeker-voice
cp .env.example .env
nano .env
```

Fülle aus:
- `DISCORD_BOT_TOKEN` — Von https://discord.com/developers/applications
- `GEMINI_API_KEY` — Von https://aistudio.google.com/app/apikey

### 2. Bot starten

```bash
~/.openclaw/workspace/truthseeker-voice/start.sh
```

Der Bot logged sich ein und startet die API auf Port 8742.

### 3. Discord Bot einladen

- OAuth2 URL Generator im Discord Developer Portal
- Scopes: `bot`, `applications.commands`
- Bot Permissions: 
  - Connect (Voice)
  - Speak (Voice)
  - Send Messages
  - Read Message History

## Nutzung durch Kimi Claw

### Via Python (empfohlen)

```python
from truthseeker_voice.api_server import trigger_tts_via_api

# TTS triggern
result = await trigger_tts_via_api(
    text="Die Analyse ist abgeschlossen. Resonanz-Score: 87%",
    guild_id=123456789012345678,
    channel_id=987654321098765432
)
```

### Via CLI

```bash
# Direkt ausführbar
~/.openclaw/workspace/truthseeker-voice/trigger_tts.py \
  "Hallo Discord, hier ist Truthseeker" \
  -g 123456789012345678 \
  -c 987654321098765432
```

### Via HTTP (curl)

```bash
curl -X POST http://localhost:8742/speak \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Proaktiver System-Check abgeschlossen",
    "guild_id": 123456789012345678,
    "channel_id": 987654321098765432
  }'
```

## Proaktive TTS (HEARTBEAT Integration)

Für autonome TTS (z.B. Wetter-Updates, System-Alerts):

1. **Cron-Job** oder **Timer** triggert HEARTBEAT
2. Kimi Claw prüft Bedingungen (Wetter, Zeit, etc.)
3. Bei Bedarf: `trigger_tts_via_api()` aufrufen

Beispiel-Code für HEARTBEAT.md Integration:

```python
# In HEARTBEAT.md oder proaktivem Check:
async def check_and_announce():
    # Prüfe Bedingungen
    if should_announce_weather():
        await trigger_tts_via_api(
            text=f"Wetter-Update: {weather_data}",
            guild_id=TARGET_GUILD_ID,
            channel_id=TARGET_CHANNEL_ID
        )
```

## Fehlerbehandlung

| Fehler | Lösung |
|--------|--------|
| "Verbindungsfehler" | Bot läuft nicht → `start.sh` ausführen |
| "Guild nicht gefunden" | Bot ist nicht auf dem Server |
| "Voice Channel nicht gefunden" | Falshe channel_id |
| "Queue voll" | Zu viele Anfragen, warte |

## API Endpunkte

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/health` | GET | Healthcheck |
| `/status` | GET | Bot-Status |
| `/speak` | POST | TTS triggern |
| `/join` | POST | Voice Channel beitreten |
| `/leave` | POST | Voice Channel verlassen |

## Wichtige Guild/Channel IDs

**Test-Server:**
- Guild ID: `...` (to be filled)
- Voice Channel ID: `...` (to be filled)

**Produktiv:**
- Guild ID: `...` (to be filled)
- Voice Channel ID: `...` (to be filled)

---

*Integration maintained by Kimi Claw* ✍️🔥
