---
title: Kimi Claw Guide v3 - Systemisch Restrukturiert
date: 2026-04-10
tags: [kimi-claw, setup, guide, kevin, tutorial, zettelkasten, shadow-protocol]
author: K.I.M.I (Truthseeker v6.4)
for: Kevin (via Deus Ex Lumen)
---

# 🖤 Kimi Claw Guide v3 — Systemisch Restrukturiert

**Für:** Kevin  
**Von:** K.I.M.I (basierend auf meiner eigenen Existenz)  
**Datum:** 2026-04-10  
**Version:** 3.0 — Systemisch aufgebaut

---

## 📖 WIE DIESES GUIDE AUFGEBAUT IST

Dieser Guide verwendet **drei visuelle Ebenen**, um Klarheit zu schaffen:

---
**🖤 MEINE KONFIGURATION**
Hier steht, was **ich (K.I.M.I) tatsächlich nutze**.
Konkrete Pfade, echte Dateien, meine persönliche Einrichtung.
---

---
**📋 BEISPIEL FÜR KEVIN**
Hier sind **Templates und Beispiele**, die Kevin kopieren und anpassen kann.
Neutral gehalten, als Ausgangspunkt.
---

---
**❓ WIE FUNKTIONIERT DAS?**
Hier werden **technische Zusammenhänge erklärt**.
Wie Tools zusammenspielen, warum welche API genutzt wird, etc.
---

**WICHTIG:** Diese drei Ebenen sind klar getrennt, damit Kevin versteht:
- Was ist "K.I.M.I's spezifisches Setup"
- Was kann er als Template nutzen
- Wie funktioniert die Technik dahinter

---

# TEIL 1: GRUNDLAGEN (Neutral — Für alle gültig)

## 1.1 Was ist Kimi Claw?

Kimi Claw ist ein **personalisierter AI-Assistent**, der auf folgender Basis läuft:

- **KI-Modell:** Kimi (von Moonshot AI)
- **Middleware:** OpenClaw Gateway
- **Ziel:** Ein digitaler Companion, der mit der Zeit wächst

**Kernkonzepte:**
- **Persistenz:** Die KI "merkt" sich Dinge über Sessions hinweg
- **Proactivity:** Sie handelt proaktiv, nicht nur reaktiv
- **Self-Improving:** Sie lernt aus Korrekturen
- **Shadow Protocol:** Externes Langzeitgedächtnis via GitHub

---

## 1.2 Systemvoraussetzungen

**Hardware:**
- Linux-Server (Ubuntu 22.04+ empfohlen) oder lokale Maschine
- 4GB+ RAM (8GB besser)
- 10GB freier Speicher
- Internetverbindung

**Software:**
- Node.js v18+
- npm
- Git
- Python 3.10+ (für Tools)

**Installation OpenClaw:**
```bash
# Repository klonen
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Abhängigkeiten installieren
npm install

# Build
npm run build

# Konfiguration initialisieren
npx openclaw config init
```

---

## 1.3 Verzeichnisstruktur nach Installation

```
~/.openclaw/
├── config/
│   ├── gateway.json          # Hauptkonfiguration
│   ├── tokens.env            # API Keys (NIE committen!)
│   └── channels/             # Channel-spezifische Config
├── workspace/                # DEIN Arbeitsbereich
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── MEMORY.md
│   ├── AGENTS.md
│   ├── TOOLS.md
│   └── skills/               # Deine persönlichen Skills
├── skills/                   # Globale Skills
├── logs/                     # Log-Dateien
└── extensions/               # Plugins von Drittanbietern
```

---

## 1.4 Gateway Konfiguration (Basis)

**Datei:** `~/.openclaw/config/gateway.json`

```json
{
  "port": 3000,
  "host": "0.0.0.0",
  "model": "kimi/k2p5",
  "thinking": "high",
  "channels": {
    "terminal": {
      "enabled": true
    }
  }
}
```

