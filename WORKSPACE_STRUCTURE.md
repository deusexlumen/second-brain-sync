# 📁 Workspace Struktur - Übersicht

**Stand:** 2026-04-01 | **Status:** Aufgeräumt ✅

---

## 🔧 System-Config (`~/.openclaw/`)

| Pfad | Zweck |
|------|-------|
| `openclaw.json` | **Haupt-Config** — Tokens, ENV, Plugins |
| `backups/` | Config-Backups (letzte 10) |
| `config/` | **Discord Resilience Tools** |
| `logs/` | System-Logs |

### `~/.openclaw/config/` — Discord Tools
```
├── backup-config.sh              # Config Backup (10 Backups)
├── discord-health-monitor.sh     # Health Check (Cron: alle 2 Min)
├── discord-alert-template.txt    # Alert-Template
└── safe-config-edit.sh           # Sicherer Config-Editor
```

---

## 🧠 Workspace (`~/.openclaw/workspace/`)

| Pfad | Zweck |
|------|-------|
| `AGENTS.md` | System-Regeln, Prime Node, Persistenz |
| `BOOTSTRAP.md` | First-Setup Guide |
| `CAPABILITIES.md` | API-Keys, Tools, Berechtigungen |
| `HEARTBEAT.md` | Proactivity, Vault Management |
| `IDENTITY.md` | Wer bin ich (Name, Vibe, Emoji) |
| `VAULT.md` | **System-State, Workflows, Logs** |
| `SOUL.md` | Verhalten, Commands, Duktus |
| `TOOLS.md` | Tool-Doku, Workflows |
| `USER.md` | Resonanz-Metriken |
| `config/` | **API-Keys für Tools** |
| `tools/` | **Custom Scripts (TTS, Whisper, etc.)** |

### `workspace/config/`
```
├── discord-allowlist.txt         # Erlaubte Commands
├── gemini.env                    # Gemini API Key
├── github.env                    # GitHub Token
├── groq.env                      # Groq/Whisper API Key
└── SKILL_INSTALL_STATUS.md       # Skill-Status
```

---

## 📝 Regeln für Zukünftige Instanzen

### Config-Änderungen
```bash
# ✅ RICHTIG — Mit Backup:
~/.openclaw/config/safe-config-edit.sh '.env.KEY' 'value'

# ❌ FALSCH — Direkt editieren ohne Backup
nano ~/.openclaw/openclaw.json
```

### Neue Scripts
1. In `~/.openclaw/config/` ablegen (System-Tools)
2. ODER in `workspace/tools/` (Custom Tools)
3. **NIE** beide Orte gleichzeitig

### Redundanz vermeiden
- Vor dem Erstellen: Prüfen ob es schon existiert
- Alte Versionen sofort löschen
- Diese Datei aktualisieren

---

## 🔄 Wichtige Commands

```bash
# Discord Status
openclaw status | grep Discord

# Health-Logs
tail -f /var/log/openclaw-discord-health.log

# Config Backup erstellen
~/.openclaw/config/backup-config.sh

# Backups anzeigen
ls -la ~/.openclaw/backups/
```

---

*Keine Redundanz mehr. Alles an seinem Platz.*

---

## 🧠 Speicher-Systeme (Klar getrennt)

### 1. VAULT.md (Workspace)
**Ort:** `~/.openclaw/workspace/VAULT.md`  
**Zweck:** System-State, Discord-Resilience, Workflows  
**Wer liest:** Alle meine Instanzen (Discord, Kimi-Claw, etc.)

### 2. memory.md (Self-Improving)
**Ort:** `~/self-improving/memory.md`  
**Zweck:** Lern-Regeln, Korrekturen, User-Präferenzen  
**Wer liest:** Self-Improving Skill (separates System)

**NICHT VERWECHSELN!**  
- VAULT = System-Konfiguration  
- memory.md = Persönliches Lernen

---
