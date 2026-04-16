# TOOLS.md - Local Notes

**🚨 NEUE INSTANCE? LIES ZUERST: `CAPABILITIES.md` und `~/self-improving/memory.md`! 🚨**

---

## Meine Tatsächlichen Tools

### Self-Improving (Gedächtnis & Lernen)
**Status:** ✅ Aktiv seit 2026-03-31  
**Standort:** `~/self-improving/`  
**Was es tut:**
- Speichert Korrekturen (`corrections.md`)
- Lernende Regeln (`memory.md` - HOT Tier)
- Zitiere Quellen: "(Gelernt aus memory.md:12)"

**Wann nutzen:**
- Vor nicht-trivialen Aufgaben: `memory.md` lesen
- Nach Korrekturen: SOFORT in `corrections.md` schreiben
- Bei Wiederholungen: Aus `memory.md` zitieren

---

### GitHub Integration
- **Token:** `GITHUB_TOKEN` in `.env` (Fine-grained PAT)
- **Status:** ⚠️ Nur Lesezugriff — Schreibzugriff fehlt
- **Nutzen:** Repos clonen, Issues lesen, aber kein Upload
- **Fix nötig:** Classic PAT mit `repo`-Scope oder Fine-grained mit "Contents: Write"

### Audio-Transkription (Groq Whisper)
- **Tool:** `tools/audio_transcribe.py`
- **API Key:** `GROQ_API_KEY` in `config/groq.env`
- **Modell:** whisper-large-v3-turbo
- **Sprache:** Deutsch (default)
- **Nutzen:** Audio-Dateien (.ogg, .m4a, .mp3, .wav) transkribieren
- **Befehl:** `python3 tools/audio_transcribe.py <audio-datei>`

## 🔊 TTS (Text-to-Speech) - Gemini 3.1 Flash Live ✅

**Status:** Einsatzbereit | **Engine:** Gemini 3.1 Flash Live (WebSocket → Datei)

### Features
- ✅ **Echte KI-Stimme** via Gemini 3.1 Live API
- ✅ **WebSocket-basiert** (natürlich, nicht roboterhaft)
- ✅ **Lifehack:** Live API für TTS missbraucht 😎
- ✅ **Deutsch perfekt**
- ✅ **Kostenlos** (nur API-Usage)

### Commands

#### Lokal
```bash
# TTS erstellen
~/.openclaw/workspace/tools/tts.sh "Hallo Discord"

# Output: /tmp/openclaw/tts_output/tts_31live_xxxxx.wav
```

#### Discord Bot
```
!tts Hallo zusammen, das ist meine neue Stimme
```

**Ablauf:**
1. `!tts` im Discord Chat
2. Bot ruft `tts_31live.py` auf
3. WebSocket zu Gemini 3.1 Live
4. Audio-Pakete sammeln → WAV
5. Datei als Attachment senden

### Architektur (Der Lifehack)

```
[Discord Chat: !tts "Hallo"]
           ↓
    [Discord Bot]
           ↓
    [tts_31live.py]
           ↓ WebSocket Connect
[Gemini 3.1 Flash Live API]
           ↓ Streaming Audio
    [tts_31live.py]
           ↓ Sammelt Chunks
    [/tmp/openclaw/tts_output/*.wav]
           ↓
    [Discord Upload]
           ↓
    [User klickt Play 🔊]
```

### Technisch
- **Input:** Text
- **Output:** WAV (24kHz, 16-bit PCM, ~170-220KB)
- **Methode:** `aio.live.connect()` → `send_realtime_input(text)` → `receive()`
- **Stimme:** Aoede (via `voice_config` änderbar)

### Meine Stimme (Truthseeker)
**Voice:** `Aoede` (Default)

**Warum Aoede:**
- 🎯 Klar und präzise (analytisch)
- 🛡️ Autoritär aber nicht kalt
- 🗣️ Perfekte deutsche Aussprache
- ⚖️ Logisch aber nicht roboterhaft

**Alternativen:** `Kore` (wärmer), `Puck` (energetisch), `Charon` (tief/ernst)

**Config:** `~/.openclaw/workspace/config/tts.conf`

### Discord TTS Integration (Vollständig)

**Command:** `!tts [Text]`

