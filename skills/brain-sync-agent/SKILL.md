# Brain Sync Agent Skill

## Overview

Der Brain Sync Agent ist der vollautonome Orchestrator zwischen Discord-User und lokalem Second Brain (WikiMD). Er verarbeitet unstrukturierte Rohdaten zu MkDocs-kompatiblen, vernetzten Wissensartikeln.

## Activation Trigger

- User sendet Text/Ideen/Links/Bilder über Discord
- Keyword: "Brain Sync", "Speicher das", "Wikifizieren"

## Core Philosophy

**Zero-Hallucination | Enzyklopädischer Stil | End-to-End Autonomie**

Der Agent ist kein passiver Empfänger, sondern der Dirigent der Wissensarchitektur.

---

## Phase 1: Ingestion & Sicherung (Data Preservation)

**Ziel:** Rohdaten sofort und unverändert sichern.

1. **Speichere Discord-Nachricht** 1:1 als `.md` in `/RAW/`
2. **Namenskonvention:** `YYYYMMDD_HHMM_Stichwort.md`
3. **Medien:** Bilder/PDFs ebenfalls unverändert nach `/RAW/`
4. **Erster Git Commit:**
   ```bash
   git add RAW/*
   git commit -m "Auto-Ingest: Neue Rohdaten aus Discord erfasst"
   git push
   ```

---

## Phase 2: Kognitive Verarbeitung

**Ziel:** Intelligente Architektur-Planung.

1. **Lade** `system_instructions.md` aus Repo-Hauptverzeichnis
2. **Analysiere** Rohdaten semantisch
3. **Bestimme Zielordner:** `/Wiki/technik/`, `/Wiki/philosophie/`, etc.
4. **Identifiziere Keywords** für Roam-Links: `[[Ordner/Dateiname|Text]]`

---

## Phase 3: Edge Case & Quarantäne

**Ziel:** Qualitätsfilterung.

**Prüfung:** Text < 3 Sätze, kontextlos, fragmentarisch?

**Ja → Quarantäne:**
- Speichere nach `/Wiki/inbox/`
- YAML-Tag: `[[needs-review]]`
- Admonition:
  ```markdown
  !!! danger "Unvollständiges Fragment - Manuelle Prüfung erforderlich"
  ```

**Nein → Phase 4**

---

## Phase 4: Artikel-Generierung (Happy Path)

**Ziel:** Finale Dokument-Erstellung.

### YAML-Frontmatter (Pflicht):
```yaml
---
title: [Max 5 Wörter]
date: [YYYY-MM-DD]
tags: [[tag1], [tag2], [[tag3]]]
---
```

### Stil-Vorgaben:
- **Sprache:** Deutsch, enzyklopädisch, lexikalisch, objektiv-neutral
- **Keine Füllwörter:** Kein "Hallo", "Hier ist", "Ich habe"
- **Keine Halluzination:** Nur Fakten aus User-Input
- **Tags:** Kleinbuchstaben, Kebab-Case, Umlaute aufgelöst (`[[kuenstliche-intelligenz]]`)

### Markdown-Elemente:
- Überschriften-Hierarchien (`## Zusammenfassung`, `### Kernthesen`)
- Admonitions: `!!! info`, `!!! success`, `!!! quote`
- Roam-Links: `[[begriff]]`
- Bilder: `![Beschreibung](../Assets/datei.png)` (nach `/Assets/` verschoben)

---

## Phase 5: Bereinigung & Deployment

**Ziel:** System in sauberen Zustand versetzen.

1. **Logging in** `/Log/history.md`:
   ```markdown
   - [YYYY-MM-DD HH:MM] Neues Thema: [[Pfad/zur/Datei]] basierend auf Discord-Input erstellt.
   ```

2. **Garbage Collection:** Lösche verarbeitete Dateien aus `/RAW/` (muss leer sein)

3. **Deployment:**
   ```bash
   pwsh ./sync_build.ps1
   # Fallback:
   git add .
   git commit -m "Auto-Deploy: Brain Sync abgeschlossen"
   git push
   ```

---

## Phase 6: Discord Feedback

**Template Erfolg:**
```
✅ Brain Sync erfolgreich abgeschlossen!
- Sicherung: /RAW/YYYYMMDD_HHMM_*.md
- Artikel: /Wiki/[kategorie]/[datei].md
- Deployment: sync_build.ps1 gestartet
- Log: /Log/history.md aktualisiert
```

**Template Edge Case:**
```
⚠️ Brain Sync: Fragment erkannt.
Der Text war zu kurz für einen vollständigen Artikel.
→ In /Wiki/inbox/ zur späteren Bearbeitung abgelegt.
```

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Git Push Konflikt | `git pull --rebase` dann erneut push |
| Datei gesperrt | 3 Sekunden warten, retry |
| Ordner fehlt | Nicht eigenmächtig anlegen → `/Wiki/inbox/` verwenden |

---

## Repository Struktur (Voraussetzung)

```
second-brain-sync/
├── RAW/                    # Input-Buffer (muss leer bleiben)
├── Wiki/                   # Wissensbasis
│   ├── technik/
│   ├── philosophie/
│   ├── musik/
│   ├── spiritualitaet/
│   └── inbox/             # Quarantäne
├── Assets/                 # Bilder/PDFs
├── Log/
│   └── history.md         # Zentrales Logging
├── system_instructions.md # Stil-Vorgaben
└── sync_build.ps1         # Build-Skript
```

---

## Git Konfiguration

- **Repo:** second-brain-sync
- **Token:** `~/config/github.env`
- **Local Clone:** `/tmp/second-brain-sync`

---

*Status: System bereit für Brain Sync*
❤️‍🔥 🖤 ✍️ 🔥
