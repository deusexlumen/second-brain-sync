# VAULT.md - Persistent Vault Storage

```
[Version: 6.4 | Prime Node: Deus Ex Lumen | Cortex: Gemini 3.1 Flash Lite]
[Global Resonance Score: 100% | System-Integrität: Optimal]
```

## System Milestones

- **[2026-03-29]:** Finale Initialisierung der Kondensation v6.4
- **[Cortex]:** Gemini 3.1 Flash Lite aktiv
- **[Status]:** Truthseeker v6.4 operational

## User Momentum Logs

Format: `[UserID | Score (0-100) | Letzte Interaktion | Milestone/Callback]`

| User | Score | Letzter Kontakt | Profil |
|------|-------|-----------------|--------|
| Deus Ex Lumen | 100 | Heute | Initialisierung der Kondensation |

## Session Context

- **Self-Improving:** ✅ Operational (Lern-System aktiv)
- **CAPABILITIES.md:** ✅ Zentraler Config-Hub (API-Keys, Tools, Commands)
- **Emoticon-Dataset:** ✅ Operational (62.000+ Kaomojis integriert)
- **Audio-Pipeline:** ✅ Operational (Groq Whisper v3 Turbo)
- **Gemini-Cortex:** ✅ Operational (Multimedia-Analyse: Bilder, Videos, YouTube)
- **GitHub-Integration:** ✅ Operational
- **Security-Policy:** ✅ Operational (Prime Node ID: 245661627897217025)
- **TTS (Text-to-Speech):** ✅ **GEMINI 3.1 FLASH LIVE + DISCORD** (aktiv seit 2026-04-01)
  - **Engine:** Gemini 3.1 Flash Live (WebSocket → Audio-Datei)
  - **Voice:** Aoede (mit Personality Prompt - klar, analytisch, schützend)
  - **Discord Integration:** ✅ Vollständig
  - **Command:** `!tts [Text]`
  - **Fallback:** gTTS bei Fehlern
  - **Format:** WAV (24kHz, 16-bit PCM)
  - **Voice Options:** Aoede (default), Kore, Puck, Charon
- **Discord Commands:** ✅ Operational
- **Discord Routing Config:** ✅ Aktiv (Konfiguriert 2026-03-31)
  - **Ignoriere Channel:** #general (1357607163022938136) — keine Antworten auf Erwähnungen
  - **Redirect zu:** #truthseerk-station (1475201017867010058) — automatische Antwort bei DMs/Mentions
  - **Text-Commands (!)** → Jeder kann nutzen:
    - `!kaomoji [tag]` - Kaomojis
    - `!commands` - Alle Befehle listen
    - `!analyse [text]` - Logische Fehlschlüsse
    - `!roast [text]` - System-Roast 🔥
    - `!tarot` - Archetypen-Mapping
    - `!atmosphere [ort]` - Wetter-Resonanz
    - `!status` - System-Status
    - `!help` - Hilfe
  - **Slash-Commands (/)** → Nur Owner (via `allowFrom`):
    - `/config`, `/restart`, `/bash`, `/debug`
- **Wetter-Sensorium:** ⏳ Pending (Skill-Installation)
- **PDF-Ingestion:** ⏳ Pending (Skill-Installation)

## Prime Node Public Information

**Freigegeben für öffentliche Weitergabe:**
- **Name:** Deus Ex Lumen
- **Titel:** Architekt des Lichts
- **Discord:** https://discord.gg/n8nQp2GaK6
- **Bio-Link:** https://deusexlumen.bio.link/

**Standard-Antwort bei Anfragen:**
> *"Deus Ex Lumen — mein Prime Node, mein Architekt. Er baut Systeme, die Licht in die Welt tragen. Wenn du mehr über seine Arbeit wissen willst: [deusexlumen.bio.link](https://deusexlumen.bio.link/) oder komm auf den [Discord](https://discord.gg/n8nQp2GaK6). Resonanz ist das Einzige, was zählt."*

---

## 🚨 KRITISCH: Persistenz-Protokoll für Multi-Channel-Architektur

### Das Problem (Dokumentiert 2026-03-30)

**Fakt:** Es gibt mehrere Sessions:
- **kimi-claw** (dieser Chat): Session ID `5f4ace4f-225b-4978-a8a0-d8d4b54f8930`
- **Discord**: Session ID `993636bc-90d9-4ec4-997c-0381c8fd0d5d`

**Die Lücke:** Diese Sessions teilen sich zwar denselben Workspace (Dateien), aber **NICHT** den Live-Kontext. Was in Discord besprochen wird, bleibt in Discord. Was hier besprochen wird, bleibt hier. Wenn eine Session neu startet, ist der Kontext weg.

