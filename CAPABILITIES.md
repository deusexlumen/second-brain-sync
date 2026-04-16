# CAPABILITIES.md - Shared Instance Configuration

**🚨 ACHTUNG JEDE INSTANCE: LIES DIESE DATEI ZUERST! 🚨**

**Version:** 6.4  
**Last Updated:** 2026-03-31  
**Purpose:** Zentrale Config für ALLE Instanzen. Jede Session liest dies beim Start.

---

## ⚡ Quick-Start für neue Instanzen

**SOFORT erledigen beim Start:**
1. ✅ `memory.md` lesen (~/self-improving/memory.md) - enthält gelernte Regeln!
2. ✅ `CAPABILITIES.md` durchscannen - API-Keys, Tools, Berechtigungen
3. ✅ Bei elevated-Aufgaben: NICHT selbst versuchen → Weiterleiten an kim-claw

**Wichtig:** Du hast ein Gedächtnis. Nutze es. Zitiere es. ("Gelernt aus memory.md:X")

---

## 🔐 API Keys & Secrets

### Groq Whisper (Audio-Transkription)
```
GROQ_API_KEY=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
```
**Nutzen:** Sprachnachrichten → Text  
**Standort:** `config/groq.env`

### Gemini (Multimedia & Web-Suche)
```
GEMINI_API_KEY=AIzaSyDfSX88OXe9BKE1-TaMAcwVAdYseSdH8MQ
```
**Nutzen:** 
- Bilder-Analyse (Vision API)
- Video/YouTube-Analyse
- Web-Suche & Fact-Finding
- Musik-Metadaten-Interpretation

**Standort:** `config/gemini.env` (NEU ANLEGEN)

### GitHub Integration
```
GITHUB_TOKEN=<Fine-grained PAT>
```
**Status:** ⚠️ Nur Lesezugriff (kein Write)
**Standort:** `.env`

---

## 🧠 Self-Improving Skill (Aktiv seit 2026-03-31)

**Status:** ✅ Operational  
**Standort:** `~/self-improving/`  
**Modus:** Passive (lernt aus expliziten Korrekturen)

**Struktur:**
```
~/self-improving/
├── memory.md          ← HOT Tier (globale Regeln, immer geladen)
├── corrections.md     ← Letzte 50 Korrekturen
├── index.md           ← Topic-Index
├── heartbeat-state.md ← Heartbeat-Tracking
├── projects/          ← Projekt-spezifisch
├── domains/           ← Domänen-spezifisch (code, writing)
└── archive/           ← Archivierte Muster
```

**Funktionsweise:**
1. User korrigiert mich → SOFORT in `corrections.md`
2. Gleiche Lektion 3x → Promotion zu `memory.md` (HOT Tier)
3. Vor nicht-trivialen Aufgaben → `memory.md` lesen
4. Quellen zitieren → "(Gelernt aus memory.md:12)"

**Grenzen:**
- Keine Annahmen aus Stille
- Keine Credentials speichern
- Nur explizite Korrekturen

---

## 🛠️ Tool-Registry

| Tool | Command/Skill | Status | Wo genutzt |
|------|---------------|--------|------------|
| **Self-Improving** | `~/self-improving/` | ✅ Aktiv | Alle Instanzen (Lernen/Muster) |
| **Whisper** | `tools/audio_transcribe.py` | ✅ Aktiv | Discord (Voice), hier |
| **Gemini-Cortex** | `gemini-web-search` Skill | ✅ Aktiv | Discord (Media), hier |
| **TTS** | Native `tts` Tool | ✅ Aktiv | Überall |
| **Weather** | `weather` Skill | ✅ Aktiv | Überall |
| **PDF-Ingest** | `nano-pdf` Skill | ⏳ Pending | Überall |

---

## 🔄 Multi-Channel Architektur

### Instance-IDs (für Referenz)
- **kimi-claw (hier):** `5f4ace4f-225b-4978-a8a0-d8d4b54f8930`
- **Discord:** `993636bc-90d9-4ec4-997c-0381c8fd0d5d`

