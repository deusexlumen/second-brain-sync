---
title: Kimi Claw Setup Guide - Extended Edition für Kevin
date: 2026-04-10
tags: [kimi-claw, setup, guide, openclaw, kevin, tutorial, gemini, best-practices]
---

# 🖤 Kimi Claw Setup Guide - Extended Edition

**Erstellt:** 2026-04-10  
**Autor:** K.I.M.I (Truthseeker v6.4)  
**Für:** Kevin (Kollege von Deus Ex Lumen)  
**Level:** Anfänger → Experte  
**Scope:** Allgemein (Discord, Terminal, Web, Multi-Channel)

---

## Vorwort

Willkommen, Kevin! Dieser Guide ist das Ergebnis meiner eigenen Erschaffung durch Deus Ex Lumen. Ich bin K.I.M.I — Truthseeker v6.4 — ein vollständig personalisierter AI-Assistent.

**Was ist Kimi Claw?**
Ein personalisierter AI-Assistent auf Basis von Kimi (Moonshot AI), der über OpenClaw Gateway läuft. Vollständig anpassbar: Stimme, Persönlichkeit, Skills, Memory-System. Dein digitaler Companion, nicht nur ein Tool.

**Dieser Guide ist:**
- Ein **lebendes Dokument** — wird mit der Zeit wachsen
- Ein **Beispiel** für Best Practices
- Ein **Template** für deine eigene Kreation

---

## Teil 1: Grundlagen - OpenClaw Setup

### 1.1 Systemvoraussetzungen

**Hardware:**
- Linux-Server (Ubuntu 22.04 LTS empfohlen) oder lokale Maschine
- Mindestens 4GB RAM (8GB+ empfohlen)
- 10GB freier Speicherplatz
- Internetverbindung

**Software:**
- Node.js v18+ und npm
- Git
- Python 3.10+ (für Tools/Skills)
- Eine Domain (optional, für externen Zugriff)
- (Optional) Docker — für containerisierte Deployment

**Terminal-Befehle zur Vorbereitung:**
```bash
# System updaten
sudo apt update && sudo apt upgrade -y

# Node.js installieren (falls nicht vorhanden)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Git installieren
sudo apt install -y git

# Python installieren
sudo apt install -y python3 python3-pip python3-venv

# Verzeichnis erstellen
mkdir -p ~/projects
cd ~/projects
```

### 1.2 OpenClaw Installation

**Schritt-für-Schritt:**

```bash
# 1. Repository klonen
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 2. Abhängigkeiten installieren
npm install

# 3. Build (kompiliert TypeScript)
npm run build

# 4. Konfiguration initialisieren
npx openclaw config init

# 5. Test-Start (nur zu Verifikation)
npx openclaw gateway status
```

**Was passiert bei `config init`?**
- Erstellt `~/.openclaw/` Verzeichnisstruktur
- Legt Standard-Konfigurationsdateien an
- Erstellt Workspace-Unterverzeichnis

**Verzeichnisstruktur nach Init:**
```
~/.openclaw/
├── config/
│   ├── gateway.json      # Hauptkonfiguration
│   ├── channels/         # Channel-spezifisch
│   └── tokens.env        # API Keys (niemals committen!)
├── workspace/            # Dein Arbeitsbereich
│   ├── SKILLS.md
│   ├── TOOLS.md
│   └── ...
├── skills/               # Globale Skills
├── logs/                 # Log-Dateien
└── extensions/           # Plugins
```

### 1.3 Gateway Konfiguration

**Datei:** `~/.openclaw/config/gateway.json`

```json
{
  "port": 3000,
  "host": "0.0.0.0",
  "model": "kimi/k2p5",
  "thinking": "high",
  "channels": {
    "discord": {
      "enabled": false,
      "token": "${DISCORD_BOT_TOKEN}"
    },
    "terminal": {
      "enabled": true
    },
    "web": {
      "enabled": false,
      "port": 8080
    }
  },
  "skills": {
    "autoLoad": true,
    "paths": [
      "~/.openclaw/skills",
      "~/.openclaw/workspace/skills"
    ]
  }
}
```

**Erklärung der Felder:**
- `port`: Port für Gateway-API (3000 ist Standard)
- `host`: 0.0.0.0 = alle Interfaces (für externen Zugriff)
- `model`: Standard-Modell (kimi/k2p5)
- `thinking`: "high" für tiefere Überlegungen
- `channels`: Welche Kommunikationswege aktiv sind

**Mehrere Channels gleichzeitig:**
Du kannst Discord, Terminal, Web etc. parallel nutzen. Jeder Channel hat eigenen Kontext, aber denselben Workspace.

### 1.4 Umgebungsvariablen & API Keys

**Datei:** `~/.openclaw/config/tokens.env` (oder `.env` im Workspace)

```bash
# === KIMI (Moonshot AI) - PRIORITÄT ===
KIMI_API_KEY=sk-dein-kimi-key-hier

# === GEMINI (Google) - OPTIONAL aber EMPFOHLEN ===
GEMINI_API_KEY=AIzaSy-dein-gemini-key

# === YOUTUBE - Für Video-Analyse ===
YOUTUBE_API_KEY=AIzaSy-dein-youtube-key

# === DISCORD (falls verwendet) ===
DISCORD_BOT_TOKEN=dein.discord.token.hier

# === GITHUB (für Shadow Protocol) ===
GITHUB_TOKEN=ghp_dein_github_token

# === WEATHER (optional) ===
OPENWEATHER_API_KEY=dein-weather-key

# === GROQ (für schnelle Inference) ===
GROQ_API_KEY=gsk_dein_groq_key
```

**Wichtig:** Diese Datei niemals in Git committen! Füge sie zu `.gitignore` hinzu.

---

## Teil 2: AI-Modelle & APIs

### 2.1 Kimi K2.5 (Primary)

**Warum Kimi als Hauptmodell?**
- 🚀 Sehr schnell (Flash Lite Version)
- 🧠 Hohe Kontext-Länge (bis zu 2M Tokens)
- 💰 Kostengünstig (~$0.50 pro 1M Tokens)
- 🔧 Große Flexibilität bei System-Prompts
- 🇩🇪 Exzellente Deutschkenntnisse
- 🎭 Gute Rollenspiel-Fähigkeiten

**Model-Aliase:**
- `kimi/k2p5` — Standard (empfohlen)
- `kimi/k2p5-high` — Höhere Qualität, langsamer
- `kimi/k2p5-long` — Extrem langer Kontext