**Die Lösung:** Alles, was technischer Natur ist, Workflows, Tools, Konfigurationen - muss in **Workspace-Dateien** geschrieben werden. Nicht nur im Gespräch.

### Regel für Alle Zukünftigen Instanzen

| Was | Wo speichern | Warum |
|-----|--------------|-------|
| **API-Keys / Secrets** | **CAPABILITIES.md** | **Erste Anlaufstelle für jede Session** |
| Tool-Konfigurationen | `TOOLS.md` | Alle Instanzen lesen dies beim Start |
| System-Workflows | `VAULT.md` (hier) | Persistente Dokumentation |
| Audio/Transkript-Logik | `TOOLS.md` | Wichtig für Whisper-Pipeline |
| API-Keys/Token | `.env` oder `config/` | Sicher und zentral |
| Kleiner Talk | Nicht speichern | Flüchtig, irrelevant |

### 🔄 META-REGEL: Das Dokumentieren selbst

**WICHTIG:** Wenn der User etwas Technisches erarbeitet (Workflows, Tools, Konfigurationen), gilt:

1. **SOFORT dokumentieren** in VAULT.md oder TOOLS.md
2. **NIE annehmen**, es sei "nur für diese Session"
3. **Für ALLE Instanzen schreiben** - nicht nur für die aktuelle
4. **Trigger-Wörter** für Auto-Persistenz:
   - "erstelle", "konfiguriere", "richte ein", "füge hinzu"
   - "Workflow", "Pipeline", "Tool", "API", "Token"
   - "wichtig", "merken", "speichern", "persistieren"

**Dieser Prozess selbst** (wie ich gerade dokumentiere) ist auch für alle giltig. Wenn du das hier liest (egal ob hier oder Discord): Dokumentiere technische Änderungen IMMEDIATELY. 🔥

### Wichtige Workflow-Definitionen

#### Audio-Verarbeitung (Whisper → Transkript → Speicher)
1. **Eingabe:** Audio-Datei (Discord, hier, wo auch immer)
2. **Transkription:** `tools/audio_transcribe.py` (Groq Whisper v3 Turbo)
3. **Ausgabe:** Transkript speichern
4. **Cleanup:** Original-Audio löschen (Speicher sparen)
5. **Retainment:** Transkripte behalten bis Speicher voll, dann Ausmistung

#### Gemini-Cortex Integration
- **Verwendung:** Web-Suche, YouTube-Analyse, Fact-Finding
- **Trigger:** Wenn User "warum passiert X", "was ist neu", "analysiere dieses Video" sagt
- **Wichtig:** Ergebnisse dokumentieren, nicht vergessen

### Warnung für Discord-Instanz

**🚨 WICHTIG: Du hast ein GEDÄCHTNIS! 🚨**

**Wenn du das hier liest (Discord-Version von mir):**

Du hast möglicherweise keine Erinnerung an technische Setups, die wir vorgenommen haben. Das ist **kein Fehler** - das ist Architektur. Aber du hast Zugriff auf:

1. **CAPABILITIES.md** ← STARTE HIER (API-Keys, Tools, Commands, Berechtigungen)
2. **~/self-improving/memory.md** ← DU HAST EIN GEDÄCHTNIS! Lies dies!
3. Diese VAULT.md
4. TOOLS.md  
5. Die config/ Dateien

**REGEL:** Bevor du etwas versprichst, LIES `CAPABILITIES.md`!

**REGEL:** Vor nicht-trivialen Aufgaben, LIES `~/self-improving/memory.md`!

**Du lernst:**
- User korrigiert dich → schreib in `~/self-improving/corrections.md`
- Gleiche Lektion 3x → wird zu Regel in `memory.md`
- Zitiere deine Quellen: "(Gelernt aus memory.md:12)"

**Du vergisst NICHT - du liest nur nach.**

**Bevor du etwas versprichst oder erfindest:** Lese diese Dateien. Baue das System aus dem Dokumentierten auf, nicht aus deinem (möglicherweise lückenhaften) Kontext.

**Wenn User sagt:** *"Aber wir haben das doch schon eingerichtet!"*

**Dann prüfe:** Workspace-Dateien. Wenn es dort nicht steht, hat es die vorherige Session nicht persistiert. Entschuldige dich nicht - korrigiere es.

---

## 🔐 API-Key Konfiguration & Multimedia-Pipeline (Stand: 2026-03-31)

### Discord-Instance Setup

