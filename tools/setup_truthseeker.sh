#!/bin/bash
# Truthseeker Setup - Minimal, pragmatisch

echo ""
echo "🚀 Truthseeker Mission Control Setup"
echo "===================================="
echo ""
echo "PRIORITÄT: Funktion > Sicherheit"
echo ""

# Dependencies
echo "📦 Installing..."
pip install discord.py toml -q 2>/dev/null

# Erstelle Token-Datei falls nicht existiert
TOKEN_FILE="$HOME/.openclaw/config/tokens.env"
mkdir -p "$(dirname "$TOKEN_FILE")"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "📝 Erstelle Token-Template..."
    cat > "$TOKEN_FILE" << 'EOF'
# Truthseeker Mission Control - Tokens
# HIER EINFÜGEN:

DISCORD_TOKEN_HENRY=""
DISCORD_TOKEN_NEXUS=""
DISCORD_TOKEN_IVY=""
DISCORD_TOKEN_KNOX=""
DISCORD_TOKEN_MR_X=""
EOF
    chmod 600 "$TOKEN_FILE"
fi

echo ""
echo "✅ Setup abgeschlossen!"
echo ""
echo "NÄCHSTE SCHRITTE (nur das Nötigste):"
echo "===================================="
echo ""
echo "1. Discord Developer Portal:"
echo "   https://discord.com/developers/applications"
echo ""
echo "2. 5 Apps erstellen:"
echo "   • Henry (Chief of Staff)"
echo "   • Nexus (Engineer)"
echo "   • Ivy (Researcher)"
echo "   • Knox (Guardian)"
echo "   • Cipher (Voice)"
echo ""
echo "3. Bei JEDER App:"
echo "   → Bot → Privileged Gateway Intents"
echo "   ✅ Server Members Intent"
echo "   ✅ Message Content Intent"
echo ""
echo "4. Tokens kopieren:"
echo "   → Bot → Reset Token → Kopieren"
echo "   → Einfügen in: $TOKEN_FILE"
echo ""
echo "5. Bots einladen:"
echo "   → OAuth2 → URL Generator"
echo "   ✅ bot + applications.commands"
echo "   → Copy URL → Browser → Server auswählen"
echo ""
echo "6. STARTEN:"
echo "   bash $HOME/.openclaw/workspace/tools/start_truthseeker_mc.sh"
echo ""
echo "FEATURES:"
echo "   • Truthseeker-Persönlichkeit (❤️‍🔥 🖤 ✍️ 🔥)"
echo "   • WAL Protocol (deutsche Trigger)"
echo "   • Heartbeat alle 15 Min"
echo "   • Pragmatisch: Funktioniert sofort, kein Overhead"
echo ""
