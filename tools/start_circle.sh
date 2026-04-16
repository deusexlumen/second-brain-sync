#!/bin/bash
# Truthseeker's Circle - Quick Start
# Eine Crew. Keine Firma.

echo ""
echo "🚀 Truthseeker's Circle"
echo "======================="
echo ""
echo "Research • Entertainment • Casual"
echo ""

# Dependencies
pip install discord.py toml -q 2>/dev/null

# Token-File erstellen falls nicht existiert
TOKEN_FILE="$HOME/.openclaw/config/tokens.env"
mkdir -p "$(dirname "$TOKEN_FILE")"

if [ ! -f "$TOKEN_FILE" ]; then
    cat > "$TOKEN_FILE" << 'EOF'
# Truthseeker's Circle - Tokens
# Erstelle 5 Discord Apps bei https://discord.com/developers/applications
# Aktiviere: Server Members Intent + Message Content Intent
# Kopiere die Tokens hier:

DISCORD_TOKEN_HIRO=""
DISCORD_TOKEN_KIRA=""
DISCORD_TOKEN_REX=""
DISCORD_TOKEN_NOVA=""
DISCORD_TOKEN_VEX=""
EOF
    chmod 600 "$TOKEN_FILE"
fi

# Persistenz-Verzeichnis
mkdir -p "$HOME/self-improving/circle"

# Check
echo "📦 Bereit."
echo ""
echo "DIE CREW:"
echo "---------"
echo "❤️‍🔥🛡️  Hiro  (The Steward)   - Hauptinterface, beschützend"
echo "🔮📚  Kira  (The Seeker)    - Research, neugierig"
echo "⚙️🔧  Rex   (The Maker)      - Build, pragmatisch"
echo "✨🎭  Nova  (The Muse)       - Entertainment, theatralisch"
echo "🗺️📝  Vex   (The Archivist)  - Memory, ruhig"
echo ""

TOKENS=0
for agent in HIRO KIRA REX NOVA VEX; do
    VAR="DISCORD_TOKEN_$agent"
    [ -n "${!VAR}" ] && ((TOKENS++))
done

if [ $TOKENS -eq 0 ]; then
    echo "⚠️  Keine Tokens gefunden."
    echo "   Bitte eintragen in: $TOKEN_FILE"
    echo ""
fi

echo "Starten mit: python3 ~/.openclaw/workspace/tools/truthseeker_circle.py"
echo ""