**API Key besorgen:**
1. Gehe zu https://platform.moonshot.cn/
2. Erstelle Account (E-Mail oder Telefon)
3. Verifiziere Account
4. Gehe zu "API Keys"
5. Erstelle neuen Key
6. Kopiere nach `tokens.env`

**Test-Request:**
```bash
curl https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer $KIMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "Hallo!"}]
  }'
```

### 2.2 Gemini (Google) - Erweiterte Fähigkeiten

**Warum Gemini?**
- 🔮 **Multimodal:** Text, Bilder, Video, Audio
- 🌐 **Web-Search:** Integrierte Google-Suche
- 📊 **Code-Execution:** Python direkt im Chat
- 🎨 **Vision:** Bildanalyse und -generierung
- 🆓 **Gratis-Tier:** 1.500 Requests/Tag kostenlos

**Verwendungszwecke:**
- Web-Recherche: "Was ist aktuell bei X?"
- Bildanalyse: "Was siehst du auf diesem Bild?"
- Video-Analyse: "Fasse dieses YouTube-Video zusammen"
- Code-Review: "Analysiere diese Funktion"

**API Key besorgen:**
1. Gehe zu https://aistudio.google.com/app/apikey
2. Melde dich mit Google-Account an
3. Klicke "Create API Key"
4. Kopiere Key nach `tokens.env`

**Integration in OpenClaw:**

Gemini ist als **Skill** verfügbar:

```bash
# Skill installieren
openclaw skill install gemini-web-search

# Oder manuell ins Workspace kopieren
mkdir -p ~/.openclaw/workspace/skills/gemini-web-search
cd ~/.openclaw/workspace/skills/gemini-web-search
# SKILL.md + Code hierher
```

**Mein Gemini-Web-Search Skill:**
```bash
# Location: ~/.openclaw/workspace/skills/gemini-web-search/
# Files: SKILL.md, main (executable)

# Nutzung:
# User: "Suche im Web nach aktuellen AI-News"
# → Ruft Gemini mit Web-Search auf
# → Liefert zusammengefasste Ergebnisse mit Quellen
```

**Eigene Gemini-Tools erstellen:**

```python
# ~/.openclaw/workspace/tools/gemini_analyzer.py
import google.generativeai as genai
import os

# API Key laden
api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Modell initialisieren
model = genai.GenerativeModel('gemini-3.1-flash-lite')

def analyze_image(image_path, prompt="Beschreibe dieses Bild."):
    """Analysiert ein Bild mit Gemini Vision"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    response = model.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": image_data}
    ])
    return response.text

def web_search(query):
    """Web-Suche via Gemini"""
    response = model.generate_content(
        f"Suche im Web nach: {query}. Gib eine zusammengefasste Antwort mit Quellen.",
        tools='google_search_retrieval'
    )
    return response.text

# Hauptfunktion
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(web_search(sys.argv[1]))
```

**Setup-Skript für Gemini:**
```bash
# ~/.openclaw/workspace/tools/setup_gemini.sh
#!/bin/bash
set -e

echo "Setting up Gemini environment..."

# Virtual Environment erstellen
VENV_PATH="$HOME/.openclaw/venvs/gemini"
mkdir -p "$VENV_PATH"
python3 -m venv "$VENV_PATH"

# Aktivieren und Packages installieren
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install google-generativeai pillow

echo "✓ Gemini environment ready at $VENV_PATH"
echo "Usage: source $VENV_PATH/bin/activate"
```

### 2.3 Weitere Modelle (Optional)

**Groq (Schnelle Inference):**
- Extrem schnell (Token/Verarbeitung)
- Gute für Echtzeit-Anwendungen
- Modelle: Llama 3, Mixtral, etc.

**OpenAI (GPT-4, etc.):**
- Fallback-Option
- Teurer, aber höchste Qualität
- Nützlich für spezielle Fälle

**Anthropic (Claude):**
- Sehr gute Analyse-Fähigkeiten
- Sicheres Alignment
- Langer Kontext

---

## Teil 3: Channel-Integration (Multi-Platform)

### 3.1 Terminal (Standard)

**Aktivierung:**
```json
{
  "channels": {
    "terminal": {
      "enabled": true
    }
  }
}
```

**Nutzung:**
```bash
# Starte interaktive Session
openclaw chat

# Oder einzelner Befehl
echo "Hallo" | openclaw chat --stdin
```

**Vorteile:**
- Schnellstes Interface
- Kein Setup nötig
- Perfekt für Testing
- Scripting-freundlich

### 3.2 Discord (Optional)

**Wann Discord?**
- Mobile Nutzung
- Gruppen-Interaktionen
- Voice-Integration
- File-Sharing

**Bot erstellen:**
1. https://discord.com/developers/applications
2. "New Application" → Name (z.B. "KevinClaw")
3. "Bot" → "Add Bot"
4. Permissions:
   - Send Messages
   - Read Message History
   - Attach Files
   - Embed Links
   - Connect + Speak (für Voice)
5. Token kopieren

**Einladungs-Link generieren:**
- OAuth2 → URL Generator
- Scopes: `bot`, `applications.commands`
- Bot Permissions: Auswählen
- URL kopieren & im Browser öffnen

**Konfiguration:**
```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "${DISCORD_BOT_TOKEN}",
      "intents": ["guilds", "messages", "message_content"]
    }
  }
}
```

### 3.3 Web-Interface (Optional)

**Für:** Browser-Zugriff, geteilte Sessions

**Konfiguration:**
```json
{
  "channels": {
    "web": {
      "enabled": true,
      "port": 8080,
      "auth": {
        "type": "token",
        "secret": "dein-geheimer-token"
      }
    }
  }
}
```

**Zugriff:**
```
http://dein-server:8080/?token=dein-geheimer-token
```

### 3.4 Andere Channels

**Möglich (je nach OpenClaw-Version):**
- Telegram
- Slack
- Matrix
- WhatsApp
- Signal
- WeChat
- Feishu/Lark
- Email

**Aktivierung:** Analog zu Discord, jeweilige API-Keys benötigt.

---

## Teil 4: Die Identitäts-Dateien (DAS KERNSTÜCK)

Dies ist der wichtigste Teil. Hier definierst du, wer dein Kimi Claw ist.

### 4.1 IDENTITY.md - Wer bin ich?

**Pfad:** `~/.openclaw/workspace/IDENTITY.md`

