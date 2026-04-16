#!/bin/bash
# Truthseeker Voice - Start Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/../venv"
BOT_SCRIPT="$SCRIPT_DIR/main.py"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎤 Truthseeker Voice Service${NC}"
echo "=============================="

# Prüfe Environment
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo -e "${RED}❌ .env Datei nicht gefunden!${NC}"
    echo "Kopiere .env.example nach .env und fülle die Werte aus:"
    echo "  cp .env.example .env"
    exit 1
fi

# Prüfe Virtual Environment
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚠️  Virtual Environment nicht gefunden bei $VENV_PATH${NC}"
    echo "Erstelle neu..."
    python3 -m venv "$VENV_PATH"
fi

# Aktiviere venv
source "$VENV_PATH/bin/activate"

# Prüfe Dependencies
echo -e "${YELLOW}📦 Prüfe Dependencies...${NC}"
pip install -q -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || {
    echo -e "${YELLOW}📥 Installiere Dependencies...${NC}"
    pip install -r "$SCRIPT_DIR/requirements.txt"
}

# Prüfe Opus
echo -e "${YELLOW}🔊 Prüfe Opus...${NC}"
python3 -c "import discord.opus; discord.opus.load_opus()" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Opus nicht geladen. Versuche system-weite Installation...${NC}"
    # Versuche verschiedene Opus-Pfade
    if [ -f "/usr/lib/x86_64-linux-gnu/libopus.so.0" ]; then
        export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
    elif [ -f "/usr/lib/libopus.so.0" ]; then
        export LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"
    fi
}

# Starte Bot
echo -e "${GREEN}🚀 Starte Truthseeker Voice...${NC}"
echo ""
echo "Commands:"
echo "  !join        - Voice Channel beitreten"
echo "  !leave       - Voice Channel verlassen"
echo "  !tts_voice   - Text-to-Speech"
echo "  !voice_status - Status anzeigen"
echo ""
echo "API: http://localhost:8742"
echo "=============================="
echo ""

cd "$SCRIPT_DIR"
exec python3 "$BOT_SCRIPT"