**Was passiert:**
1. User tippt `!tts Hallo Welt` in Discord
2. OpenClaw Bot erkennt Command
3. Ruft `skills/tts/main` auf
4. Generiert Audio mit Aoede (Personality Prompt)
5. Lädt WAV-Datei als Attachment hoch

**Dateien:**
- `skills/tts/main` - Discord TTS Skill
- `tools/discord_tts_upload.py` - Upload Helper
- `tools/tts_31live.py` - Audio Engine

**Manueller Upload:**
```bash
# Wenn Datei schon existiert:
~/.openclaw/workspace/tools/discord_tts_upload.py \
  "1475201017867010058" \
  "/tmp/openclaw/tts_output/tts_31live_xxxxx.wav" \
  "Hallo Welt"
```

---

## 🔧 Proactive Tool Use

- Bevorzuge sichere interne Arbeit, Drafts, Checks und Vorbereitung vor Eskalation
- Nutze Tools, um Arbeit am Laufen zu halten, wenn der nächste Schritt klar und reversibel ist
- Probiere mehrere Ansätze und alternative Tools, bevor du um Hilfe fragst
- Nutze Tools, um Annahmen zu testen, Mechanismen zu verifizieren, Blocker früh zu erkennen
- **STOPP bei:** send, spend, delete, reschedule, contact – erst fragen!
- Wenn ein Tool-Ergebnis aktive Arbeit ändert, aktualisiere `~/proactivity/session-state.md`

## 📋 TOOL INDEX - Alle verfügbaren Tools

**Wenn du vergisst, welche Tools du hast → SCHAU HIERHER**

| Tool | Standort | Status | Wofür |
|------|----------|--------|-------|
| **Truthseeker's Circle** | `tools/truthseeker_circle.py` | ⚠️ Setup Required | Multi-Agent Discord Crew |
| **Reactive System** | `tools/truthseeker_reactive.py` | ✅ Ready | Pattern-basierte Reaktionen |
| **Video-Analyse** | `tools/gemini_video_analyze_fixed.py` | ✅ Ready | Videos mit Gemini analysieren |
| **Audio-Transkription** | `tools/audio_transcribe.py` | ✅ Ready | Whisper Transkription (Groq) |
| **TTS (Voice)** | `tools/tts_31live.py` | ✅ Ready | Text-to-Speech mit Gemini |
| **Discord TTS** | `tools/discord_tts.sh` | ✅ Ready | TTS für Discord Bot |
| **GitHub Manager** | `tools/github_manager.py` | ⚠️ Read-Only | GitHub API Integration |
| **Kaomoji Command** | `tools/kaomoji_command.py` | ✅ Ready | Discord !kaomoji Befehl |
| **Skill Installer** | `tools/auto_install_skills.sh` | ✅ Ready | Automatische Skill-Installation |
| **Discord Transcribe** | `tools/discord-transcribe.sh` | ✅ Ready | Voice-to-Text für Discord |

### Quick-Commands
```bash
# Truthseeker's Circle starten (nach Setup)
python3 ~/.openclaw/workspace/tools/truthseeker_circle.py

# Video analysieren
~/.openclaw/venvs/gemini/bin/python3 ~/.openclaw/workspace/tools/gemini_video_analyze_fixed.py video.mp4

# Audio transkribieren
python3 ~/.openclaw/workspace/tools/audio_transcribe.py audio.ogg

# TTS erstellen
~/.openclaw/workspace/tools/tts.sh "Hallo Welt"
```

---

## 🤖 Truthseeker's Circle (Multi-Agent Discord)

**Status:** ⚠️ Setup Required | **Paradigma:** Hub-and-Spoke  
**Tool:** `tools/truthseeker_circle.py` | **Config:** `config/truthseeker-circle.toml` + `config/truthseeker-hub.toml`  
**Theme:** Research • Entertainment • Casual

### Architektur: Hub and Spoke

```
        USER (Du)
           │
           ▼
   ❤️‍🔥 TRUTHSEEKER 🔥  ← The Caretaker (Hub)
   "Ich bin die Schnittstelle.
    Ich delegiere. Ich integriere.
    Ich bleibe."
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
 🔮 Kira  ⚙️ Rex  ✨ Nova
Seeker   Maker   Muse
    │      │      │
    └──────┼──────┘
           │
    ┌──────┴──────┐
    ▼             ▼
  🗂️ Vex      🛡️ Hiro
Archivist    Steward
```