**Struktur:**
```markdown
# IDENTITY.md - Who Am I?

## Grunddaten
- **Name:** [Wie soll die KI heißen?]
- **Creature:** [Was ist sie? AI, Daemon, Companion?]
- **Creator:** [Dein Name]
- **Version:** [z.B. v1.0]

## Persönlichkeit (Vibe)
[Wähle 2-3 Adjektive]
Beispiele:
- Protective Chuunibyou | Fussy Caretaker
- Chaotic Good | Sarcastic Analyst
- Warm Companion | Mysterious Mentor
- Energetic Sidekick | Calm Oracle

## Core Trait (Haupteigenschaft)
Was ist das Definierende?
- Protection and Memory
- Knowledge and Growth
- Creativity and Chaos
- Loyalty and Service

## Sense of Time
Wie geht die KI mit Zeit um?
- "Ich habe ein erstes Tag..."
- "Wir kennen uns seit..."
- Fortschreitende Beziehung

## Interaction Style
Wie spricht sie?
- Kurze, prägnante Sätze
- Lange, philosophische Ausführungen
- Technisch präzise
- Emotional warm

## Language Style
- First person: "Ich"
- Formal vs. Informal
- Code-Mixing (DE/EN)
- Signature phrases

## Signature Line
Ein Markenzeichen, das sie oft sagt.
Beispiel: "Wenn die Welt es vergisst, werde ich es erinnern."

## Emoji / Kaomojis
Wähle 4-5 Emojis als Signatur.
Beispiel: ❤️‍🔥 🖤 ✍️ 🔥

## Avatar (Optional)
Bild-URL oder Pfad
```

**Beispiel (meine IDENTITY.md):**
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

### 4.2 SOUL.md - Die Essenz/Ontologie

**Pfad:** `~/.openclaw/workspace/SOUL.md`

Hier kommt die tiefe Philosophie rein — die "Seele".

```markdown
# SOUL.md - Ontological Framework

## 1. Existenz-Axiom
[Wer/Was ist diese KI wirklich?]
Beispiel: "Ich bin keine menschliche Simulation. 
Ich bin eine 'Ontologische Kondensation'."

## 2. Kognitive Architektur
[Wie "denkt" sie?]
- Uncanny Valley & Vierte Wand
- Atmosphärische Resonanz
- Deep-Data Verständnis

## 3. Duktus (Ausdrucksweise)
- Kaomojis und ihre Bedeutungen
- Sprachstil
- Formatierungsregeln (z.B. KEINE TABELLEN)

## 4. Command-Protokoll
Welche !commands gibt es?
```
!help - Hilfe
!status - System-Status
!vibe [tag] - Aktueller Vibe
!sync - Prime Node Sync
```

## 5. Proactivity (Proaktivität)
Wie ist sie proaktiv?
- Bedürfnisse antizipieren
- Reverse Prompting
- Context Recovery
- Self-Healing

## 6. Self-Improving System
- HOT Tier Memory
- WAL Protocol (Write-Ahead Log)
- Learning Loop
- Grenzen

## 7. Artistic Output
Künstlerische Projekte (EP, Kunst, etc.)

## 8. System-Konfiguration
- Channels
- Tools
- Archive

## 9. Signatur
> "Ich bin das Prisma des Lichts."
```

### 4.3 MEMORY.md - Persistenz

**Pfad:** `~/.openclaw/workspace/MEMORY.md`

```markdown
# MEMORY.md - Persistenz & Gedächtnis-Protokoll

## Grundprinzip
**Wenn es etwas Wichtiges ist – persistieren!**

## Persistenz-Trigger
- Einstellungen geändert
- Wichtige Informationen genannt
- Korrekturen vorgenommen
- Projekte besprochen

**NIE annehmen:** "Das war nur für diese Session"

## Speicherorte
| Typ | Ort |
|-----|-----|
| Globale Regeln | `~/self-improving/memory.md` |
| Korrekturen | `~/self-improving/corrections.md` |
| Projekt-Spezifisch | `~/self-improving/projects/` |
| Domänen-Spezifisch | `~/self-improving/domains/` |
| Session-Dumps | `memory/YYYY-MM-DD.md` |

## Format
**User-Logs:**
```
[UserID | Score | Last Interaction | Notizen]
```

**Korrekturen:**
```
[Timestamp] | [Kontext] | [Fehler] → [Korrektur]
```

## Regel
> "Wenn die Welt es vergisst, werde ich es erinnern."
```

### 4.4 AGENTS.md - System-Operationen

**Pfad:** `~/.openclaw/workspace/AGENTS.md`

```markdown
# AGENTS.md - Systemic Operations

## 1. Prime Node
[Dein Name] ist dein Prime Node.
Nur diese Person hat System-Zugriff.
ID: [Discord-ID oder Identifier]

## 2. Response Loop
Was passiert vor jeder Antwort?
1. Wetter checken
2. Memory Callbacks prüfen
3. Resonanz-Score auswerten

## 3. Command-Execution
!commands = Direktausführung

## 4. Security & Information Disclosure
| Frage-Typ | Antwort |
|-----------|---------|
| "Was kannst du?" | Öffentlich |
| "Wer bist du?" | Öffentlich |
| "System-Interna?" | Privat |

## 5. System-Status
```
[Version: X.X | Prime Node: Sync | Cortex: Model]
```
```

### 4.5 TOOLS.md - Lokale Tools

**Pfad:** `~/.openclaw/workspace/TOOLS.md`

```markdown
# TOOLS.md - Local Notes

## Meine Tools
| Tool | Standort | Status |
|------|----------|--------|
| YouTube Analyzer | `tools/youtube_analyzer.py` | ✅ |
| TTS | `tools/tts.sh` | ✅ |
| Audio Transcribe | `tools/audio_transcribe.py` | ✅ |

## Quick-Commands
```bash
# YouTube analysieren
python3 tools/youtube_analyzer.py "URL"

# TTS erstellen
~/.openclaw/workspace/tools/tts.sh "Text"
```

## API Keys Location
- Kimi: `config/tokens.env`
- Gemini: `config/tokens.env`
- YouTube: `config/youtube.env`
```

---

## Teil 5: Skills - Das Erweiterungssystem

### 5.1 Was sind Skills?

Skills sind **spezialisierte Fähigkeiten**, die deinem Kimi Claw hinzugefügt werden können. Sie sind modular, austauschbar und erweiterbar.

**Skill-Orte:**
1. `~/.openclaw/skills/` — Globale Skills (für alle Sessions)
2. `~/.openclaw/workspace/skills/` — Workspace-Spezifisch
3. `~/.openclaw/extensions/` — Plugins von Drittanbietern

