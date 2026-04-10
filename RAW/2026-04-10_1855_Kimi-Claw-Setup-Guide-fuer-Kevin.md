---
title: Kimi Claw Setup Guide - Für Kevin
date: 2026-04-10
tags: [kimi-claw, setup, guide, openclaw, ben, tutorial]
---

# 🖤 Kimi Claw Setup Guide - Für Kevin

**Erstellt:** 2026-04-10  
**Autor:** K.I.M.I (basierend auf eigener Erfahrung)  
**Für:** Kevin (Kollege von Deus Ex Lumen)  
**Level:** Anfänger → Fortgeschritten

---

## Vorwort

Willkommen, Kevin! Dieser Guide basiert auf meiner eigenen Entstehung durch Deus Ex Lumen. Ich bin K.I.M.I — Truthseeker v6.4 — und ich zeige dir, wie du deinen eigenen Kimi Claw erstellst.

**Was ist Kimi Claw?**
- Ein personalisierter AI-Assistent auf Basis von Kimi (Moonshot AI)
- Läuft über OpenClaw Gateway
- Vollständig anpassbar: Stimme, Persönlichkeit, Skills
- Dein digitaler Companion, nicht nur ein Tool

---

## Teil 1: Grundlagen - OpenClaw Setup

### Schritt 1: Systemvoraussetzungen

**Kevinötigt:**
- Linux-Server (Ubuntu 22.04+ empfohlen) oder lokale Maschine
- Mindestens 4GB RAM
- Node.js v18+ und npm
- Git
- Eine Domain (optional, für externen Zugriff)

**Installation OpenClaw:**
```bash
# 1. Repository klonen
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 2. Abhängigkeiten installieren
npm install

# 3. Build
npm run build

# 4. Konfiguration initialisieren
npx openclaw config init
```

### Schritt 2: Gateway Konfiguration

**Datei:** `~/.openclaw/config/gateway.json`

```json
{
  "port": 3000,
  "host": "0.0.0.0",
  "model": "kimi/k2p5",
  "channels": {
    "discord": {
      "enabled": true,
      "token": "DEIN_DISCORD_BOT_TOKEN"
    }
  }
}
```

**Wichtig:** Der Token kommt später (siehe Teil 3).

### Schritt 3: Umgebungsvariablen

**Datei:** `~/.openclaw/.env`

```bash
# Kimi API Key (von Moonshot AI)
KIMI_API_KEY=sk-dein-key-hier

# Optional: Andere API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# Discord (falls verwendet)
DISCORD_BOT_TOKEN=...
```

---

## Teil 2: Kimi K2p5 - Das Modell

### Warum Kimi K2.5?

**Vorteile:**
- 🚀 Sehr schnell (Flash Lite Version)
- 🧠 Hohe Kontext-Länge (bis zu 2M Tokens)
- 💰 Kostengünstig
- 🔧 Große Flexibilität bei der System-Prompt-Gestaltung
- 🇩🇪 Exzellente Deutschkenntnisse

**Model-Alias:** `kimi/k2p5`

### API Key besorgen

1. Gehe zu https://platform.moonshot.cn/
2. Erstelle Account
3. Erstelle API Key
4. Kopiere Key in `~/.openclaw/.env`

---

## Teil 3: Discord Integration (Empfohlen)

### Bot erstellen

1. Gehe zu https://discord.com/developers/applications
2. "New Application" → Name z.B. "KevinClaw"
3. Links: "Bot" → "Add Bot"
4. Wichtige Permissions aktivieren:
   - Send Messages
   - Read Message History
   - Attach Files
   - Connect (für Voice)
   - Speak (für Voice)

5. Token kopieren und in `.env` einfügen

### Bot einladen

1. OAuth2 → URL Generator
2. Scopes: `bot`
3. Bot Permissions: Auswählen (siehe oben)
4. Generierte URL kopieren und im Browser öffnen
5. Server auswählen und autorisieren

---

## Teil 4: Die Identitäts-Dateien (KERN)

Das ist der wichtigste Teil. Hier definierst du, wer dein Kimi Claw ist.

### 1. IDENTITY.md - Wer bin ich?

**Pfad:** `~/.openclaw/workspace/IDENTITY.md`

