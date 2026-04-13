# AGENTS.md – WikiMD / Kimi Brain

> Diese Datei ist für AI-Coding-Agenten bestimmt. Sie beschreibt die Architektur, Konventionen und Workflows dieses Projekts.

---

## Projekt-Übersicht

**WikiMD** (auch „Kimi Brain“ oder „Second Brain“) ist ein persönliches Knowledge-Management-System. Es basiert auf [MkDocs](https://www.mkdocs.org/) mit dem [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)-Theme und wird als statische Website gebaut und deployed.

Die Inhalte werden als Markdown-Dateien im Ordner `Wiki/` gepflegt, Medien (Bilder, PDFs) in `Assets/` abgelegt und der HTML-Output durch `mkdocs build` im Ordner `site/` erzeugt.

Ein zentrales Konzept ist der **Brain Sync**: Ein automatisierter Workflow, bei dem unbearbeitete Rohdateien aus `RAW/` in strukturierte Wiki-Einträge umgewandelt, das Wiki neu gebaut und auf GitHub gepusht werden.

---

## Technologie-Stack

| Komponente | Details |
|------------|---------|
| Generator | MkDocs 1.6.x |
| Theme | `material` (MkDocs Material 9.7.x) |
| Python-Env | Lokales `.venv`-Verzeichnis (PowerShell) |
| Plugins | `search`, `tags`, `roamlinks` (`mkdocs-roamlinks-plugin`) |
| Markdown-Extensions | `meta`, `admonition`, `pymdownx.details`, `pymdownx.superfences`, `pymdownx.mark`, `pymdownx.tasklist` |
| Editor | VS Code (empfohlene Extension: `foam.foam-vscode`) |
| Automatisierung | PowerShell-Skripte (`serve.ps1`, `sync_build.ps1`) |

**Wichtig:** Es gibt keine `requirements.txt`, `pyproject.toml` oder `package.json` im Repository. Die Python-Abhängigkeiten liegen vollständig im mitgelieferten `.venv`-Ordner.

---

## Verzeichnisstruktur

```
WikiMD/
├── Wiki/                   # Quell-Markdown-Dateien (docs_dir in mkdocs.yml)
│   ├── index.md            # Startseite
│   ├── meta/
│   ├── technik/
│   ├── philosophie/
│   ├── politik/
│   ├── musik/
│   └── spiritualitaet/
├── Assets/                 # Bilder, PDFs und andere Medien
├── RAW/                    # Eingangskorb für unbearbeitete Rohdateien
├── Log/                    # Verarbeitungshistorie
│   └── history.md
├── site/                   # Generierter HTML-Output (in .gitignore)
├── .venv/                  # Python-Virtual-Environment (in .gitignore)
├── .vscode/                # VS Code Tasks & Extensions
├── mkdocs.yml              # MkDocs-Konfiguration
├── serve.ps1               # Lokaler Entwicklungsserver
├── sync_build.ps1          # Build & Deploy-Skript
└── system_instructions.md  # Direktiven für autonome Brain-Sync-Agenten
```

---

## Build- und Entwicklungs-Befehle

Alle Befehle werden aus dem Projekt-Root ausgeführt.

### Lokalen Server starten

```powershell
.\serve.ps1
```

Dies aktiviert `.venv`, öffnet den Browser unter `http://127.0.0.1:8000` und startet `mkdocs serve`.

### Wiki bauen & deployen

```powershell
.\sync_build.ps1
```

Ablauf des Skripts:
1. `git pull origin main` (bricht bei Fehler ab)
2. `.venv\Scripts\Activate.ps1`
3. `mkdocs build`
4. `git add .`
5. `git commit -m "Auto-Sync & Build"`
6. `git push origin main`

### VS Code Tasks

Zwei Tasks sind in `.vscode/tasks.json` definiert:
- **Brain Sync & Build** → führt `.­\sync_build.ps1` aus
- **Brain Server Starten** → führt `.­\serve.ps1` aus

---

## Inhalts-Konventionen (Wiki / Markdown)

### YAML-Frontmatter (Pflicht)

Jede Markdown-Datei unter `Wiki/` **muss** folgenden Frontmatter enthalten:

```yaml
---
title: <Anzeigetitel der Seite>
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---
```

### Wiki-Links (Backlinks)

Verwende für interne Verlinkungen die `roamlinks`-Syntax:

```markdown
[[pfad/zur-datei|Anzeigetext]]
```

Beispiel:
```markdown
- [[technik/vibe-coding|Vibe Coding]] — KI-gestützte Softwareentwicklung
```

### Admonitions

Wichtige Hinweise, Warnungen und Erfolgsmeldungen werden mit Admonitions hervorgehoben:

```markdown
!!! info "Titel"
    Beschreibender Text.

!!! danger "Kritische Risiken"
    - Punkt 1
    - Punkt 2

!!! success "Erfolg"
    Aktion abgeschlossen.

!!! quote "Zitat"
    Zitierter Text.
```

### Medien-Referenzen

Bilder und Dateien aus `Assets/` werden relativ referenziert:

```markdown
![Beschreibung](../Assets/bildname.jpg)
```

### Strukturelle Elemente

- **Abschnitte** werden durch horizontale Linien (`---`) voneinander getrennt.
- **Überschriften** folgen einer numerischen Gliederung (`## 1. Titel`, `### 1.1 Untertitel`).
- **Tabellen** werden für Vergleiche und Statusübersichten genutzt.
- **Code-Blöcke** (mit oder ohne Sprachangabe) sowie **Mathe-Blöcke** (`$$...$$`) sind erlaubt.
- Alle Inhalte sind auf **Deutsch** verfasst.

---

## Brain Sync Workflow

Wenn der Nutzer den Befehl **„Kimi, Brain Sync“** (oder Ähnliches) gibt, führe die folgende 3-Phasen-Sequenz **autonom und ohne Rückfragen** aus:

### Phase 1: Daten abholen
1. Führe im Terminal aus: `git pull origin main`
2. Warte auf den Abschluss des Pulls.

### Phase 2: Kognitive Verarbeitung
1. Analysiere alle neuen Dateien im Ordner `/RAW`.
2. Verschiebe alle Bilder/PDFs aus `/RAW` nach `/Assets`.
3. Konvertiere die Texte aus `/RAW` in strukturierte Markdown-Notizen und speichere sie in `/Wiki` (unter sinnvoller Pfad-Struktur).
4. **Zwingende Regeln für neue Wiki-Dateien:**
   - YAML-Frontmatter mit `title`, `date`, `tags`
   - Logische `[[Backlinks]]` zu verwandten Themen
   - Admonitions für wichtige Tipps/Hinweise
   - Medien relativ referenzieren (`../Assets/bildname.jpg`)
5. Lösche die verarbeiteten Dateien aus `/RAW`.
6. Dokumentiere die Arbeit (hinzugefügte Themen) kurz in `/Log/history.md`.

### Phase 3: Versiegelung & Deployment
1. Führe im Terminal aus: `.\sync_build.ps1`
2. Melde dich anschließend mit: **„Brain Sync abgeschlossen. Dein Wiki ist aktuell.“**

---

## Git & Ignore-Regeln

Die `.gitignore` ignoriert:
- `.venv/`
- `site/`
- `.DS_Store`

**Hinweis:** Obwohl `site/` in `.gitignore` steht, existiert der Ordner lokal als Build-Artefakt. Der Deployment-Output wird typischerweise über `mkdocs build` erzeugt und kann separat (z. B. via GitHub Pages) deployed werden.

---

## Sicherheits- und Pflegehinweise

- **Nie Dateien außerhalb des Projekt-Roots verändern**, es sei denn, es wird explizit angefordert.
- `.venv/` und `site/` nicht manuell committen.
- Bei `sync_build.ps1` wird bei einem fehlgeschlagenen `git pull` sofort abgebrochen, um Merge-Konflikte zu vermeiden.
- Der Brain Sync arbeitet direkt auf dem `main`-Branch; Branches werden nicht verwendet.