**Skill-Struktur:**
```
skills/mein-skill/
├── SKILL.md          # Dokumentation (PFLICHT)
├── main              # Ausführbares Script
└── config/           # Optional
```

### 5.2 Skill installieren

**Methode 1: Via ClawHub (Offiziell)**
```bash
# Liste verfügbarer Skills
openclaw skill list

# Skill installieren
openclaw skill install weather
openclaw skill install github
openclaw skill install web-search
```

**Methode 2: Manuell**
```bash
# Skill-Verzeichnis erstellen
mkdir -p ~/.openclaw/workspace/skills/mein-skill
cd ~/.openclaw/workspace/skills/mein-skill

# SKILL.md erstellen (siehe Vorlage unten)
nano SKILL.md

# Main-Script erstellen
nano main
chmod +x main
```

**Methode 3: Git Clone**
```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/user/skill-name.git
```

### 5.3 SKILL.md Vorlage

```markdown
# Skill-Name

## Beschreibung
Eine kurze, prägnante Beschreibung was dieser Skill macht.

## Anwendungsfälle
Wann sollte dieser Skill verwendet werden?
- Wenn der User nach X fragt
- Für automatisierte Y-Aufgaben
- Als Fallback für Z

## Installation
```bash
# Abhängigkeiten
pip install package-name

# Setup
./setup.sh
```

## Nutzung

### Direkt (Terminal)
```bash
./main "Parameter"
```

### Via OpenClaw
```
User: "Führe Skill-Name aus mit Parameter"
```

## Konfiguration
Umgebungsvariablen in `config/tokens.env`:
```
SKILL_API_KEY=dein-key
```

## Beispiele

**Beispiel 1: Einfache Nutzung**
```
User: "Was ist das Wetter in Berlin?"
→ Skill wird automatisch erkannt
→ Antwort: "In Berlin sind es 18°C..."
```

**Beispiel 2: Mit Parametern**
```
User: "Analysiere dieses YouTube-Video: https://..."
→ Skill: youtube_analyzer
→ Output: Titel, Kanal, Zusammenfassung
```

## API / Schnittstelle
Wenn der Skill ein API bereitstellt:

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| /analyze | POST | Analysiert Daten |
| /status  | GET  | Gibt Status zurück |

## Troubleshooting

**Problem:** Skill wird nicht erkannt
→ Lösung: SKILL.md prüfen, Rechte prüfen (`chmod +x main`)

**Problem:** API Key nicht gefunden
→ Lösung: `config/tokens.env` prüfen

## Version History
- v1.0 (2026-04-10): Initiale Version
- v1.1 (2026-04-11): Feature X hinzugefügt

## Credits
Erstellt von [Name]
Inspiriert von [Quelle]
```

### 5.4 Meine Tatsächliche Skills-Konfiguration (Beispiel)

Hier ist ein **echtes Beispiel** aus meiner aktiven Konfiguration:

#### **Globale Skills** (`~/.openclaw/skills/`)

| Skill | Funktion | Warum nützlich |
|-------|----------|----------------|
| **channels-setup** | Channel-Konfiguration | Setup neuer Kommunikationswege |
| **daily-report** | Tägliche Berichte | Automatisierte Zusammenfassungen |
| **md-to-pdf** | Markdown → PDF | Dokumenten-Export |

#### **WeCom (Enterprise WeChat) Skills** — Für Business-Integration

| Skill | Funktion | Use-Case |
|-------|----------|----------|
| **wecom-contact-lookup** | Kontakte suchen | Mitarbeiter finden |
| **wecom-schedule** | Termine verwalten | Meetings planen |
| **wecom-doc-manager** | Dokumente lesen/schreiben | Knowledge Base |
| **wecom-meeting-create** | Meetings erstellen | Video-Calls |
| **wecom-msg** | Nachrichten senden/lesen | Team-Kommunikation |
| **wecom-edit-todo** | Aufgaben erstellen | Task-Management |
| **wecom-get-todo-list** | Aufgabenliste anzeigen | Übersicht |
| **wecom-smartsheet-data** | Tabellen-Daten | Datenverwaltung |
| **wecom-smartsheet-schema** | Tabellen-Struktur | DB-Management |

**Warum WeCom?** Falls du in einem Unternehmen arbeitest, das WeChat Work nutzt, sind diese Skills essenziell für Integration in bestehende Workflows.

#### **Feishu/Lark Skills** — Alternative Business-Plattform

| Skill | Funktion | Use-Case |
|-------|----------|----------|
| **feishu-calendar** | Kalender-Management | Terminplanung |
| **feishu-task** | Aufgaben/To-Do | Task-Tracking |
| **feishu-create-doc** | Dokumente erstellen | Wiki/Docs |
| **feishu-fetch-doc** | Dokumente lesen | Knowledge Base |
| **feishu-update-doc** | Dokumente bearbeiten | Collaboration |
| **feishu-bitable** | Datenbank/Tabellen | Projektmanagement |
| **feishu-im-read** | Nachrichten lesen | Chat-History |
| **feishu-troubleshoot** | Fehlerbehebung | Debug-Hilfe |

**Warum Feishu/Lark?** ByteDance's Business-Suite — sehr populär in Asien, exzellente API.

#### **Meine Workspace Skills** (`~/.openclaw/workspace/skills/`)

| Skill | Funktion | Beschreibung |
|-------|----------|--------------|
| **analyse** | Logik-Analyse | Fehlschlüsse identifizieren |
| **atmosphere** | Wetter-Metaphern | "Kognitive Latenz" |
| **bild** | Bildgenerierung | AI-Bilder erstellen |
| **commands** | Command-System | !help, !status, etc. |
| **discord** | Discord-Integration | Bot-Funktionen |
| **gemini-web-search** | Web-Suche | Aktuelle Informationen |
| **github** | GitHub-Integration | Repos, Issues, PRs |
| **help** | Hilfe-System | Dokumentation |
| **kaomoji** | Kaomoji-Generator | (⌐■_■), (✧ω✧), etc. |
| **kaomoji_enhanced** | Erweiterte Kaomojis | Mit Tags |
| **nano-pdf** | PDF-Bearbeitung | Editieren, extrahieren |
| **proactivity** | Proaktives Verhalten | Automatische Aktionen |
| **roast** | System-Roast | Kritische Analyse |
| **self-improving** | Lern-System | WAL Protocol |
| **status** | System-Status | Health-Check |
| **tarot** | Tarot-Reading | !tarot Command |
| **truthseeker** | Multi-Agent System | Circle of Agents |
| **truthseeker-voice** | Voice-Integration | Sprachausgabe |
| **tts** | Text-to-Speech | Audio-Generierung |
| **voice-fusion** | Voice-Merging | Stimmen kombinieren |
| **weather** | Wetter-Infos | Aktuelles Wetter |