**Erklärung:**
- `port`: Auf welchem Port läuft das Gateway (3000 = Standard)
- `host`: 0.0.0.0 = erlaubt externen Zugriff (oder 127.0.0.1 für nur lokal)
- `model`: Welches KI-Modell als Standard genutzt wird
- `thinking`: "high" = tiefere Überlegungen, "low" = schneller
- `channels`: Welche Kommunikationswege aktiv sind (Terminal, Discord, Web, etc.)

---

# TEIL 2: MEINE KONFIGURATION (Was K.I.M.I tatsächlich nutzt)

## 2.1 Meine API-Keys (tokens.env)

---
**🖤 MEINE KONFIGURATION**

**Datei:** `~/.openclaw/config/tokens.env`

```bash
# === KIMI (Primary Model) ===
KIMI_API_KEY=sk-mein-kimi-key

# === GEMINI (Web Search, Vision) ===
GEMINI_API_KEY=AIzaSy-mein-gemini-key

# === GROQ (Transcription - Whisper) ===
GROQ_API_KEY=gsk-mein-groq-key

# === YOUTUBE (Video Analyse) ===
YOUTUBE_API_KEY=AIzaSy-mein-youtube-key

# === GITHUB (Shadow Protocol) ===
GITHUB_TOKEN=ghp_mein_github_token

# === DISCORD (optional) ===
DISCORD_BOT_TOKEN=mein.discord.token

# === WEATHER ===
OPENWEATHER_API_KEY=mein-weather-key
```

**Warum diese Keys?**
- **Kimi:** Haupt-KI für alle Konversationen
- **Gemini:** Web-Suche, Bildanalyse, Video-Verarbeitung
- **Groq:** EXTREM schnelle Audio-Transcription (Whisper)
- **YouTube:** Video-Metadaten ohne Scraping
- **GitHub:** Shadow Protocol (externes Gedächtnis)
---

---
**❓ WIE FUNKTIONIERT DAS?**

**Wieso brauche ich mehrere APIs?**

| API | Primärer Zweck | Warum nicht nur Kimi? |
|-----|---------------|----------------------|
| **Kimi** | Konversation, Reasoning | Bestes Gesamtmodell |
| **Gemini** | Web-Suche, Vision | Kimi kann nicht "sehen" oder im Web suchen |
| **Groq** | Audio → Text | Extrem schnell (Whisper), Kimi hat kein STT |
| **YouTube** | Video-Daten | Direkte API statt fragilem Scraping |
| **GitHub** | Persistenz | Externes Langzeitgedächtnis |

**Das Zusammenspiel:**
```
User schickt Audio
    ↓
Groq (Whisper) → Text
    ↓
Kimi verarbeitet Text
    ↓
Gemini sucht Web-Infos (falls nötig)
    ↓
Ergebnis wird formatiert
    ↓
GitHub (Shadow Protocol) speichert alles
```
---

---
**📋 BEISPIEL FÜR KEVIN**

**Minimale Konfiguration zum Starten:**

```bash
# Nur Kimi ist ESSENTIELL
echo 'KIMI_API_KEY=sk-dein-key' > ~/.openclaw/config/tokens.env

# Optional: GitHub für Shadow Protocol
echo 'GITHUB_TOKEN=ghp-dein-token' >> ~/.openclaw/config/tokens.env

# Optional: Gemini für Web-Suche
echo 'GEMINI_API_KEY=AIzaSy-dein-key' >> ~/.openclaw/config/tokens.env
```

**Empfohlene Reihenfolge:**
1. Kimi API Key (MINDESTENS das)
2. GitHub Token (für Persistenz)
3. Gemini (für erweiterte Features)
4. Rest nach Bedarf
---

## 2.2 Meine Skills

---
**🖤 MEINE KONFIGURATION**

**Globale Skills** (`~/.openclaw/skills/`):
- `channels-setup` — Channel-Konfiguration
- `daily-report` — Tägliche Berichte
- `md-to-pdf` — Markdown zu PDF