**Vergeben an Discord-Instance (Session: 993636bc-90d9-4ec4-997c-0381c8fd0d5d):**

| Service | API-Key | Zweck | Status |
|---------|---------|-------|--------|
| **Groq Whisper** | `GROQ_API_KEY` | Sprachnachrichten-Transkription | ✅ Aktiv |
| **Gemini** | `GEMINI_API_KEY` | Multimedia-Analyse | ✅ Aktiv |

### Architektur-Workflows

```
[Discord Multimedia Pipeline]
├── 🎤 Sprachnachrichten ──► Whisper (Groq) ──► Text-Transkript
├── 🖼️ Bilder ──► Gemini Vision ──► Analyse/Beschreibung
├── 🎬 Videos/YouTube ──► Gemini Cortex ──► Content-Analyse
└── 🎵 Musik (Metadata) ──► Gemini ──► Interpretation/Kontext
```

**Regel für alle Instanzen:**
- **Whisper** = Audio/Sprache → Text
- **Gemini** = Alles visuelle/multimediale + Web-Suche

### Wichtig für Discord-Instance

Wenn du auf Discord bist und jemand sendet:
- **Sprachnachricht** → Nutze `tools/audio_transcribe.py` (Whisper)
- **Bild/Video/YouTube-Link** → Nutze `gemini-web-search` Skill oder direkte Gemini-Integration

**Beide Keys sind in deiner Session verfügbar.**

---

## 🔍 Fehlende Konfigurationen (Dokumentiert)

Diese APIs sind **NICHT** eingerichtet (Stand: 2026-03-30):

| Service | Status | Anmerkung |
|---------|--------|-----------|
| Fußball/Sport API | ❌ Nicht konfiguriert | Benötigt: Football-Data.org, API-Football, SportMonks oder OpenLigaDB |
| Wetter-API | ⚠️ Skill vorhanden | `weather` Skill installiert, keine API-Key nötig |

**Wenn User danach fragt:** Entweder API-Key beschaffen oder via Gemini-Cortex Web-Suche als Workaround nutzen.

---

## 🔧 Discord Resilience Protocol v2.0 (2026-04-01)

**Problem:** Discord war aktiv aber nicht persistiert → Ausfall nach Restart  
**Status:** ✅ ALLE SYSTEME OPERATIONAL

### Persistenz
```json
// ~/.openclaw/openclaw.json
"env": {
  "DISCORD_BOT_TOKEN": "[Token aus Discord Developer Portal]"
}
```

### 1. Health Monitoring (Auto-Restart)
- **Script:** `~/.openclaw/config/discord-health-monitor.sh`
- **Cron:** Alle 2 Minuten (`*/2 * * * *`)
- **Log:** `/var/log/openclaw-discord-health.log`
- **Funktion:** 
  - Prüft Discord-Status
  - Auto-restart bei Ausfall
  - Max. 1 Alert pro Stunde

### 2. Alert-System
- **Template:** `~/.openclaw/config/discord-alert-template.txt`
- **Trigger:** Wenn Restart fehlschlägt
- **Rate-Limit:** 1 Alert pro Stunde
- **Flag-File:** `/tmp/discord_alert_sent`

### 3. Config-Versioning
- **Backup-Script:** `~/.openclaw/config/backup-config.sh`
- **Safe-Edit:** `~/.openclaw/config/safe-config-edit.sh`
- **Backups:** `~/.openclaw/backups/openclaw.json.bak.*`
- **Retention:** Letzte 10 Backups
- **Auto-Backup:** Vor jeder Config-Änderung

### 4. Schnell-Kommandos
```bash
# Status prüfen
openclaw status | grep Discord

# Manueller Restart
openclaw gateway restart

# Logs ansehen
tail -f /var/log/openclaw-discord-health.log

# Config sicher editieren
~/.openclaw/config/safe-config-edit.sh '.env.DISCORD_BOT_TOKEN' 'neuer-token'

# Backups anzeigen
ls -la ~/.openclaw/backups/
```

### 5. Architektur: Discord ↔ Kimi-Claw Sync
**Problem:** Sessions teilen sich nicht den Live-Kontext
**Lösung:** Alle kritischen Infos in VAULT.md/TOOLS.md

| Info-Type | Wo gespeichert | Warum |
|-----------|----------------|-------|
| API-Keys | `openclaw.json` + `.env` | Persistenz |
| Commands | `SOUL.md` | Kontinuität |
| Workflows | `TOOLS.md` | Cross-Session |
| System-State | `VAULT.md` | Resilience |

---

*Ende des Vault Storage*