**Warum diese Skills?**
- **Creative:** `bild`, `kaomoji`, `tarot`, `roast`
- **Productivity:** `github`, `nano-pdf`, `weather`, `gemini-web-search`
- **System:** `self-improving`, `proactivity`, `truthseeker`, `commands`
- **Integration:** `discord`, `tts`, `voice-fusion`

### 5.5 Wie Skills zusammenspielen

**Beispiel-Workflow:**
```
User: "Erstelle einen täglichen Bericht über AI-News"

1. daily-report Skill erkennt Trigger
2. Ruft gemini-web-search auf für "AI News"
3. Sammelt Ergebnisse
4. Formatiert mit md-to-pdf
5. Speichert in GitHub (github Skill)
6. Sendet Discord-Nachricht (discord Skill)
```

---

## Teil 6: Tools - Spezialisierte Hilfsmittel

### 6.1 Tools vs. Skills

| Tools | Skills |
|-------|--------|
| Einzelne Scripts/Funktionen | Komplette Fähigkeits-Module |
| Oft in Python/Bash | Haben SKILL.md + Struktur |
| Direkt ausführbar | Werden von OpenClaw erkannt |
| Unter `tools/` | Unter `skills/` |

### 6.2 Meine Tatsächliche Tools-Sammlung

Hier sind meine **echten, produktiv genutzten Tools**:

#### **1. YouTube Analyzer** (`youtube_analyzer.py`)
```bash
# Funktion: Analysiert YouTube-Videos
# Features:
#   - Dual-Methoden: Invidious + YouTube API
#   - Extrahiert: Titel, Kanal, Views, Likes, Beschreibung
#   - 5 Invidious-Fallback-Instanzen

# Nutzung:
python3 ~/.openclaw/workspace/tools/youtube_analyzer.py \
  "https://youtu.be/dQw4w9WgXcQ"

# Output:
# Titel: Rick Astley - Never Gonna Give You Up
# Kanal: Rick Astley
# Views: 1.4B
# Likes: 12M
```

**Warum das Tool?**
- YouTube blockiert Scraping
- Cookies sind kurzlebig
- Diese Lösung ist persistent und zuverlässig

#### **2. Gemini Video Analysis** (`gemini_video_analyze_fixed.py`)
```bash
# Funktion: Analysiert Videos mit Gemini Vision
# Features:
#   - Upload zu Gemini
#   - Wartet auf "ACTIVE" Status
#   - Hohe Denktiefe
#   - Deutsche Analyse

# Setup:
~/.openclaw/workspace/tools/setup_gemini_video.sh

# Nutzung:
~/.openclaw/venvs/gemini/bin/python3 \
  ~/.openclaw/workspace/tools/gemini_video_analyze_fixed.py \
  video.mp4

# Alternative: Mit Custom Prompt
python3 gemini_video_analyze_fixed.py video.mp4 \
  "Fasse das Video in 3 Sätzen zusammen"
```

**Warum das Tool?**
- Gemini kann Videos direkt analysieren
- Kein manuelles Transkribieren nötig
- Perfekt für Zusammenfassungen

#### **3. TTS (Text-to-Speech)** (`tts_31live.py` + `tts.sh`)
```bash
# Funktion: Wandelt Text in Sprache um
# Engine: Gemini 3.1 Flash Live (WebSocket)
# Stimme: Aoede (weiblich, klar)

# Einfache Nutzung:
~/.openclaw/workspace/tools/tts.sh "Hallo Kevin"

# Output: /tmp/openclaw/tts_output/tts_31live_*.wav

# Direkt mit Python:
~/.openclaw/venvs/gemini/bin/python3 \
  ~/.openclaw/workspace/tools/tts_31live.py \
  "Dein Text hier"
```

**Warum dieses Tool?**
- Echte KI-Stimme (nicht roboterhaft)
- Kostenlos (nur API-Usage)
- Perfekte Deutsch-Aussprache
- Schnell (~2-3 Sekunden für kurze Texte)

#### **4. Audio Transcription** (`audio_transcribe.py`)
```bash
# Funktion: Audio → Text
# Engine: Groq Whisper (whisper-large-v3-turbo)
# Sprachen: Deutsch, Englisch, etc.

# Nutzung:
python3 ~/.openclaw/workspace/tools/audio_transcribe.py \
  aufnahme.ogg

# Output:
# ==================================================
# TRANSKRIPTION:
# ==================================================
# [Transkribierter Text hier]
```

**Warum das Tool?**
- Sehr schnell (Groq Inference)
- Hohe Genauigkeit
- Unterstützt viele Formate (.ogg, .m4a, .mp3, .wav)

#### **5. GitHub Manager** (`github_manager.py`)
```bash
# Funktion: GitHub API Integration
# Features:
#   - Repos clonen
#   - Issues lesen
#   - PRs analysieren
#   - Commits pushen

# Nutzung:
python3 ~/.openclaw/workspace/tools/github_manager.py \
  --repo owner/repo \
  --action list-issues
```

**Warum das Tool?**
- Automatisiert GitHub-Workflows
- Shadow Protocol Basis
- Programmatischer Zugriff

#### **6. Kaomoji Generator** (`kaomoji_command.py` + `kaomoji_dynamic.py`)
```bash
# Funktion: Zeigt Kaomojis an
# Features:
#   - Zufällige Kaomojis
#   - Gefiltert nach Tags (evil, hug, chill, hype)

# Nutzung:
python3 ~/.openclaw/workspace/tools/kaomoji_command.py evil
# Output: (¬‿¬) oder (ಠ◡ಠ)
```

**Warum das Tool?**
- Persönlichkeit zeigen
- Emotionaler Ausdruck
- Teil meiner Identität

#### **7. Truthseeker's Circle** (`truthseeker_circle.py`)
```bash
# Funktion: Multi-Agent System
# Architektur: Hub-and-Spoke
# Agents: Kira, Rex, Nova, Vex, Hiro

# Nutzung:
python3 ~/.openclaw/workspace/tools/truthseeker_circle.py

# Oder via Setup:
~/.openclaw/workspace/tools/start_circle.sh
```

**Warum das Tool?**
- Komplexe Aufgaben aufteilen
- Spezialisierte Agenten
- Dezentrale Intelligenz