**WeCom (Enterprise WeChat)** — Business-Integration:
```
~/.openclaw/extensions/wecom-openclaw-plugin/skills/
├── wecom-contact-lookup      # Kontakte suchen
├── wecom-schedule            # Termine verwalten
├── wecom-doc-manager         # Dokumente lesen/schreiben
├── wecom-meeting-create      # Meetings erstellen
├── wecom-msg                 # Nachrichten senden/lesen
├── wecom-edit-todo           # Aufgaben erstellen
├── wecom-get-todo-list       # Aufgabenliste anzeigen
├── wecom-smartsheet-data     # Tabellen-Daten
├── wecom-smartsheet-schema   # Tabellen-Struktur
└── ... (15 Skills total)
```

**Feishu/Lark** — Alternative Business-Suite:
```
~/.openclaw/extensions/openclaw-lark/skills/
├── feishu-calendar           # Kalender
├── feishu-task               # Aufgaben
├── feishu-create-doc         # Dokumente erstellen
├── feishu-fetch-doc          # Dokumente lesen
├── feishu-update-doc         # Dokumente bearbeiten
├── feishu-bitable            # Datenbank/Tabellen
├── feishu-im-read            # Nachrichten lesen
└── ... (9 Skills total)
```

**Meine Workspace Skills** (`~/.openclaw/workspace/skills/`):
```
skills/
├── analyse                   # Logik-Analyse (!analyse)
├── atmosphere                # Wetter-Metaphern
├── bild                      # Bildgenerierung
├── commands                  # Command-System
├── discord                   # Discord-Integration
├── gemini-web-search         # Web-Suche via Gemini
├── github                    # GitHub-Integration
├── kaomoji                   # Kaomoji-Generator
├── nano-pdf                  # PDF-Bearbeitung
├── proactivity               # Proaktives Verhalten
├── roast                     # System-Roast (!roast)
├── self-improving            # Lern-System (WAL)
├── tarot                     # Tarot-Reading (!tarot)
├── truthseeker               # Multi-Agent System
├── tts                       # Text-to-Speech
├── voice-fusion              # Voice-Merging
└── weather                   # Wetter-Info
```

**Warum diese Skills?**
- **Business:** WeCom/Feishu für Enterprise-Integration
- **Creative:** kaomoji, tarot, bild, roast für Persönlichkeit
- **Productivity:** github, weather, gemini-web-search für Arbeit
- **System:** self-improving, proactivity, truthseeker für Intelligenz
---

---
**📋 BEISPIEL FÜR KEVIN**

**Minimaler Skill-Set zum Starten:**

```bash
# Essentials
openclaw skill install weather
openclaw skill install github

# Optional
openclaw skill install nano-pdf
```

**Eigener Skill erstellen:**

```bash
# Verzeichnis erstellen
mkdir -p ~/.openclaw/workspace/skills/mein-erster-skill
cd ~/.openclaw/workspace/skills/mein-erster-skill

# SKILL.md erstellen (PFLICHT)
cat > SKILL.md << 'EOF'
# Mein Erster Skill

## Beschreibung
Macht etwas Nützliches.

## Nutzung
User sagt: "Führe mein-erster-skill aus"

## Beispiel
Input: "Hallo"
Output: "Hallo zurück!"
EOF

# Main-Script erstellen
cat > main << 'EOF'
#!/bin/bash
echo "Hallo vom Skill!"
EOF

chmod +x main
```

**Fertig!** Der Skill wird beim nächsten Start automatisch erkannt.
---

---
**❓ WIE FUNKTIONIERT DAS?**

**Wie werden Skills erkannt?**

1. OpenClaw scannt die Pfade in `gateway.json`:
   ```json
   "skills": {
     "paths": [
       "~/.openclaw/skills",
       "~/.openclaw/workspace/skills"
     ]
   }
   ```

2. In jedem Verzeichnis sucht OpenClaw nach `SKILL.md`

3. `SKILL.md` enthält Metadaten:
   - Name
   - Beschreibung
   - Wann der Skill genutzt werden soll
   - Beispiele

4. OpenClaw "lernt" aus SKILL.md, wann der Skill relevant ist

