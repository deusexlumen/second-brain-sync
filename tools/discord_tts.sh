#!/bin/bash
# Discord TTS Integration
# Liest Nachrichten vor im Voice Channel

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHANNEL_ID="1475201017867010058"  # truthseerk-station

# TTS erstellen
echo "🎙️ Erstelle TTS..."
AUDIO_FILE=$($SCRIPT_DIR/tts.sh "$1" "${2:-de}")

if [ -f "$AUDIO_FILE" ]; then
    echo "✅ Audio erstellt: $AUDIO_FILE"
    echo ""
    echo "📤 Um in Discord zu senden:"
    echo "   1. Datei manuell in #truthseerk-station hochladen"
    echo "   2. ODER: OpenClaw Discord Integration nutzen"
    echo ""
    echo "🔊 Datei: $AUDIO_FILE"
else
    echo "❌ TTS fehlgeschlagen"
    exit 1
fi