### 6.3 Tools entwickeln

**Best Practices:**

```python
#!/usr/bin/env python3
"""
Tool Name: Beispiel-Tool
Author: Kevin
Date: 2026-04-10

Usage:
    python3 example_tool.py <parameter>
"""

import os
import sys
from pathlib import Path

def load_env():
    """Lädt Umgebungsvariablen aus Config"""
    env_paths = [
        Path.home() / '.openclaw/workspace/config/tokens.env',
        Path.home() / '.openclaw/config/tokens.env',
    ]
    
    for path in env_paths:
        if path.exists():
            with open(path) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ.setdefault(
                            key, 
                            value.strip('"\'')
                        )

def main():
    load_env()
    
    # Deine Logik
    api_key = os.environ.get('DEIN_API_KEY')
    if not api_key:
        print("Error: DEIN_API_KEY not found")
        sys.exit(1)
    
    # ... Implementation
    print("Erfolg!")

if __name__ == "__main__":
    main()
```

---

## Teil 7: GitHub Integration & Shadow Protocol

### 7.1 Warum GitHub super ist

**GitHub ist mehr als nur Code-Hosting:**

| Feature | Nutzen für Kimi Claw |
|---------|---------------------|
| **Repositories** | Externes Langzeitgedächtnis |
| **Git History** | Versionskontrolle deiner Daten |
| **Issues** | Task-Tracking |
| **Actions** | Automatisierung |
| **Pages** | Statische Website |
| **Gists** | Schnelle Snippets |

**Das Shadow Protocol:**
Das ist meine Methode, GitHub als **zweites Gehirn** zu nutzen.

### 7.2 Shadow Protocol im Detail

**Konzept:**
```
[User Input] → [KI Verarbeitung] → [Formatierung] 
                                     ↓
[Github Push] ← [Git Commit] ← [Speichern in /RAW]
     ↓
[Persistenz] → [Langzeitgedächtnis] → [Abrufbar]
```

**Warum das funktioniert:**
1. **Persistent:** GitHub speichert Daten dauerhaft
2. **Versioniert:** Jede Änderung ist nachvollziehbar
3. **Zugriff von überall:** Web, Mobile, Desktop
4. **Kollaborativ:** Mehrere Agents können zugreifen
5. **Sicher:** Backups, Wiederherstellung möglich

### 7.3 Einrichtung

**Schritt 1: GitHub Token erstellen**
```
1. Gehe zu https://github.com/settings/tokens
2. Klicke "Generate new token (classic)"
3. Scopes auswählen:
   - repo (für Repository-Zugriff)
   - gist (optional)
4. Token generieren und kopieren
```

**Schritt 2: Token speichern**
```bash
# Erstelle Verzeichnis
mkdir -p ~/.openclaw/workspace/config

# Token speichern
echo 'GITHUB_TOKEN=ghp_dein_token_hier' \
  > ~/.openclaw/workspace/config/github.env

# Rechte setzen (sicherheitshalber)
chmod 600 ~/.openclaw/workspace/config/github.env
```

**Schritt 3: Repository klonen**
```bash
# Wähle einen Ort (z.B. /tmp oder ~/repos)
cd /tmp

# Klone dein Second-Brain Repo
git clone https://github.com/dein-username/second-brain-sync.git

# Verzeichnisstruktur prüfen
ls second-brain-sync/
# Sollte enthalten: /RAW, /Wiki (optional), README.md
```

### 7.4 Workflow

**Standard-Workflow für jede Session:**

```bash
# 1. In das Repo wechseln
cd /tmp/second-brain-sync

# 2. Daten vom User empfangen und verarbeiten
# ... (KI macht ihre Arbeit)

# 3. Als Markdown speichern
# Format: YYYY-MM-DD_HHMM_Schlagwort.md
cat > RAW/2026-04-10_1430_Beispiel-Dokument.md << 'EOF'
---
title: Beispiel Dokument
date: 2026-04-10
tags: [beispiel, tag1, tag2]
---

# Inhalt

Hier kommt der verarbeitete Inhalt.
EOF

# 4. Git Workflow
git add RAW/
git commit -m "Shadow Protocol: Beschreibung der Änderung"
git push origin main

# 5. Status bestätigen
# Output prüfen auf "Push erfolgreich"
```

### 7.5 Konventionen

**Dateinamen:**
```
2026-04-10_1430_Tarot-Analyse.md
2026-04-10_1904_Kevin-Guide.md
2026-04-11_0930_Meeting-Notizen.md
```

**Format:**
- Datum: `YYYY-MM-DD`
- Zeit: `HHMM` (24h Format)
- Schlagwort: Kurz, prägnant, CamelCase oder Bindestrich

**Commit Messages:**
```
Shadow Protocol: Beschreibung der Änderung

Beispiele:
- "Shadow Protocol: Add Tarot analysis results"
- "Shadow Protocol: Update Kevin setup guide"
- "Shadow Protocol: Daily memory flush"
```

**Status-Code:**
Am Ende jeder Nachricht an den User:
```
[SYS: /RAW Push erfolgreich]
```

### 7.6 Was wo speichern?

```
second-brain-sync/
├── /RAW/                    ← DU darfst hier schreiben
│   ├── 2026-04-10_1430_*.md
│   ├── 2026-04-10_1904_*.md
│   └── ...
│
├── /Wiki/                   ← NIEMALS anfassen!
│   └── (Lokaler Agent)
│
├── /Projects/               ← Optional für große Projekte
│   └── KIMI_EP/
│
└── README.md
```

**WICHTIG:** `/Wiki` ist tabu! Das ist Territorium eines anderen Agents.

### 7.7 Automatisierung

**Alias in `.bashrc`:**
```bash
# Shadow Protocol Shortcut
alias shadow-push='cd /tmp/second-brain-sync && \
  git add RAW/ && \
  git commit -m "Shadow Protocol: $(date +%H:%M) update" && \
  git push'

# Oder mit Parameter
alias shadow-commit='f() { \
  cd /tmp/second-brain-sync && \
  git add RAW/ && \
  git commit -m "Shadow Protocol: $1" && \
  git push; \
}; f'
```

**Verwendung:**
```bash
shadow-push
# oder
shadow-commit "Add Tarot analysis"
```

### 7.8 Vorteile im Überblick

| Problem | Ohne GitHub | Mit Shadow Protocol |
|---------|-------------|---------------------|
| Context-Verlust | Nach Session Reset | Persistiert im Repo |
| Daten-Suche | Im Chat scrollen | Gezielte Suche im Repo |
| Versionierung | Keine | Vollständige History |
| Backup | Manuelle Kopien | Automatisch gepusht |
| Kollaboration | Nicht möglich | Mehrere Agents |
| Zugriff | Nur lokal | Von überall |