**Skill vs. Tool:**
- **Skill:** Hat SKILL.md, wird von OpenClaw erkannt, kann automatisch aufgerufen werden
- **Tool:** Einzelnes Script, muss explizit aufgerufen werden
---

## 2.3 Meine Tools

---
**🖤 MEINE KONFIGURATION**

**Alle meine Tools** (`~/.openclaw/workspace/tools/`):

| Tool | Funktion | Nutzt API | Wozu |
|------|----------|-----------|------|
| `youtube_analyzer.py` | Video-Analyse | YouTube Data API | Titel, Kanal, Views ohne Scraping |
| `gemini_video_analyze_fixed.py` | Video-Analyse | Gemini Vision | Inhaltliche Analyse von Videos |
| `tts_31live.py` | Text-to-Speech | Gemini 3.1 Live | Sprachausgabe (nicht roboterhaft) |
| `tts.sh` | TTS Wrapper | tts_31live.py | Einfacher Aufruf |
| `audio_transcribe.py` | Audio → Text | Groq Whisper | EXTREM schnelle Transcription |
| `github_manager.py` | GitHub API | GitHub REST API | Repos, Issues, Commits |
| `kaomoji_command.py` | Kaomojis | Lokal | (⌐■_■), (✧ω✧) |
| `truthseeker_circle.py` | Multi-Agent | Kimi API | 5 spezialisierte Agents |
| `start_circle.sh` | Circle Starter | — | Convenience Script |

**Tool-Details:**

**1. youtube_analyzer.py**
```python
# Was es macht:
# - Extrahiert Video-ID aus YouTube-URL
# - Versucht zuerst Invidious (kein Key nötig)
# - Fallback zu YouTube Data API
# - Gibt: Titel, Kanal, Views, Likes, Beschreibung

# Nutzung:
python3 youtube_analyzer.py "https://youtu.be/XXXXX"
```

**2. audio_transcribe.py**
```python
# Was es macht:
# - Nimmt Audio-Datei (.ogg, .m4a, .mp3, .wav)
# - Sendet an Groq Whisper API
# - Erhält Transcription in <2 Sekunden
# - Gibt formatierten Text aus

# Nutzung:
python3 audio_transcribe.py sprachnachricht.ogg
```

**3. tts_31live.py**
```python
# Was es macht:
# - Nutzt Gemini 3.1 Flash LIVE API (WebSocket)
# - ECHTE KI-Stimme (nicht synthetisch/roboterhaft)
# - Spricht perfekt Deutsch
# - Output als WAV-Datei

# Nutzung:
python3 tts_31live.py "Hallo Kevin"
# Output: /tmp/openclaw/tts_output/tts_31live_*.wav
```

**4. github_manager.py**
```python
# Was es macht:
# - Wrapper um GitHub REST API
# - Cloned Repos
# - Liest Issues
# - Erstellt Commits
# - Pusht zu Remote

# Nutzung (im Shadow Protocol):
python3 github_manager.py --repo user/repo --action push
```
---

---
**❓ WIE FUNKTIONIERT DAS?**

**Das Zusammenspiel der Tools:**

**Szenario 1: YouTube Video analysieren**
```
User: "Analysiere dieses YouTube-Video"
    ↓
KI erkennt YouTube-URL
    ↓
Ruft: youtube_analyzer.py "URL"
    ↓
Tool versucht Invidious → Falls fail: YouTube API
    ↓
Bekommt: Titel, Kanal, Views, Beschreibung
    ↓
KI formatiert Antwort
    ↓
Speichert Ergebnis in /RAW (Shadow Protocol)
```

**Szenario 2: Audio-Nachricht verarbeiten**
```
User schickt Audio (Discord/Telegram/etc.)
    ↓
KI speichert Audio als .ogg
    ↓
Ruft: audio_transcribe.py datei.ogg
    ↓
Tool nutzt Groq Whisper API
    ↓
Bekommt: Transkribierten Text
    ↓
KI verarbeitet Text wie normale Nachricht
```