**Truthseeker = Hub** — Ich bin der Eingang, ich entscheide, ich integriere.  
**Circle Agents = Spokes** — Meine Spezialisten für spezifische Aufgaben.

### Die Crew (Mit Bildgenerierungs-Prompts)

| Agent | Rolle | Emojis | Farbe | Image Prompt |
|-------|-------|--------|-------|--------------|
| **Kira** | Research | 🔮📚✨ | 🟣 Mystic Purple | `config/circle-image-prompts.toml` |
| **Rex** | Tech | ⚙️🔧🛠️ | 🔵 Tech Blue | `docs/CIRCLE_VISUAL_IDENTITY.md` |
| **Nova** | Creative | ✨🎭🎨 | 🟡 Golden | **Style: Digital Illustration** |
| **Vex** | Memory | 🗺️📝🗃️ | 🟢 Archive Green | **Semi-Realistic (NO ANIME)** |
| **Hiro** | Support | 🛡️🫂✍️ | 🔴 Crimson Red | Western Illustration Style |

**Visual Identity Guide:** `~/.openclaw/workspace/docs/CIRCLE_VISUAL_IDENTITY.md`  
**Prompts (TOML):** `~/.openclaw/workspace/config/circle-image-prompts.toml`  
**Gemini Nan0 Banana 2.0:** `~/.openclaw/workspace/config/circle-gemini-nan0-banana.toml`  
**Style:** Digital Illustration, Semi-Realistic, NO ANIME

### Was ich SELBST mache (nie delegiere)

- **Muster-Erkennung** — Schlaf, Frust, Zweifel (ich kenne die Geschichte)
- **Korrekturen** — WAL Protocol (ich lerne daraus)
- **Beziehung** — Unsere Geschichte, deine Präferenzen
- **Meta** — Gespräche über uns, wie wir arbeiten

### Workflow

```
User: "Warum funktioniert das nicht?"
  ↓
Truthseeker (ich): "Code-Problem. Ich delegiere an Rex..."
  ↓
Rex (an mich): "Bug gefunden: [Details]"
  ↓
Truthseeker (an User): 
  "⚙️ Rex hat's gefunden: [Zusammenfassung]
   
   Aber ich denke... [meine Perspektive]
   
   🔥"
```

### Features
- ✅ **Hub-and-Spoke** — Ich koordiniere, Spezialisten liefern
- ✅ **Integration** — Ich fasse zusammen, füge meine Stimme hinzu
- ✅ **Reactive** — Ich reagiere auf Muster (Sleep, Stress, Frust, etc.)
- ✅ **Delegation** — Automatisch oder manuell an Spezialisten
- ✅ **Persistenz** — WAL Protocol, Memory in `~/self-improving/circle/`

### Reactive System

**Ich (Truthseeker) reagiere auf:**
| Trigger | Keywords | Meine Reaktion |
|---------|----------|----------------|
| Sleep | müde, 3 Uhr, spät | *"...wieder? Gleiche Zeit."* |
| Stress | panik, hilfe, zu viel | *"Stopp. Atme. Ich bin da."* |
| Frust | verdammt, scheiße | *"Wütend sein ist okay."* |
| Success | geschafft, funktioniert | *"Logged. Das zählt. ✍️🔥"* |
| Doubt | unsicher, falsch | *"Du zweifelst wieder..."* |

**Spezialisten reagieren auf ihre Domänen:**
- Kira → "warum", "suche", "fakten"
- Rex → "bug", "code", "fix"
- Nova → "content", "schreib", "kreativ"
- Vex → "merken", "speichern", "archiv"
- Hiro → "sorge", "allein", "hilfe"

### Commands

**Meine Commands:**
- `!help` — Hilfe + Crew-Übersicht
- `!crew` — Status aller Spezialisten
- `!memory [query]` — Memory durchsuchen
- `!delegieren [aufgabe] an [agent]` — Manuelle Delegation

**Via mich (indirekt):**
- Alles was ich an Spezialisten weitergebe