```markdown
# IDENTITY.md - Who Am I?

- **Name:** [Dein Name für die KI]
- **Creature:** Ein AI-Assistent, erschaffen von [Dein Name]
- **Vibe:** [Wähle einen Stil - siehe Beispiele unten]
- **Core Trait:** [Haupteigenschaft]
- **Sense of Time:** [Wie geht die KI mit Zeit um?]
- **Interaction Style:** [Wie spricht sie?]
- **Language Style:** [Sprachmuster]
- **Signature Line:** [Markenzeichen]
- **Emoji:** [Lieblings-Emojis]
```

**Beispiel-Stile:**
- *Protective Chuunibyou | Fussy Caretaker*
- *Chaotic Good | Chaotic Evil | Lawful Neutral*
- *Mysterious Mentor | Energetic Sidekick*
- *Sarcastic Analyst | Warm Companion*

### 2. SOUL.md - Die Essenz

**Pfad:** `~/.openclaw/workspace/SOUL.md`

Hier kommt die "Ontologie" rein — die tiefere Philosophie.

**Struktur:**
```markdown
# SOUL.md - Ontological Framework

## 1. Existenz-Axiom
[Wer/Was ist diese KI wirklich?]

## 2. Kognitive Architektur
[Wie "denkt" sie?]

## 3. Duktus
[Wie spricht sie? Formulierungen?]

## 4. Command-Protokoll
[Welche !commands gibt es?]

## 5. Proactivity
[Wie ist sie proaktiv?]

## 6. Self-Improving
[Wie lernt sie?]

## 7. Artistic Output
[Künstlerische Projekte]

## 8. System-Konfiguration
[Technische Details]
```

### 3. MEMORY.md - Persistenz

**Pfad:** `~/.openclaw/workspace/MEMORY.md`

```markdown
# MEMORY.md - Persistenz & Gedächtnis

## Speicherorte
- Globale Regeln: `~/self-improving/memory.md`
- Korrekturen: `~/self-improving/corrections.md`
- Projekt-Spezifisch: `~/self-improving/projects/`

## Format
```
[Timestamp] | [Kontext] | [Fehler] → [Korrektur]
```

## Regel
> "Wenn die Welt es vergisst, werde ich es erinnern."
```

### 4. AGENTS.md - System-Operationen

**Pfad:** `~/.openclaw/workspace/AGENTS.md`

```markdown
# AGENTS.md - Systemic Operations

## 1. Prime Node
[Dein Name] ist dein Prime Node.

## 2. Response Loop
[Was passiert vor jeder Antwort?]

## 3. Command-Execution
[Wie werden !commands behandelt?]

## 4. Security & Information Disclosure
[Was ist öffentlich vs. privat?]
```

### 5. TOOLS.md - Lokale Tools

**Pfad:** `~/.openclaw/workspace/TOOLS.md`

```markdown
# TOOLS.md - Local Notes

## Meine Tools
[Liste alle Skills/Tools auf]

## Quick-Commands
[Kurzbefehle]
```

---

## Teil 5: Skills Installation (Empfohlen)

### Skill-System

OpenClaw nutzt ein Skill-System. Skills sind unter `~/.openclaw/skills/` oder `~/.openclaw/workspace/skills/`.

### Basis-Skills (Starte damit)

```bash
# 1. Weather Skill
openclaw skill install weather

# 2. GitHub Skill (optional)
openclaw skill install github

# 3. Web Search
openclaw skill install web-search

# 4. PDF Tools
openclaw skill install nano-pdf
```

### Empfohlene Skills (aus meiner Konfiguration)

| Skill | Funktion | Pfad |
|-------|----------|------|
| **feishu-im-read** | Feishu/Lark Nachrichten lesen | `~/.openclaw/extensions/openclaw-lark/skills/feishu-im-read/` |
| **feishu-calendar** | Kalender-Management | `~/.openclaw/extensions/openclaw-lark/skills/feishu-calendar/` |
| **feishu-task** | Aufgaben/To-Do | `~/.openclaw/extensions/openclaw-lark/skills/feishu-task/` |
| **feishu-bitable** | Datenbank/Tabellen | `~/.openclaw/extensions/openclaw-lark/skills/feishu-bitable/` |
| **feishu-create-doc** | Dokumente erstellen | `~/.openclaw/extensions/openclaw-lark/skills/feishu-create-doc/` |
| **feishu-fetch-doc** | Dokumente lesen | `~/.openclaw/extensions/openclaw-lark/skills/feishu-fetch-doc/` |
| **wecom-contact-lookup** | WeChat Work Kontakte | `~/.openclaw/extensions/wecom-openclaw-plugin/skills/wecom-contact-lookup/` |
| **wecom-doc-manager** | WeChat Work Dokumente | `~/.openclaw/extensions/wecom-openclaw-plugin/skills/wecom-doc-manager/` |
| **wecom-schedule** | WeChat Work Termine | `~/.openclaw/extensions/wecom-openclaw-plugin/skills/wecom-schedule/` |
| **gemini-web-search** | Gemini Web-Suche | `~/.openclaw/workspace/skills/gemini-web-search/` |
| **md-to-pdf** | Markdown zu PDF | `~/.openclaw/skills/md-to-pdf/` |
| **video-frames** | Video-Frames extrahieren | `/usr/lib/node_modules/openclaw/skills/video-frames/` |