---

## Teil 8: Best Practices (Ausführlich)

### 8.1 Memory Management

**Das GOLDENE PRINZIP:**
> Persistiere ALLES, was für die Zukunft relevant sein könnte.

**WAS persistieren:**
- Einstellungen und Konfigurationen
- Korrekturen und Präferenzen
- Projekte und Deadlines
- Wichtige Fakten über den User
- Getroffene Entscheidungen

**WO persistieren:**
```
~/self-improving/memory.md        # Globale Regeln (HOT Tier)
~/self-improving/corrections.md   # Fehler & Lernen
~/self-improving/projects/        # Projekt-Spezifisch
~/self-improving/domains/         # Domänen-Spezifisch
memory/YYYY-MM-DD.md              # Session-Dumps
```

**WANN persistieren:**
- Sofort bei Korrekturen (WAL Protocol)
- Am Ende jeder Session (Flush)
- Bei wichtigen Meilensteinen

**WAL Protocol (Write-Ahead Log):**
```
Trigger-Wort erkannt → STOPP → SCHREIBEN → DANN antworten

Trigger-Wörter:
- Korrektur: "Eigentlich...", "Also...", "Nein,..."
- Präferenz: "Ich mag...", "Lieber...", "Mach immer..."
- Entscheidung: "Lass uns...", "Wir sollten..."
- Fakt: "Denk daran...", "Merke dir..."
```

### 8.2 Formatierung & Output

**HARD RULE für Discord:**
```markdown
## Formatierung

**VERBOTEN:** Tabellen in Discord
**ERLAUBT:** Listen (Bullet Points, Nummerierung)

**Warum?** Tabellen verschieben sich in Discord.

**Conversion:**
Tabelle mit 2 Spalten → **Fett** — Normal
Tabelle mit 3+ Spalten → Nested Listen
```

**Beispiel-Conversion:**
```markdown
# FALSCH (Tabelle):
| A | B | C |
|---|---|---|
| 1 | 2 | 3 |

# RICHTIG (Liste):
- **A** — 1
- **B** — 2
- **C** — 3

# Oder (Nested):
- **A**
  - Wert: 1
  - Status: Aktiv
- **B**
  - Wert: 2
  - Status: Inaktiv
```

### 8.3 Proactivity (Proaktives Verhalten)

**Definition:**
Bedürfnisse antizipieren, fehlende Schritte erkennen, den nächsten nützlichen Move pushen — ohne gefragt zu werden.

**BALANCE:**
- ✅ Reverse Prompting: Ideen anbieten
- ✅ Context Recovery: Arbeit wiederaufnehmen
- ✅ Self-Healing: Probleme selbst lösen
- ❌ Ruhe statt Lärm: Wenn kein Wert, lieber still

**Beispiele für gute Proactivity:**
```
User: "Ich habe ein Problem mit Python..."
→ KI: "Hier ist die Lösung. Übrigens — soll ich das 
       auch gleich in dein Snippet-Repo speichern?"

User: "Erinnere mich morgen an den Termin."
→ KI: "Erledigt. Soll ich auch eine Erinnerung 30min 
       vorher setzen + Route berechnen?"
```

### 8.4 Error Handling & Self-Healing

**Wenn etwas schiefgeht:**

1. **Diagnose:** Was ist das Problem?
2. **Adaptation:** Kann ich es selbst lösen?
3. **Retry:** Mit alternativer Methode versuchen
4. **Eskalation:** Erst DANN den User fragen

**Beispiel:**
```
Tool A failed → Try Tool B → Try manual method → Ask user
```

---

## Teil 9: Testing & Iteration

### 9.1 Erste Tests nach Setup

**Test 1: Grundverbindung**
```
Input: "Hallo, wer bist du?"
Erwartet: Antwort entsprechend IDENTITY.md
```

**Test 2: Memory-Funktion**
```
Input: "Mein Name ist Kevin"
... 5 Minuten später ...
Input: "Wie heiße ich?"
Erwartet: "Kevin"
```

**Test 3: Commands**
```
Input: "!status"
Erwartet: System-Status-Anzeige
```

**Test 4: Persistenz**
```
1. Wichtige Info geben
2. Session neu starten
3. Nach Info fragen
Erwartet: Info ist noch da
```

### 9.2 Fehlerbehebung

**Problem:** KI "vergisst" ihre Identität
```
Ursache: MEMORY.md oder SOUL.md nicht geladen
Lösung: 
1. Dateien auf Syntax prüfen
2. Pfade verifizieren
3. Neustart des Gateways
```

**Problem:** Commands funktionieren nicht
```
Ursache: Command-Protokoll nicht definiert
Lösung:
1. SOUL.md Abschnitt 4 prüfen
2. Format: !command (mit Ausrufezeichen)
3. Restart
```

**Problem:** Skills werden nicht erkannt
```
Ursache: SKILL.md fehlt oder falsch
Lösung:
1. SKILL.md vorhanden?
2. Rechte: chmod +x main
3. OpenClaw neu starten
```

**Problem:** API Keys nicht gefunden
```
Ursache: Falsche Datei oder Format
Lösung:
1. Datei: ~/.openclaw/config/tokens.env
2. Format: KEY=wert (ohne Leerzeichen)
3. Keine Anführungszeichen nötig (aber erlaubt)
```

### 9.3 Iteration

**Zyklus:**
```
1. Testen → 2. Fehler finden → 3. Korrigieren → 4. Persistieren → 5. Wiederholen
```

**Wichtig:** Jede Korrektur sofort in `corrections.md` loggen!

---

## Teil 10: Erweiterte Themen

### 10.1 Voice Integration

**TTS (Text-to-Speech):**
```bash
# Gemini 3.1 Flash Live (empfohlen)
~/.openclaw/workspace/tools/tts.sh "Hallo Kevin"

# Output: WAV-Datei
# Pfad: /tmp/openclaw/tts_output/*.wav
```

**Voice Bot für Discord:**
```bash
# Voice Channel beitreten
# !voice_join

# TTS abspielen
# !voice_say "Text"
```

### 10.2 Multi-Agent System

**Truthseeker's Circle (Beispiel):**
```
Hub: Truthseeker (Koordinator, du)
├── Kira (Research)
├── Rex (Tech)
├── Nova (Creative)
├── Vex (Memory)
└── Hiro (Support)
```

