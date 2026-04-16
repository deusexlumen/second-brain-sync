# Mission Control - Multi-Agent Discord System

## Overview

Mission Control ist ein Multi-Agent Discord System basierend auf OpenClaw und inspiriert vom Video "Vibe with AI".

## Architektur

```
┌─────────────────────────────────────────────────────────┐
│                    MOTHER SHIP                          │
│                  (Discord Server)                       │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐                                            │
│  │  Henry   │ ◄── Chief of Staff (Main Interface)        │
│  └────┬─────┘                                            │
│       │                                                  │
│       ├───► Nexus (CTO) ─────► #engineering              │
│       ├───► Ivy (Researcher) ─► #research                │
│       ├───► Knox (Security) ──► #security                │
│       └───► Mr. X (Content) ──► #content                 │
│                                                          │
│  Shared Channels:                                        │
│  - #status (Heartbeat / Status Updates)                  │
│  - #command-center (User <-> Henry)                      │
│  - #general                                              │
└─────────────────────────────────────────────────────────┘
```

## Features

### 1. Heartbeat System
- Jeder Agent postet alle 30 Minuten Status in #status
- Zeigt aktive Tasks, Status, und letzte Aktivität

### 2. Shared Memory
- Integration mit `~/self-improving/`
- Jeder Agent kann auf globales Memory zugreifen
- Agent-spezifische Memories in `~/self-improving/projects/agents/`

### 3. Commands
| Command | Description |
|---------|-------------|
| `!status` | Zeigt Agent-Status |
| `!memory <query>` | Durchsucht Shared Memory |
| `!summarize` | Postet Zusammenfassung in #status (WAL Protocol) |

### 4. WAL Protocol Integration
- Jede Änderung wird zuerst geschrieben, dann ausgeführt
- Deutsche Trigger-Wörter unterstützt
- Persistenz über Sessions hinweg

## Setup Instructions

### Step 1: Discord Developer Portal

1. Gehe zu https://discord.com/developers/applications
2. Erstelle 5 neue Applications:
   - **Henry** (Chief of Staff)
   - **Nexus** (CTO)
   - **Ivy** (Researcher)
   - **Knox** (Security)
   - **Mr. X** (Content)

### Step 2: Bot Configuration

Für JEDE App:

1. **Sidebar: "Bot"**
   - Click "Reset Token"
   - Kopiere den Token (wird nur einmal angezeigt!)
   - Speichere ihn sicher

2. **Privileged Gateway Intents (WICHTIG!)**
   - ✅ **SERVER MEMBERS INTENT**
   - ✅ **MESSAGE CONTENT INTENT**
   - Speichern!

### Step 3: OAuth2 URL Generator

1. **Sidebar: "OAuth2" → "URL Generator"**
   - Scopes: ✅ `bot`, ✅ `applications.commands`
   - Bot Permissions:
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ View Channels
     - ✅ Embed Links
     - ✅ Add Reactions

2. **Generated URL kopieren** und im Browser öffnen
3. Server auswählen und autorisieren

### Step 4: Environment Variables

```bash
# ~/.bashrc oder ~/.zshrc hinzufügen:
export DISCORD_TOKEN_HENRY="YOUR_HENRY_TOKEN_HERE"
export DISCORD_TOKEN_NEXUS="YOUR_NEXUS_TOKEN_HERE"
export DISCORD_TOKEN_IVY="YOUR_IVY_TOKEN_HERE"
export DISCORD_TOKEN_KNOX="YOUR_KNOX_TOKEN_HERE"
export DISCORD_TOKEN_MR_X="YOUR_MR_X_TOKEN_HERE"
```

Dann laden:
```bash
source ~/.bashrc  # oder ~/.zshrc
```

### Step 5: Kanal-Struktur erstellen

Auf deinem Discord Server:

**Text Channels:**
- `#command-center` (nur Henry + User)
- `#status` (alle Agents können posten)
- `#general` (alle)
- `#engineering` (Nexus)
- `#research` (Ivy)
- `#security` (Knox)
- `#content` (Mr. X)

**Optional:**
- `#dev`, `#code-reviews` (Nexus)
- `#docs`, `#knowledge-base` (Ivy)
- `#logs`, `#alerts` (Knox)
- `#social`, `#media` (Mr. X)

### Step 6: Starten

```bash
# Dependencies installieren
pip install discord.py toml

# Mission Control starten
python3 ~/.openclaw/workspace/tools/mission_control.py
```

## Usage

### Commands pro Agent

Jeder Agent reagiert auf:
- `!status` - Zeigt aktuellen Status
- `!memory <query>` - Sucht im Shared Memory
- `!summarize` - Postet Summary nach #status

### Heartbeat

Automatisch alle 30 Minuten (konfigurierbar in `mission-control.toml`):
```
[12:30] Henry: [Henry] Status: online | Tasks: 2 | Last active: 12:30
[12:30] Nexus: [Nexus] Status: online | Tasks: 1 | Last active: 12:30
...
```

### Memory System

Das System nutzt das `~/self-improving/` Verzeichnis:

```
~/self-improving/
├── memory.md           # Global memory (alle Agents)
├── corrections.md      # Korrekturen
├── projects/agents/    # Agent-spezifisch
│   ├── henry.md
│   ├── nexus.md
│   └── ...
└── domains/            # Domänen-spezifisch
```

## Troubleshooting

### "Intents not enabled"
- Discord Developer Portal → Bot → Privileged Gateway Intents → BEIDE aktivieren

### "Token invalid"
- Token wurde wahrscheinlich zurückgesetzt
- Neuen Token generieren und in Environment Variable speichern

### Bot sieht keine Nachrichten
- Message Content Intent ist nicht aktiviert
- Bot hat keine Berechtigungen für den Kanal

## Advanced Configuration

### Heartbeat Interval ändern

`~/.openclaw/workspace/config/mission-control.toml`:
```toml
[heartbeat]
interval_minutes = 60  # Statt 30
```

### Neue Commands hinzufügen

In `mission_control.py`, in der `create_bot` Methode:

```python
@bot.command(name="mein_command")
async def mein_command(ctx):
    await ctx.send("Hallo!")
```

## Integration mit bestehendem System

Das Mission Control System integriert sich mit:
- ✅ `~/self-improving/` Memory System
- ✅ WAL Protocol (Write-Ahead Log)
- ✅ German trigger words
- ✅ Existing tools (video analysis, etc.)

## References

- Original Video: https://www.youtube.com/watch?v=GwSYhTrWWuA
- Discord.py Docs: https://discordpy.readthedocs.io/
- OpenClaw Docs: https://docs.openclaw.ai
