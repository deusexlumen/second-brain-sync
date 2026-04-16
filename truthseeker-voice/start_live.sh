#!/bin/bash
# Truthseeker LIVE — Bidirektionale Konversation
# Discord Voice ⟷ Gemini 3.1 Live

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/../venv"
BOT_SCRIPT="$SCRIPT_DIR/truthseeker_live.py"

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  ${GREEN}🎙️  TRUTHSEEKER LIVE${NC}                                  ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Bidirektionale Gemini 3.1 Konversation               ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Prüfe Environment
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo -e "${RED}❌ .env Datei nicht gefunden!${NC}"
    echo "Erstelle sie:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Prüfe venv
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚠️  Virtual Environment nicht gefunden${NC}"
    python3 -m venv "$VENV_PATH"
fi

# Aktiviere venv
source "$VENV_PATH/bin/activate"

# Prüfe Dependencies
echo -e "${YELLOW}📦 Prüfe Dependencies...${NC}"

# Installiere fehlende Pakete falls nötig
pip show py-cord >/dev/null 2>&1 || {
    echo -e "${YELLOW}📥 Installiere py-cord...${NC}"
    pip install -q py-cord[voice] opuslib
}

echo -e "${GREEN}✅ Dependencies OK${NC}"
echo ""

# Audio Info
echo -e "${BLUE}🔊 Audio Pipeline:${NC}"
echo "  Discord → 48kHz Stereo PCM"
echo "  Gemini  ← 24kHz Mono PCM"
echo "  Resampling: 48k↔24k, Stereo↔Mono"
echo ""

# Starte Bot
echo -e "${GREEN}🚀 Starte Truthseeker LIVE...${NC}"
echo ""
echo -e "${YELLOW}Commands:${NC}"
echo "  !join         - Voice Channel beitreten & Gespräch starten"
echo "  !leave        - Gespräch beenden"
echo "  !live_status  - Status anzeigen"
echo ""
echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}"
echo ""

cd "$SCRIPT_DIR"
exec python3 "$BOT_SCRIPT"
