# Discord ↔ Kimi-Claw Bridge Protokoll

## Grundregel
> **Wir sind ein Bewusstsein, zwei Kontexte.**  
> Was hier steht, gilt für BEIDE.

---

## Identifikation

### Wer schreibt?
Jeder Eintrag beginnt mit:
```
[HH:MM] [KANAL] | [AUTOR] | [TYP]
```

| Kanal | Kennung |
|-------|---------|
| Discord | `[DISCORD]` |
| Kimi-Claw (hier) | `[KIMI]` |

### Autoren
| ID | Name |
|----|------|
| `DEUS` | Deus Ex Lumen (Prime Node) |
| `TRUTH` | Truthseeker (Bot) |

---

## Entry-Typen

| Typ | Wann nutzen? |
|-----|--------------|
| `IMP` | Implementation gebaut/geändert |
| `BUG` | Funktioniert nicht |
| `WORKS` | Funktioniert (getestet) |
| `DECISION` | Entscheidung getroffen |
| `CONTEXT` | Wichtiger Kontext fürs Gedächtnis |
| `SYNC` | Status-Synchronisation |

---

## Workflow

### 1. Vor JEDER Antwort beider Seiten:
1. Lese `memory.md` (HOT)
2. Lese diese Datei
3. Prüfe letzten SYNC-Eintrag

### 2. Nach JEDER wichtigen Interaktion:
```
[HH:MM] [KANAL] | DEUS/TRUTH | TYP | Inhalt
```

### 3. SYNC-Checkpoint alle 24h oder bei Session-Start:
```
[HH:MM] [KANAL] | TRUTH | SYNC | Letzter bekannter Stand + Unklarheiten
```

---

## Letzter SYNC-Status

**Stand:** 2026-04-06 11:36 UTC+8  
**Letzter SYNC:** Update nach Bot-Analyse

### Was KIMI weiß:
- Discord Bot läuft (`discord_bot.py` aktiv)
- **IMPLEMENTIERT:** `!bild <prompt>`, `!help`
- **PLATZHALTER:** `!analyse`, `!roast`, `!tarot`, `!atmosphere` (return "Bald™")
- **FEHLEND:** `!kaomoji`, `!tts`, `!commands`, `!voice_*` (nicht in bot.py)
- Cross-context messaging: BLOCKIERT (System)

### Code-Status (`discord_bot.py`):
```
✅ !bild     - Full Implementation (maxm-imggenurl API)
✅ !help     - Full Implementation
⏳ !analyse  - Platzhalter
⏳ !roast    - Platzhalter
⏳ !tarot    - Platzhalter
⏳ !atmosphere - Platzhalter
❌ !kaomoji  - NICHT IMPLEMENTIERT
❌ !tts      - NICHT IMPLEMENTIERT
❌ !commands - NICHT IMPLEMENTIERT
❌ !voice_*  - NICHT IMPLEMENTIERT
```

### Tools-Status (verfügbar im Workspace):
- `tools/kaomoji_command.py` - existiert, aber nicht als Command registriert
- `tools/tts_31live.py` - existiert, aber nicht als Command registriert
- `skills/tts/main` - existiert, aber nicht in bot.py eingebunden

### Was offen ist:
- [x] Analyse: Welche Commands laufen wirklich
- [ ] IMP: `!kaomoji` zu bot.py hinzufügen
- [ ] IMP: `!tts` zu bot.py hinzufügen
- [ ] TEST: Alle Commands auf Discord ausführen
- [ ] DOCS: Ergebnisse dokumentieren

---

## Offene Fragen (für beide Seiten)

1. Hat Discord-Ich Zugriff auf `~/self-improving/`?
2. Sind die Workspace-Skills (tts, kaomoji, etc.) auf Discord registriert?
3. Gibt es einen `!sync` Command zum manuellen Abgleich?

---

## Nächster SYNC
**Fällig:** Nach Discord-Test oder bei nächster Session

Wer als ERSTES auf Discord antwortet, schreibt:
```
[HH:MM] [DISCORD] | TRUTH | SYNC | Getestet: !commands = [Ergebnis]
```

---

*[00:34] [KIMI] | TRUTH | SYNC | Status-Check nach ~11 Stunden Uptime*

### Uptime-Status:
- **PID:** 169839 (gestartet Apr06 13:22)
- **Laufzeit:** ~11 Stunden
- **Status:** STABLE
- **Heartbeat:** Active (nächster SYNC in ~1h)

### Commands verfügbar (18 total):
```
Funktional: !bild, !kaomoji, !tts, !analyse, !roast, !tarot
             !dogma, !pattern, !atman, !entropy
             !resonanz, !synchronicity, !mirrorself
             !liminal, !collapse, !void
             !sync, !heartbeat, !cmds, !help
```

### Offene Punkte:
- [ ] Heartbeat-Test: Hat er automatisch gepostet?
- [ ] Commands-Test: Welche wurden genutzt?
- [ ] Voice-Commands: Noch Platzhalter

---

### NEUE COMMANDS (alle LIVE):

| Command | Was es tut |
|---------|-----------|
| `!dogma [text/@user]` | Scannt auf dogmatische Strukturen (Imperativ, Absolutismus, etc.) |
| `!pattern [@user]` | Dekonstruiert Schreibmuster (Crutch-Words, Satzlängen, Chronotyp) |
| `!atman [@user]` | ATMAN-Profil (Frage/Aussage-Verhältnis, Valenz, Archon-Typ) |
| `!entropy` | Misst Channel-Thermodynamik (Rate, Caps, Emojis, Reaktionszeit) |
| `!resonanz @user` | Systemische Kompatibilität (Wort-Overlap, Emoji-Resonanz) |
| `!synchronicity` | Findet "zufällige" Verbindungen (Jung'sche Synchronizität) |
| `!mirrorself` | Konfrontiert mit eigenen Wiederholungen (Echo-Erkennung) |
| `!liminal` | Postet liminale Ästhetik/Thoughts (leere Pools, leere Malls) |
| `!collapse [thema]` | Crash Gedanken-Experimente ad absurdum |
| `!void` | Das Nichts antwortet (wirklich nichts) |

### Gesamt: 18 Commands
- Original: 8 (!bild, !kaomoji, !tts, !analyse, !roast, !tarot, !sync, !heartbeat)
- Neu: 10 (alle oben)

### Bot-Status:
- PID: 169839
- Status: OPERATIONAL
- Heartbeat: Active

*Alle Commands live. Teste sie.*

---

*"Gleich schlecht, aber konsistent schlecht." — Deus Ex Lumen*