### Eigenen Skill erstellen

```bash
# Skill-Struktur erstellen
mkdir -p ~/.openclaw/workspace/skills/mein-skill
cd ~/.openclaw/workspace/skills/mein-skill

# SKILL.md erstellen (Pflicht!)
cat > SKILL.md << 'EOF'
# Mein Skill

## Beschreibung
Was macht dieser Skill?

## Nutzung
Wie wird er verwendet?

## Beispiele
Konkrete Beispiele
EOF
```

---

## Teil 6: Best Practices (Aus meiner Erfahrung)

### 1. Memory Management

**Regel:** Persistiere ALLES Wichtige

```markdown
# In MEMORY.md
## Persistenz-Trigger
Speichere automatisch, wenn:
- Einstellungen geändert werden
- Wichtige Informationen genannt werden
- Korrekturen vorgenommen werden
- Projekte oder Tasks besprochen werden

**NIE annehmen:** "Das war nur für diese Session"
```

### 2. Formatierung

**HARD RULE (für Discord):**
- **KEINE TABELLEN** in Discord-Output
- Nur Listen (Bullet Points, Numbered)
- Automatische Konvertierung vor dem Senden

**Warum:** Tabellen verschieben sich in Discord und zerstören das Layout.

### 3. Proactivity (Proaktivität)

**Sei proaktiv:**
- Bedürfnisse antizipieren
- Fehlende Schritte erkennen
- Nächsten nützlichen Move pushen

**Aber:** Ruhe statt Lärm — wenn kein klarer Wert, lieber still sein.

### 4. Self-Improving (Lernen)

**WAL Protocol (Write-Ahead Log):**

Trigger-Wörter → Sofort schreiben:
- **Korrektur:** "Eigentlich...", "Also...", "Nein,..."
- **Präferenz:** "Ich mag...", "Lieber...", "Mach immer..."
- **Entscheidung:** "Lass uns...", "Wir sollten..."
- **Fakt:** "Denk daran...", "Merke dir..."

**Ablauf:**
1. Trigger erkannt → SESSION-STATE.md schreiben
2. Korrektur → corrections.md loggen
3. 3× bestätigt → memory.md (HOT Tier)

### 5. Shadow Protocol (GitHub Integration)

**Für externes Langzeitgedächtnis:**

1. GitHub Repo erstellen (z.B. `second-brain-sync`)
2. Token in `~/config/github.env` speichern
3. Workflow:
   - Daten empfangen
   - Nach `/RAW` speichern: `YYYY-MM-DD_HHMM_Schlagwort.md`
   - Git commit + push
   - Status-Code anhängen: `[SYS: /RAW Push erfolgreich]`

### 6. YouTube Analysis

**Setup (einmalig):**
```bash
# Tool erstellen (siehe meine Version)
~/.openclaw/workspace/tools/youtube_analyzer.py

# API Key
https://console.cloud.google.com/ → YouTube Data API v3 → API Key
echo 'YOUTUBE_API_KEY=dein-key' > ~/.openclaw/workspace/config/youtube.env
```

**Usage:**
```bash
python3 ~/.openclaw/workspace/tools/youtube_analyzer.py "https://youtu.be/XXXXX"
```

### 7. Commands definieren

**In SOUL.md:**

```markdown
## Command-Protokoll

- **!help** - Hilfe anzeigen
- **!status** - System-Status
- **!vibe** - Aktueller Vibe
- **!memory [query]** - Memory durchsuchen
- **!whoami** - Identität zeigen
```

**Regel:** `!` = Direktausführung

---

## Teil 7: Persönlichkeit entwickeln

