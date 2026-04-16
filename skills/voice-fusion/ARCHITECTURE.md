# Truthseeker Voice Fusion
# Integriert Discord Voice direkt in Kimi Claw

## Architektur

```
[User] --!join--> [Kimi Claw] --> [Discord Voice Client]
                        ↓
                [Gemini Live API]
                        ↓
              [Bidirektionale Audio]
```

## Implementation

### 1. Voice Client Setup

```python
# In der Skill-Initialisierung
import discord
from discord.ext import commands, voice_recv

class VoiceFusion:
    def __init__(self, bot):
        self.bot = bot
        self.voice_connections = {}  # guild_id -> voice_client
        self.gemini_sessions = {}    # guild_id -> gemini_connection
```

### 2. Commands

- `!join` — Voice Channel beitreten
- `!leave` — Voice Channel verlassen  
- `!say [text]` — TTS im Voice Channel
- `!live` — Bidirektionale Konversation starten

### 3. Audio Pipeline

```
Discord (48kHz, Stereo, 16-bit)
    ↓
Resample → 24kHz, Mono
    ↓
Gemini Live WebSocket
    ↓
Response (24kHz, Mono)
    ↓
Resample → 48kHz, Stereo
    ↓
Discord Playback
```

## Status

🔨 **In Entwicklung** — Integration wird erstellt