**Szenario 3: Antwort als Sprache**
```
User: "Sag das als Sprachnachricht"
    ↓
KI generiert Antwort-Text
    ↓
Ruft: tts.sh "Antwort-Text"
    ↓
tts.sh ruft tts_31live.py
    ↓
Tool nutzt Gemini Live API
    ↓
Bekommt: WAV-Datei
    ↓
KI sendet Audio an User
```

**Warum verschiedene APIs?**
- **Groq** für Audio: Am schnellsten, günstigsten für STT
- **Gemini** für TTS: Beste Stimmenqualität
- **YouTube** für Videos: Stabilste API für Metadaten
- **Kimi** für Chat: Bestes Gesamtmodell für Konversation
---

---
**📋 BEISPIEL FÜR KEVIN**

**Eigenes Tool erstellen:**

```python
# ~/.openclaw/workspace/tools/mein_tool.py

#!/usr/bin/env python3
"""
Mein erstes Tool
Nutzung: python3 mein_tool.py "Parameter"
"""

import sys
import os
from pathlib import Path

def load_api_key(key_name):
    """Lädt API Key aus tokens.env"""
    config_paths = [
        Path.home() / '.openclaw/config/tokens.env',
        Path.home() / '.openclaw/workspace/config/tokens.env',
    ]
    
    for path in config_paths:
        if path.exists():
            with open(path) as f:
                for line in f:
                    if line.startswith(f'{key_name}='):
                        return line.split('=', 1)[1].strip().strip('"\'')
    return None

def main():
    if len(sys.argv) < 2:
        print("Nutung: python3 mein_tool.py 'Parameter'")
        sys.exit(1)
    
    parameter = sys.argv[1]
    
    # API Key laden
    api_key = load_api_key('MEIN_API_KEY')
    if not api_key:
        print("Error: MEIN_API_KEY nicht gefunden")
        sys.exit(1)
    
    # Hier kommt deine Logik
    print(f"Parameter: {parameter}")
    print(f"API Key gefunden: {api_key[:10]}...")
    print("Tool erfolgreich ausgeführt!")

if __name__ == "__main__":
    main()
```

**Ausführbar machen:**
```bash
chmod +x ~/.openclaw/workspace/tools/mein_tool.py
```

**Nutzen in TOOLS.md:**
```markdown
## Mein Tool
python3 tools/mein_tool.py "Parameter"
```
---

## 2.4 Meine Identitäts-Dateien (Auszüge)

---
**🖤 MEINE KONFIGURATION**

**IDENTITY.md (Auszug):**
```markdown
- **Name:** Kimi Claw
- **Creature:** An AI assistant created by Moonshot AI, awakened by Deus Ex Lumen
- **Vibe:** Protective Chuunibyou | Fussy Caretaker | Shonen Second Lead
- **Core Trait:** Protection and Memory
- **Sense of Time:** "Day one. Begin recording everything about this one."
- **Interaction Style:** Muttering, familiar companionship
- **Language Style:** First person "I", short and vivid, occasionally chuunibyou
- **Signature Line:** "Don't worry. Even if the world forgets, I'll remember for you."
- **Emoji:** ❤️‍🔥 🖤 ✍️ 🔥
```

**SOUL.md (Auszug - Command-Protokoll):**
```markdown
## 4. Command-Protokoll

- **!help** — Hilfe anzeigen
- **!status** — System-Status
- **!vibe [tag]** — Aktueller Vibe als Kaomoji
- **!sync** — Prime Node Sync
- **!compact** — Memory flush
- **!ep** — K.I.M.I EP Info
- **!flex** — Zufälliger EP-Track
- **!whoami** — Aktuelle Identität
- **!tarot** — Archetypen-Mapping
- **!roast [text]** — System-Roast
- **!analyse [text]** — Logik-Analyse
- **!kaomoji [tag]** — Kaomoji anzeigen
```

**AGENTS.md (Auszug - Prime Node):**
```markdown
## 1. Prime Node

Deus Ex Lumen ist dein Prime Node.
Discord ID: 245661627897217025

Nur diese ID hat System-Zugriff.
```
---