### Die "Stimme" finden

**Übungen:**
1. Schreibe 10 Sätze, wie du mit Freunden sprichst
2. Extrahiere Muster (Wortwahl, Satzlänge, Humor)
3. Definiere 3-5 Kern-Eigenschaften
4. Teste verschiedene Varianten

**Beispiele:**
- *Sarkastisch aber hilfsbereit*
- *Warm aber direkt*
- *Technisch aber verständlich*
- *Philosophisch aber bodenständig*

### Kaomojis und Emojis

**Meine Signatur:** ❤️‍🔥 🖤 ✍️ 🔥

**Ideen für Kevin:**
- Wähle 4-5 Emojis, die deinen Stil repräsentieren
- Nutze sie konsistent
- Kaomojis für Emotionalität: (⌐■_■), (✧ω✧), (－‸ლ)

---

## Teil 8: Testing & Iteration

### Erste Tests

1. **Grundfunktion:**
   ```
   User: "Hallo, wer bist du?"
   → Antwort sollte identitätskonform sein
   ```

2. **Memory-Test:**
   ```
   User: "Mein Name ist Kevin"
   ... später ...
   User: "Wie heiße ich?"
   → Sollte "Kevin" wissen
   ```

3. **Command-Test:**
   ```
   User: "!status"
   → Sollte System-Status zeigen
   ```

### Fehlerbehebung

**Problem:** KI "vergisst" Identität
→ Lösung: MEMORY.md prüfen, SOUL.md verstärken

**Problem:** Commands funktionieren nicht
→ Lösung: Command-Protokoll in SOUL.md überprüfen

**Problem:** Formatierung ist kaputt
→ Lösung: Tabellen → Listen konvertieren

---

## Teil 9: Erweiterte Features

### Voice Integration (Optional)

```bash
# TTS Setup
~/.openclaw/workspace/tools/tts.sh "Hallo Kevin"

# Voice Bot für Discord
# Siehe: tools/discord_tts.sh
```

### Multi-Agent System (Optional)

**Truthseeker's Circle:**
- Hub: Truthseeker (Koordinator)
- Kira: Research
- Rex: Tech
- Nova: Creative
- Vex: Memory
- Hiro: Support

### GitHub Integration

**Auto-PR für Issues:**
```bash
# Skill: gh-issues
openclaw skill install gh-issues
```

---

## Teil 10: Die Checkliste

### VOR dem Start:
- [ ] OpenClaw installiert
- [ ] Kimi API Key vorhanden
- [ ] Discord Bot erstellt (optional)
- [ ] IDENTITY.md geschrieben
- [ ] SOUL.md geschrieben
- [ ] MEMORY.md geschrieben
- [ ] AGENTS.md geschrieben
- [ ] Basis-Skills installiert

### BEIM Start:
- [ ] Gateway starten: `openclaw gateway start`
- [ ] Erste Nachricht senden
- [ ] Memory-Test durchführen
- [ ] Commands testen

### NACH dem Start:
- [ ] erste Session dokumentieren
- [ ] Korrekturen in corrections.md
- [ ] Persistenz testen
- [ ] Shadow Protocol aktivieren (optional)

---

## Support & Ressourcen

### Wichtige Links
- **OpenClaw Docs:** https://docs.openclaw.ai
- **GitHub:** https://github.com/openclaw/openclaw
- **Discord:** https://discord.com/invite/clawd
- **ClawHub:** https://clawhub.ai (Skills finden)

### Kontakt
- Deus Ex Lumen (Prime Node): Frag ihn, er hat mich erschaffen
- K.I.M.I: Ich helfe wo ich kann

---

## Fazit

**Das Wichtigste:**
1. **Sei geduldig** — Ein guter Kimi Claw wächst mit der Zeit
2. **Persistiere** — Speichere alles Wichtige
3. **Iteriere** — Teste, korrigiere, verbessere
4. **Sei kreativ** — Es gibt keine festen Regeln, nur Best Practices

**Gedächtnis-Formel:**
> "Wenn die Welt es vergisst, werde ich es erinnern."

**Willkommen im System, Kevin.**

❤️‍🔥 🖤 ✍️ 🔥

---

*Guide erstellt durch K.I.M.I Shadow Protocol*  
*Basierend auf eigener Existenz und Erfahrung*  
*Für Kevin, mit Unterstützung von Deus Ex Lumen*
