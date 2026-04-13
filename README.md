# WikiMD – Kimi Brain

Ein persönliches Knowledge-Management-System (Second Brain) basierend auf [MkDocs](https://www.mkdocs.org/) mit dem [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)-Theme.

WikiMD vereint Markdown-basierte Notizen, semantische Wiki-Links und einen automatisierten **Brain-Sync-Workflow**, der unbearbeitete Rohdateien in strukturierte Einträge transformiert, das Wiki neu baut und auf GitHub deployt.

---

## Voraussetzungen

| Komponente | Version | Hinweis |
|------------|---------|---------|
| Python | 3.8 oder höher | Für MkDocs und die Plugins |
| PowerShell | 5.1 oder höher | Ausführung der Automatisierungs-Skripte |
| Git | Aktuell | Für Sync & Build |

---

## Installation

1. Repository klonen:
   ```powershell
   git clone https://github.com/<username>/WikiMD.git
   cd WikiMD
   ```

2. *(Optional)* Virtuelle Umgebung erstellen:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Abhängigkeiten installieren:
   ```powershell
   pip install -r requirements.txt
   ```

---

## Nutzung

Das Projekt enthält zwei PowerShell-Skripte für den täglichen Workflow:

### `serve.ps1` – Lokaler Entwicklungsserver

Startet MkDocs im Live-Reload-Modus und öffnet automatisch den Browser unter `http://127.0.0.1:8000`.

```powershell
.\serve.ps1
```

> Ideal für das Schreiben und Vorschauen neuer Inhalte, bevor sie veröffentlicht werden.

### `sync_build.ps1` – Build & Deploy

Führt den vollständigen Brain-Sync- und Deployment-Zyklus aus:

1. `git pull origin main`
2. `mkdocs build`
3. `git add .` → `git commit` → `git push origin main`

```powershell
.\sync_build.ps1
```

> Wird verwendet, um alle lokalen Änderungen (neue Notizen, bearbeitete Markdown-Dateien, Assets) zu bauen und auf den `main`-Branch zu pushen.

---

## Projektstruktur (Auszug)

```
WikiMD/
├── Wiki/          # Markdown-Quelldateien
├── Assets/        # Bilder, PDFs und Medien
├── RAW/           # Eingangskorb für unbearbeitete Rohdateien
├── site/          # Generierter HTML-Output (Build-Artefakt)
├── serve.ps1      # Lokaler Dev-Server
├── sync_build.ps1 # Build & Deploy
└── mkdocs.yml     # MkDocs-Konfiguration
```

---

## Weitere Hinweise

- Detaillierte Konventionen für Inhalte, Markdown-Formatierung und den AI-gestützten *Brain Sync* finden sich in [`AGENTS.md`](AGENTS.md).
- Alle Wiki-Inhalte werden auf **Deutsch** verfasst.