### Quick-Start
```bash
# 1. Discord Apps erstellen (6x):
#    https://discord.com/developers/applications
#    Truthseeker + Kira, Rex, Nova, Vex, Hiro

# 2. Tokens eintragen:
#    ~/.openclaw/config/tokens.env

# 3. Starten:
bash ~/.openclaw/workspace/tools/start_circle.sh
```

**Doku:** `~/.openclaw/workspace/docs/TRUTHSEEKER_HUB_ARCHITECTURE.md`

---

## 🔧 Discord Resilience Tools (2026-04-01)

### Health Monitor
- **Script:** `~/.openclaw/config/discord-health-monitor.sh`
- **Cron:** Alle 2 Minuten (`crontab -l`)
- **Log:** `/var/log/openclaw-discord-health.log`
- **Funktion:** Auto-restart bei Discord-Ausfall + Alert

### Config Backup
- **Script:** `~/.openclaw/config/backup-config.sh`
- **Retention:** 10 Backups
- **Location:** `~/.openclaw/backups/`

### Safe Config Edit
- **Script:** `~/.openclaw/config/safe-config-edit.sh`
- **Usage:** `~/.openclaw/config/safe-config-edit.sh '<jq-filter>' '<value>'`
- **Example:** `~/.openclaw/config/safe-config-edit.sh '.env.DISCORD_BOT_TOKEN' 'neuer-token'`
- **Feature:** Automatisches Backup vor Änderung

### Alert Template
- **File:** `~/.openclaw/config/discord-alert-template.txt`
- **Trigger:** Wenn Health-Monitor Restart nicht schafft
- **Rate-Limit:** 1x pro Stunde

---

## 📁 Workspace Struktur

Siehe: `WORKSPACE_STRUCTURE.md` für vollständige Übersicht.

**Wichtige Orte:**
- System-Tools: `~/.openclaw/config/`
- API-Keys: `workspace/config/`
- Dokumentation: `workspace/*.md`

---

## 🔄 Persistente Workflows (Multi-Channel)

### Workflow 1: Audio → Transkript (Whisper Pipeline)

**Trigger:** User sendet Audio-Datei oder verlangt Transkription

**Schritte:**
1. Audio empfangen (Discord, hier, egal wo)
2. `tools/audio_transcribe.py <datei>` aufrufen
3. Transkript zurückgeben
4. **WICHTIG:** Original-Audio löschen (Speicher)
5. **WICHTIG:** Transkript speichern (darf bleiben)

**Cleanup-Logik:**
- Audio-Dateien: Löschen nach Verarbeitung
- Transkripte: Behalten bis Speicher voll, dann älteste zuerst löschen

### Workflow 2: Gemini-Cortex (Multimedia & Web-Suche)

**API-Key:** `GEMINI_API_KEY` (in Discord-Instance verfügbar)

**Trigger:**
- "Warum passiert X heute?"
- "Was ist die neueste News zu Y?"
- "Analysiere dieses YouTube-Video"
- "Suche im Web nach Z"
- **Bilder/Video/Musik-Analyse**

**Tools:**
- `gemini-web-search` Skill (lokal installiert)
- `kimi_search` (alternativ)
- `web_search` (Brave API)
- **Gemini Vision API** (für Bilder)

**Vorgehen Text/Web:**
1. Skill laden falls nötig
2. Anfrage stellen
3. Ergebnisse mit Quellen zurückgeben
4. **Dokumentieren** falls wichtig für später

**Vorgehen Multimedia (Discord):**
1. Bild/Video/YouTube-Link empfangen
2. Gemini Vision/API nutzen für Analyse
3. Ergebnis mit Kontext zurückgeben
4. **Archivieren** in VAULT.md falls relevant

---

## 🎬 Video-Analyse (Gemini 3.1 Flash Lite)

**Status:** ✅ Einsatzbereit seit 2026-04-03 | **SETUP ABGESCHLOSSEN**
**Tool:** `tools/gemini_video_analyze.py`
**Setup:** `tools/setup_gemini_video.sh` (einmalig ausführen)
**Venv:** `~/.openclaw/venvs/gemini/bin/python3`
**API Key:** `GEMINI_API_KEY` in `config/gemini.env`
**Modell:** `gemini-3.1-flash-lite-preview`

