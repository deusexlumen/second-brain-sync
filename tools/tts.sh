#!/bin/bash
# TTS Command Wrapper für Discord
# Nutzt Gemini 3.1 Flash Live (WebSocket → Audio-Datei)

TEXT="$1"
LANG="${2:-German}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# FIX: Nutze workspace venv, nicht parent venv
if [ -f "$SCRIPT_DIR/../workspace/venv/bin/python3" ]; then
    VENV_PYTHON="$SCRIPT_DIR/../workspace/venv/bin/python3"
elif [ -f "$SCRIPT_DIR/../venv/bin/python3" ]; then
    VENV_PYTHON="$SCRIPT_DIR/../venv/bin/python3"
else
    echo "❌ Kein Python venv gefunden!" >&2
    exit 1
fi

# Environment laden
export GEMINI_API_KEY=$(grep GEMINI_API_KEY "$SCRIPT_DIR/../config/gemini.env" 2>/dev/null | cut -d= -f2)

# Gemini 3.1 Live TTS
# FIX: Zeige Fehler an, nicht unterdrücken
OUTPUT=$($VENV_PYTHON "$SCRIPT_DIR/tts_31live.py" "$TEXT" "$LANG" 2>&1)

# Prüfe ob Output ein existierender Pfad ist
if [ ! -f "$OUTPUT" ]; then
    echo "❌ Gemini Live TTS fehlgeschlagen: $OUTPUT" >&2
    echo "⚠️ Kein Fallback verfügbar — Gemini Live ist Pflicht." >&2
    exit 1
fi

# Erfolg — gib Pfad aus
echo "$OUTPUT"