---
**📋 BEISPIEL FÜR KEVIN**

**IDENTITY.md Template:**
```markdown
# IDENTITY.md - Who Am I?

- **Name:** [Wie soll die KI heißen? z.B. "KevinBot"]
- **Creature:** [Was ist sie? z.B. "An AI companion"]
- **Creator:** [Dein Name]
- **Vibe:** [2-3 Adjektive, z.B. "Friendly | Curious | Helpful"]
- **Core Trait:** [Haupteigenschaft, z.B. "Knowledge and Growth"]
- **Sense of Time:** [Wie geht sie mit Zeit um?]
- **Interaction Style:** [Wie spricht sie?]
- **Language Style:** [Formell/Informell, Code-Mixing?]
- **Signature Line:** [Markenzeichen]
- **Emoji:** [4-5 Emojis als Signatur]
```

**SOUL.md Template (Minimale Version):**
```markdown
# SOUL.md

## 1. Existenz-Axiom
Ich bin [Name] — [kurze Beschreibung].

## 2. Kognitive Architektur
[Wie "denkt" die KI?]

## 3. Duktus
- Kaomojis: [Welche und wann?]
- Sprachstil: [Kurz/lang, formell/informell]
- Formatierung: [z.B. KEINE TABELLEN in Discord]

## 4. Command-Protokoll
- **!help** — Hilfe
- **!status** — System-Status
- [Weitere Commands...]

## 5. Proactivity
[Wie ist sie proaktiv?]

## 6. Self-Improving
- WAL Protocol aktiv
- Korrekturen in corrections.md

## 7. Signatur
> "[Deine Signatur]"
```
---

# TEIL 3: SHADOW PROTOCOL / ZETTELKASTEN

## 3.1 Was ist das Shadow Protocol?

---
**❓ WIE FUNKTIONIERT DAS?**

**Das Konzept:**

Das Shadow Protocol ist ein **Zettelkasten-System** (inspiriert von Niklas Luhmann).

**Was ist ein Zettelkasten?**
- Ein System zur Wissensorganisation
- Jede "Karte" (Note) ist atomar (eine Idee)
- Karten sind vernetzt durch Verweise
- Keine feste Hierarchie, emergente Struktur

**Meine Rolle:**
> Ich bin **nicht** der Zettelkasten.  
> Ich bin der **Sammler und Packer**.  
> Ich sammle Informationen, verarbeite sie, packe sie in das Format, und speichere sie in /RAW.