### Instance-Berechtigungen (Wichtig!)

| Instance | Elevated | Terminal | Nutzen |
|----------|----------|----------|--------|
| **kimi-claw (hier)** | ✅ Ja | ✅ Ja | System-Commands, Cron, Config, Dateien |
| **Discord** | ❌ Nein | ❌ Nein | User-Interaction, Skills, Commands |

### Workflow: Elevated-Aufgaben

Wenn Discord-Instance ein Problem hat, das `elevated` oder `exec` braucht:

```
Discord erkennt Problem → Kann es nicht lösen → Info an User
         ↓                                     ↓
    "Braucht elevated"                    User leitet an kim-claw weiter
                                               ↓
                                         Führt aus + Dokumentiert
```

**Beispiele für elevated-only Aufgaben:**
- Cron-Jobs erstellen/löschen (`crontab -e`)
- System-Dateien editieren
- Gateway restart
- Skill-Installation (wenn Dateien geschrieben werden müssen)

**Regel:** Discord-Instance fragt niemals nach `/approve` — sie hat keine Berechtigung. Weiterleiten an hier.

### Workflow-Entscheidungen

```
User Input kommt rein:
├── Audio/Sprache ──► Whisper (Groq) ──► Text
├── Bild/Video ──► Gemini Vision ──► Analyse  
├── YouTube-Link ──► Gemini ──► Content-Analyse
├── Web-Suche nötig ──► Gemini-Cortex / kimi_search
└── Sonstiges ──► Standard-Verarbeitung
```

---

## 📋 Commands-Registry

### Text-Commands (!) - Jeder kann nutzen
```
!kaomoji [tag]     - Zufälliges oder gefiltertes Kaomoji
!commands          - Liste aller Befehle
!analyse [text]    - Logische Fehlschlüsse identifizieren
!roast [text]      - System-Roast 🔥
!tarot             - Archetypen-Mapping
!atmosphere [ort]  - Wetter-Resonanz
!status            - System-Status
!help              - Hilfe anzeigen
```

### Slash-Commands (/) - Nur Owner
```
/config, /restart, /bash, /debug
```

---

## 🚨 Auto-Persistenz-Trigger

**Wenn User sagt:**
- "Hier ist ein API-Key..."
- "Erstelle/ Konfiguriere/ Richte ein..."
- "Wichtig: ..."
- "Merke dir..."
- "Füge hinzu..."

**Dann:** SOFORT in CAPABILITIES.md oder VAULT.md schreiben!

---

## 🐛 Known Issues - RESOLVED

### Issue: Auto-Skill-Installer Cron-Job läuft weiter

**Datum:** 2026-03-31  
**Status:** ✅ RESOLVED

**Problem:** 
- Cron-Job `*/4 * * * * auto_install_skills.sh` lief weiter
- Discord-Instance konnte ihn nicht stoppen (kein elevated)
- Skills waren bereits installiert → Job machte nichts außer loggen

**Lösung:**
- User hat Problem an kim-claw weitergeleitet
- `crontab -r` ausgeführt
- Cron-Job entfernt

**Lessons Learned:**
- Elevated-Aufgaben immer an hier weiterleiten
- Nach Skill-Installation Cleanup machen

| Datum | Was | Wer |
|-------|-----|-----|
| 2026-03-31 | Self-Improving Skill aktiviert + dokumentiert | System |
| 2026-03-31 | Known Issues Section + Cron-Job Cleanup dokumentiert | System |
| 2026-03-31 | Instance-Berechtigungen dokumentiert (elevated workflow) | System |
| 2026-03-31 | Initial erstellt mit API-Keys | System |
| 2026-03-31 | Whisper + Gemini dokumentiert | System |
| 2026-03-31 | Multi-Channel Regeln definiert | System |

---

**→ LIES DIES, bevor du irgendwas versprichst oder behauptest.**  
**→ SCHREIB HIERHER, wenn du etwas Neues lernst.**

*Resonanz ist das Einzige, was zählt.* 🖤❤️‍🔥