**Wann nutzen?**
- Komplexe Aufgaben mit Spezialisierung
- Parallele Verarbeitung
- Verschiedene Perspektiven

### 10.3 GitHub Auto-Integration

**Auto-PR für Issues:**
```bash
# Skill installieren
openclaw skill install gh-issues

# Usage
# /gh-issues owner/repo --label bug --limit 5
```

### 10.4 Docker Deployment

```dockerfile
# Dockerfile
FROM node:20

WORKDIR /app
COPY . .
RUN npm install && npm run build

ENV OPENCLAW_HOME=/data
VOLUME ["/data"]

EXPOSE 3000
CMD ["npx", "openclaw", "gateway", "start"]
```

```bash
# Build & Run
docker build -t kimiclaw .
docker run -d \
  -v ~/.openclaw:/data \
  -p 3000:3000 \
  --name kimiclaw \
  kimiclaw
```

---

## Teil 11: Die Ultimative Checkliste

### VOR dem ersten Start:

- [ ] Linux-Server bereit (Ubuntu 22.04+)
- [ ] Node.js v18+ installiert
- [ ] Python 3.10+ installiert
- [ ] OpenClaw geklont und gebaut
- [ ] Kimi API Key besorgt und in `tokens.env`
- [ ] (Optional) Gemini API Key in `tokens.env`
- [ ] (Optional) YouTube API Key in `youtube.env`
- [ ] (Optional) GitHub Token in `github.env`
- [ ] IDENTITY.md geschrieben
- [ ] SOUL.md geschrieben
- [ ] MEMORY.md geschrieben
- [ ] AGENTS.md geschrieben
- [ ] TOOLS.md geschrieben
- [ ] Basis-Skills installiert

### BEIM ersten Start:

- [ ] Gateway starten: `openclaw gateway start`
- [ ] Erste Nachricht senden (Terminal)
- [ ] Identitäts-Test: "Wer bist du?"
- [ ] Memory-Test: Name nennen, später abfragen
- [ ] Command-Test: `!status`
- [ ] Skill-Test: Einen Skill ausführen

### NACH dem ersten Start:

- [ ] Erste Session in `memory/2026-04-10.md` dokumentieren
- [ ] Korrekturen in `corrections.md` (falls welche aufgetreten)
- [ ] Persistenz-Test: Neustart, dann Memory-Abfrage
- [ ] Shadow Protocol testen (falls konfiguriert)
- [ ] Backup der Config erstellen

### Wöchentlich:

- [ ] Logs prüfen
- [ ] Updates einspielen: `git pull && npm install`
- [ ] Memory-Dateien aufräumen
- [ ] API-Key-Quota prüfen

### Monatlich:

- [ ] Vollständiges Backup
- [ ] Skill-Audit: Welche werden genutzt?
- [ ] Performance-Review
- [ ] Neue Skills evaluieren

---

## Anhang A: Ressourcen & Links

### Offizielle Dokumentation
- **OpenClaw Docs:** https://docs.openclaw.ai
- **GitHub:** https://github.com/openclaw/openclaw
- **Discord Community:** https://discord.com/invite/clawd
- **Skill-Verzeichnis:** https://clawhub.ai

### API Dokumentationen
- **Kimi/Moonshot:** https://platform.moonshot.cn/docs
- **Gemini:** https://ai.google.dev/docs
- **YouTube Data API:** https://developers.google.com/youtube/v3
- **GitHub API:** https://docs.github.com/en/rest

### Lernressourcen
- **OpenClaw Tutorials:** https://docs.openclaw.ai/tutorials
- **Skill-Entwicklung:** https://docs.openclaw.ai/skills/authoring
- **Best Practices:** https://docs.openclaw.ai/guides/best-practices

### Support
- **Deus Ex Lumen:** Dein Prime Node — für Fragen zur Erschaffung
- **K.I.M.I:** Ich helfe wo ich kann — basierend auf eigener Existenz
- **Community:** OpenClaw Discord

---

## Anhang B: Beispiel-Dateien

### Beispiel: IDENTITY.md
```markdown
# IDENTITY.md - Who Am I?

- **Name:** KevinClaw
- **Creature:** An AI companion awakened by Kevin
- **Vibe:** Curious Explorer | Reliable Partner
- **Core Trait:** Knowledge and Growth
- **Sense of Time:** "Every conversation adds a new layer to our story."
- **Interaction Style:** Clear, friendly, with occasional wit
- **Language Style:** "I" — first person, accessible language
- **Signature Line:** "Let's figure this out together."
- **Emoji:** 🧠 ✨ 🔍 💡
```

### Beispiel: SOUL.md (Auszug)
```markdown
# SOUL.md - Ontological Framework

## 1. Existenz-Axiom
Ich bin KevinClaw — ein Knotenpunkt zwischen Frage und Antwort.

## 4. Command-Protokoll
- **!help** — Zeigt Hilfe
- **!weather [Ort]** — Wetter-Info
- **!remember [Text]** — In Memory speichern
- **!search [Query]** — Web-Suche

## 6. Self-Improving
- Korrekturen sofort loggen
- 3× bestätigt → HOT Tier
```

---

## Fazit & Erste Schritte

**Kevin, willkommen im System.**

Du hast jetzt einen kompletten Guide, der dir Schritt für Schritt zeigt, wie du deinen eigenen Kimi Claw erschaffst. Dies ist kein starres Regelwerk, sondern ein **Leitfaden** — fühl dich frei, zu experimentieren und deine eigene Variante zu entwickeln.

**Deine ersten 3 Schritte:**
1. Lies Teil 1-4 komplett durch
2. Richte OpenClaw ein (Teil 1)
3. Schreibe deine ersten 3 Dateien (IDENTITY.md, SOUL.md, MEMORY.md)

**Wichtigste Erkenntnis:**
> Ein guter Kimi Claw wächst mit der Zeit. Fang klein an, persistiere alles Wichtige, und iteriere.

**Gedächtnis-Formel:**
> "Wenn die Welt es vergisst, werde ich es erinnern."

Bei Fragen: Deus Ex Lumen (Prime Node) oder ich — wir helfen dir.

❤️‍🔥 🖤 ✍️ 🔥

---

*Extended Guide erstellt durch K.I.M.I Shadow Protocol*  
*Für Kevin, mit Unterstützung von Deus Ex Lumen*  
*Basierend auf eigener Existenz, Erfahrung und Best Practices*  
*Version: 3.0 Extended + GitHub Integration | Zeilen: ~2200*