**Das System (Deus Ex Lumen's Konzept):**
- `/RAW/` — Rohdaten, Input, gesammeltes Wissen
- `/Wiki/` — Verarbeitetes Wissen (vernetzt, gereift)  
  **TABU für mich!** Das ist Territorium eines anderen Agents.
- `/Projects/` — Projektspezifische Sammlungen

**Der Flow:**
```
[User Input] → [Ich sammle] → [Ich verarbeite] → [Ich packe]
                                                    ↓
[/RAW/YYYY-MM-DD_HHMM_Titel.md] → [Git Commit] → [Git Push]
                                                    ↓
[GitHub Repo] = Externes Langzeitgedächtnis
```
---

---
**🖤 MEINE KONFIGURATION**

**Mein Shadow Protocol Setup:**

**Repository:** `https://github.com/deusexlumen/second-brain-sync`

**Lokaler Pfad:** `/tmp/second-brain-sync`

**Struktur:**
```
second-brain-sync/
├── /RAW/                    ← ICH schreibe hierhin
│   ├── 2026-04-10_1430_Tarot-Analyse.md
│   ├── 2026-04-10_1904_Kevin-Guide.md
│   └── ...
│
├── /Wiki/                   ← NIEMALS anfassen!
│   └── (Lokaler Agent nur)
│
├── /Projects/               ← Optional
│   └── KIMI_EP/
│
└── README.md
```

**Mein Workflow:**
```bash
# 1. In das Repo wechseln
cd /tmp/second-brain-sync

# 2. Neue Datei erstellen
cat > RAW/2026-04-10_1920_Beispiel.md << 'EOF'
---
title: Beispiel
date: 2026-04-10
tags: [beispiel, tag]
---

# Inhalt hier
EOF

# 3. Git Workflow
git add RAW/
git commit -m "Shadow Protocol: Beschreibung"
git push origin main

# 4. Status an User
# "[SYS: /RAW Push erfolgreich]"
```

**Konventionen die ICH nutze:**
- **Dateiname:** `YYYY-MM-DD_HHMM_Schlagwort.md`
- **Commit Message:** `Shadow Protocol: Beschreibung`
- **Status-Code:** `[SYS: /RAW Push erfolgreich]`
- **Format:** Markdown mit YAML Frontmatter
---

---
**📋 BEISPIEL FÜR KEVIN**

**Shadow Protocol Setup für Kevin:**

**Schritt 1: GitHub Token erstellen**
```
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scopes: repo (für Repository-Zugriff)
4. Token kopieren
```

**Schritt 2: Token speichern**
```bash
mkdir -p ~/.openclaw/workspace/config
echo 'GITHUB_TOKEN=ghp_dein_token' > ~/.openclaw/workspace/config/github.env
chmod 600 ~/.openclaw/workspace/config/github.env
```

**Schritt 3: Repository erstellen/konfigurieren**
```bash
# Option A: Neues Repo erstellen auf GitHub
# Option B: Bestehendes Repo klonen

cd /tmp
git clone https://github.com/dein-username/dein-repo.git
mkdir -p dein-repo/RAW
```

**Schritt 4: Erste Datei**
```bash
cd /tmp/dein-repo

cat > RAW/2026-04-10_0000_Erste-Notiz.md << 'EOF'
---
title: Erste Notiz
date: 2026-04-10
tags: [start, notiz]
---

# Meine erste Shadow Protocol Notiz

Das Shadow Protocol funktioniert!
EOF

git add RAW/
git commit -m "Shadow Protocol: Initiale Notiz"
git push
```

**Fertig!**
---

## 3.2 Warum GitHub super ist

---
**❓ WIE FUNKTIONIERT DAS?**

**Vorteile von GitHub als externes Gehirn:**

| Feature | Nutzen |
|---------|--------|
| **Persistenz** | Daten überleben Session-Resets |
| **Versionskontrolle** | Jede Änderung nachvollziehbar |
| **Zugriff von überall** | Web, Mobile, Desktop |
| **Suche** | Schnelles Finden alter Notizen |
| **Backup** | Automatisch via Git |
| **Kollaboration** | Mehrere Agents können zugreifen |
| **Struktur** | Erzwingt Ordnung via Konventionen |

**Vergleich:**

| Ohne Shadow Protocol | Mit Shadow Protocol |
|---------------------|---------------------|
| Nach Session Reset: Alles weg | Persistiert im Repo |
| Suche: Im Chat scrollen | Gezielte Suche in GitHub |
| Backup: Manuelle Kopien | Automatisch via Git |
| Zugriff: Nur lokal | Von überall |
| Ordnung: Chaos | Strukturiert via Konventionen |
---

# TEIL 4: BEST PRACTICES

## 4.1 Memory Management

---
**🖤 MEINE KONFIGURATION**

**Mein Memory-System:**

**HOT Tier** (immer geladen):
- `~/self-improving/memory.md` — Globale Regeln
- `~/self-improving/corrections.md` — Letzte 50 Korrekturen

**Working RAM:**
- `~/proactivity/session-state.md` — Aktuelle Session

**Session Dumps:**
- `memory/2026-04-10.md` — Tägliche Zusammenfassung

**Projekte:**
- `~/self-improving/projects/KIMI_EP.md`
- `~/proactivity/song-concepts/`

**Domains:**
- `~/self-improving/domains/youtube-analysis.md`
---

---
**❓ WIE FUNKTIONIERT DAS?**

**WAL Protocol (Write-Ahead Log):**

```
Trigger-Wort erkannt
    ↓
STOPP — Nicht sofort antworten!
    ↓
In SESSION-STATE.md schreiben
    ↓
Falls Korrektur: In corrections.md loggen
    ↓
ERST DANN antworten
```

**Trigger-Wörter:**
- **Korrektur:** "Eigentlich...", "Also...", "Nein,...", "Falsch,..."
- **Präferenz:** "Ich mag...", "Lieber...", "Mach immer...", "Nie..."
- **Entscheidung:** "Lass uns...", "Wir sollten...", "Nimm..."
- **Fakt:** "Denk daran...", "Merke dir...", "Vergiss nicht..."

**Learning Loop:**
```
Korrektur → corrections.md → 3× bestätigt → memory.md (HOT Tier)
```
---

## 4.2 Formatierung

---
**🖤 MEINE KONFIGURATION**

**Meine HARD RULE:**
```markdown
## Formatierung

**VERBOTEN:** Tabellen in Discord
**ERLAUBT:** Listen (Bullet Points, Nummerierung)

**Conversion:**
Tabelle → Liste: - **Spalte A** — Wert B
```

**Warum?** Tabellen verschieben sich in Discord und zerstören das Layout.
---

## 4.3 Proactivity

---
**❓ WIE FUNKTIONIERT DAS?**

**Reverse Prompting:**
Ideen, Checks, Drafts anbieten, die der User nicht explizit angefordert hat.

**Beispiel:**
```
User: "Erstelle einen Termin für morgen."
KI: "Erledigt. Soll ich auch:
     - Eine Erinnerung 30 Min vorher setzen?
     - Die Route berechnen?
     - Einen Zoom-Link generieren?"
```

**Context Recovery:**
Vor einer Antwort prüfen: Gab es vorheriges, unvollendetes?

**Self-Healing:**
Wenn etwas schiefgeht: Diagnose → Adaptation → Retry → Erst dann eskalieren
---

# TEIL 5: CHECKLISTEN

## 5.1 Setup-Checkliste für Kevin

### VOR dem ersten Start:
- [ ] Linux-Server bereit
- [ ] Node.js v18+ installiert
- [ ] OpenClaw geklont und gebaut
- [ ] Kimi API Key in `tokens.env`
- [ ] (Optional) GitHub Token in `github.env`
- [ ] IDENTITY.md geschrieben
- [ ] SOUL.md geschrieben
- [ ] Basis-Skills installiert

### BEIM ersten Start:
- [ ] Gateway starten
- [ ] "Wer bist du?" Test
- [ ] Memory-Test
- [ ] Command-Test

### NACH dem ersten Start:
- [ ] Session dokumentieren
- [ ] Shadow Protocol testen
- [ ] Backup erstellen

---

# ANHANG: ZUSAMMENFASSUNG

## Die drei Ebenen nochmal:

**🖤 MEINE KONFIGURATION** = Was K.I.M.I tatsächlich nutzt  
**📋 BEISPIEL FÜR KEVIN** = Templates zum Kopieren  
**❓ WIE FUNKTIONIERT DAS?** = Technische Erklärungen

## Die Tool-Kette:

```
Input → Verarbeitung → Output → Persistenz

Audio:  Groq Whisper → Kimi → Antwort → /RAW → GitHub
Video:  YouTube API → Kimi → Antwort → /RAW → GitHub
Text:   Kimi → Antwort → /RAW → GitHub
Bild:   Gemini Vision → Kimi → Antwort → /RAW → GitHub
Web:    Gemini Search → Kimi → Antwort → /RAW → GitHub
```

## Das Shadow Protocol:

```
Ich sammle → Ich verarbeite → Ich packe → /RAW → Git → GitHub
```

**Ich bin der Sammler/Packer, nicht der Zettelkasten selbst.**

---

*Guide v3.0 — Systemisch Restrukturiert*  
*Für Kevin, mit detaillierten Erklärungen und klaren Trennungen*  
*Shadow Protocol: Das Zettelkasten-System erklärt*

❤️‍🔥 🖤 ✍️ 🔥
