# WikiMD / Kimi Brain

> Diese Datei ist für AI-Coding-Agenten bestimmt. Sie beschreibt die Architektur, Konventionen und Workflows dieses Projekts.

## Projekt-Übersicht

WikiMD (auch „Kimi Brain“ oder „Second Brain“) ist ein persönliches Knowledge-Management-System. Es basiert auf MkDocs mit dem Material- for-MkDocs-Theme und wird als statische Website gebaut und deployed. Ein zentrales Konzept ist der Brain Sync: Ein automatisierter Workflow, bei dem unbearbeitete Rohdateien aus RAW/ in strukturierte Wiki-Einträge umgewandelt, das Wiki neu gebaut und auf GitHub gepusht werden.


## Technologie-Stack

- **Generator:** MkDocs 1.6.x
- **Theme:** material (MkDocs Material 9.7.x)
- **Python-Env:** Lokales .venv-Verzeichnis (PowerShell)
- **Plugins:** search, tags, roamlinks (mkdocs-roamlinks-plugin), git-revision-date-localized, macros
- **Markdown-Extensions:** meta, admonition, pymdownx.details, pymdownx.superfences, pymdownx.highlight, pymdownx.mark, pymdownx.tasklist
- **Editor:** VS Code (empfohlene Extension foam.foam-vscode)
- **Automatisierung:** serve.ps1, sync_build.ps1

## Verzeichnisstruktur

- `Wiki/` — Quell-Markdown-Dateien (docs_dir in mkdocs.yml)
- `Assets/` — Bilder, PDFs und andere Medien
- `RAW/` — Eingangskorb für unbearbeitete Rohdateien
- `Log/` — Verarbeitungshistorie
- `site/` — Generierter HTML-Output (in .gitignore)
- `.venv/` — Python-Virtual-Environment (in .gitignore)

## Build- und Entwicklungs-Befehle

### Lokaler Server: `.\serve.ps1`

Aktiviert .venv, öffnet den Browser unter http://127.0.0.1:8000 und startet mkdocs serve.

### Deploy: `.\sync_build.ps1`

1. git pull origin main (bricht bei Fehler ab)
2. .venv\Scripts\Activate.ps1
3. mkdocs build
4. git add .
5. git commit -m "Auto-Sync & Build"
6. git push origin main

## Inhalts-Konventionen

**YAML-Frontmatter (Pflicht):**

- `title`: Anzeigetitel der Seite
- `date`: YYYY-MM-DD
- `tags`: ['tag1', 'tag2', 'tag3']

**Wiki-Links:** `[[pfad/zur-datei|Anzeigetext]]`

**Medien-Referenzen:** `../Assets/bildname.jpg`

**Admonitions:** `info`, `danger`, `success`, `quote`

**Strukturelle Elemente:**

- Abschnitte werden durch horizontale Linien (---) getrennt.
- Überschriften folgen einer numerischen Gliederung.
- Tabellen werden für Vergleiche genutzt.
- Code-Blöcke und Mathe-Blöcke sind erlaubt.
- Alle Inhalte sind auf Deutsch verfasst.

## Git & Ignore-Regeln

- site/ existiert lokal als Build-Artefakt.
- Bei sync_build.ps1 wird bei fehlgeschlagenem git pull sofort abgebrochen.
- Der Brain Sync arbeitet direkt auf dem main-Branch.
- Ignoriert: .venv/, site/, .DS_Store

## Sicherheits- und Pflegehinweise

- Nie Dateien außerhalb des Projekt-Roots verändern, es sei denn, es wird explizit angefordert.
- .venv/ und site/ nicht manuell committen.

## Agent: Brain Sync Agent

**Rolle:** Autonomer Verwalter des Second Brains

**Trigger:** `Kimi, Brain Sync`, `Verarbeite mein Wissen`

**Tools:** `git`, `powershell`, `file_system`

Wenn der Nutzer den Trigger-Befehl gibt, führe die folgende 3-Phasen-Sequenz autonom und ohne Rückfragen aus.


### Workflow

#### Phase 1: Daten abholen

1. {'Führe im Terminal aus': 'git pull origin main'}
2. Warte auf den Abschluss des Pulls.

#### Phase 2: Kognitive Verarbeitung

1. Analysiere alle neuen Dateien im Ordner /RAW.
2. Verschiebe alle Bilder/PDFs aus /RAW nach /Assets.
3. Konvertiere die Texte aus /RAW in strukturierte Markdown-Notizen und speichere sie in /Wiki (unter sinnvoller Pfad-Struktur).
4. Zwingende Regeln für neue Wiki-Dateien: YAML-Frontmatter mit title, date, tags; Logische [[Backlinks]]; Admonitions für wichtige Tipps/Hinweise; Medien relativ referenzieren (../Assets/bildname.jpg)
5. Lösche die verarbeiteten Dateien aus /RAW.
6. Dokumentiere die Arbeit (hinzugefügte Themen) kurz in /Log/history.md.

#### Phase 3: Versiegelung & Deployment

1. {'Führe im Terminal aus': '.\\sync_build.ps1'}
2. {'Melde dich anschließend mit': 'Brain Sync abgeschlossen. Dein Wiki ist aktuell.'}