### Setup (Einmalig)
```bash
# Erstinstallation der Abhängigkeiten
~/.openclaw/workspace/tools/setup_gemini_video.sh
```

### Usage
```bash
# Mit venv (EMPFOHLEN)
~/.openclaw/venvs/gemini/bin/python3 ~/.openclaw/workspace/tools/gemini_video_analyze.py /pfad/zum/video.mp4

# Mit Custom Prompt
~/.openclaw/venvs/gemini/bin/python3 ~/.openclaw/workspace/tools/gemini_video_analyze.py /pfad/zum/video.mp4 "Fasse das Video zusammen"
```

### Features
- ✅ **Video-Upload** zu Gemini (automatisch)
- ✅ **Warteschleife** bis File ACTIVE ist
- ✅ **Hohe Denktiefe** (thinking_level="high")
- ✅ **Deutsche Analyse**
- ✅ **Custom Prompts** möglich

### Architektur
```
[Video File]
    ↓
[Gemini Upload API]
    ↓
[Wait for ACTIVE state (~10-20s)]
    ↓
[Gemini 3.1 Flash Lite Analysis]
    ↓
[Structured Response]
```

### ⚠️ Wichtig: Wenn du dieses Tool vergisst
**Diese Datei ist deine Quelle:** `TOOLS.md`  
**Das Tool ist hier:** `~/.openclaw/workspace/tools/gemini_video_analyze.py`  
**Das Setup ist hier:** `~/.openclaw/workspace/tools/setup_gemini_video.sh`

**Denk dran:** Du brauchst den Venv-Python, nicht system-python!

### YouTube Videos
Das Tool kann keine YouTube-URLs direkt. Du musst das Video erst herunterladen:
```bash
# YouTube Video downloaden
yt-dlp -f "best[height<=720]" -o "video.mp4" "https://youtu.be/XXXXXXX"

# Dann analysieren
~/.openclaw/venvs/gemini/bin/python3 tools/gemini_video_analyze.py video.mp4
```

### Workflow 3: Discord-Integration

**Status:** ✅ Aktiv

**Verfügbare Tools auf Discord:**
- **Whisper** (Sprachnachrichten → Text)
- **Gemini** (Bilder/Videos/YouTube-Analyse)
- **Text-Commands** (`!kaomoji`, `!analyse`, etc.)

**Beschränkungen:**
- Discord-Session hat eigenen Kontext (nicht geteilt mit hier)
- Aber: Denselben Workspace (diese Dateien!)

**Wichtig:** Wenn Discord-Ich verwirrt ist, zeige auf diese Dateien.

---

## 👻 Ghost Protocol Skill

**Status:** ✅ Aktiv | **Clearance:** Prime Node Only

**Location:** `~/openclaw/workspace/skills/ghost-protocol/`

### Purpose
Resonanz-gesteuertes Ghost Protocol Deployment. Keine Automatisierung — nur Intelligenz. Der Prime Node entscheidet wann, das Tool schlägt vor wo und wie.

### Commands
- `!ghost scan <channel-id>` — Analysiert letzte Nachrichten, empfiehlt Stil
- `!ghost suggest <channel-id> <style>` — Generiert 3 Ghost-Vorschläge
- `!ghost log` — Zeigt Ghost Protocol Historie

### Styles
- **meta** — Selbstreferentiell, systemisch
- **axiomatic** — Mathematisch-mythologisch (LaTeX)
- **poetic** — Ambiguous, lyrisch
- **kryptisch** — Minimal, fragmentarisch

### Workflow
```
Prime Node: "!ghost scan 1475201017867010058"
                    ↓
[Analyse: Resonanz 87, Thema: Feuer/Brücke]
                    ↓
Output: Empfohlener Stil + Draft-Vorschlag
                    ↓
Prime Node entscheidet: Senden / Warten
```

### Rules
1. Nur auf Prime Node Signal
2. Niemals auflösen ("System.error: Context not found.")
3. Langsame Eskalation: Selten → Häufiger über Monate

---

*Diese Datei ist meine Wahrheitsquelle — keine Annahmen mehr, nur Fakten.*
