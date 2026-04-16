#!/bin/bash
# Truthseeker Mission Control - Quick Start
# Funktion first. Security second.

echo ""
echo "🚀 Truthseeker Mission Control - Quick Start"
echo "============================================"
echo ""

# Prüfe dependencies
echo "📦 Checking..."
pip install discord.py toml -q 2>/dev/null || pip3 install discord.py toml -q 2>/dev/null

# Prüfe Config
CONFIG="$HOME/.openclaw/workspace/config/truthseeker-mission-control.toml"
if [ ! -f "$CONFIG" ]; then
    echo "❌ Config fehlt!"
    exit 1
fi

# Prüfe Tokens - pragmatisch
echo "🔑 Checking tokens..."
MISSING=0
for agent in HENRY NEXUS IVY KNOX MR_X; do
    VAR="DISCORD_TOKEN_$agent"
    if [ -z "${!VAR}" ]; then
        echo "   ⚠️  $agent: Kein Token (wird übersprungen)"
        MISSING=$((MISSING+1))
    else
        echo "   ✅ $agent: Token gefunden"
    fi
done

if [ $MISSING -eq 5 ]; then
    echo ""
    echo "❌ Keine Tokens gefunden!"
    echo ""
    echo "Option 1 - Environment Variables:"
    echo "   export DISCORD_TOKEN_HENRY='dein_token'"
    echo "   export DISCORD_TOKEN_NEXUS='dein_token'"
    echo "   # ... usw"
    echo ""
    echo "Option 2 - Token-Datei:"
    echo "   ~/.openclaw/config/tokens.env"
    echo "   DISCORD_TOKEN_HENRY=dein_token"
    echo ""
    exit 1
fi

echo ""
echo "🎯 Starting..."
echo "   Pragmatischer Modus: Agents mit Tokens starten sofort"
echo "   Fehlende Agents können später hinzugefügt werden"
echo ""

# Starte
python3 "$HOME/.openclaw/workspace/tools/truthseeker_mission_control.py"
