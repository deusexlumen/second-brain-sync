# YouTube Integration Setup

## Problem
YouTube blockiert automatisierten Zugriff. Cookies sind kurzlebig (rotieren automatisch).

## Lösung: Zwei Methoden

### Methode 1: Invidious (Sofort, kein API Key)
Invidious ist ein YouTube-Proxy ohne Tracking.

**Vorteile:**
- Kein API Key nötig
- Keine Cookies
- Open Source

**Nachteile:**
- Instanzen können down sein
- Manchmal langsam

**Verwendung:**
```bash
python3 ~/.openclaw/workspace/tools/youtube_analyzer.py "https://youtu.be/XXXXX"
```

### Methode 2: YouTube Data API v3 (Persistent)
Offizielle API mit API Key.

**Setup:**
1. Gehe zu https://console.cloud.google.com/
2. Erstelle neues Projekt (oder nutze bestehendes)
3. Aktiviere "YouTube Data API v3"
4. Erstelle API Key (Credentials → Create Credentials → API Key)
5. Speichere Key:

```bash
echo 'YOUTUBE_API_KEY=YOUR_KEY_HERE' > ~/.openclaw/workspace/config/youtube.env
```

**Vorteile:**
- Stabil und zuverlässig
- 10.000 Quota Units/Tag (kostenlos)
- Offiziell unterstützt

**Nachteile:**
- Erfordert Google Account
- Einmaliger Setup-Aufwand

## Nutzung

```bash
# Analysiere YouTube Video
python3 ~/.openclaw/workspace/tools/youtube_analyzer.py "https://youtu.be/79a2O_cQcIM"

# Oder mit Umgebungsvariable
export YOUTUBE_API_KEY=your_key
python3 ~/.openclaw/workspace/tools/youtube_analyzer.py "URL"
```

## Troubleshooting

### "Sign in to confirm you're not a bot"
→ Invidious Instanzen sind down. Nutze YouTube API oder warte.

### "API key not valid"
→ Prüfe ob YouTube Data API v3 aktiviert ist.

### "Quota exceeded"
→ Du hast das tägliche Limit (10.000) erreicht. Warte bis morgen.

---

*Setup erstellt: 2026-04-10*
