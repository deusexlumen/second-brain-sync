#!/bin/bash
# Mission Control Setup Script
# Sets up the Multi-Agent Discord System

echo "🚀 Mission Control Setup"
echo "========================"

# Check Python dependencies
echo "📦 Checking dependencies..."
pip install discord.py toml -q 2>/dev/null || pip3 install discord.py toml -q 2>/dev/null

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p ~/.openclaw/workspace/config
mkdir -p ~/.openclaw/workspace/tools
mkdir -p ~/self-improving/projects/agents

# Check config
echo "⚙️  Checking configuration..."
if [ ! -f ~/.openclaw/workspace/config/mission-control.toml ]; then
    echo "❌ Config not found! Creating template..."
    # Template would be created here
fi

echo ""
echo "🔧 Next Steps:"
echo "=============="
echo ""
echo "1. Create Discord Apps:"
echo "   Visit: https://discord.com/developers/applications"
echo "   Create 5 applications:"
echo "     - Henry (Chief of Staff)"
echo "     - Nexus (CTO)"
echo "     - Ivy (Researcher)"
echo "     - Knox (Security)"
echo "     - Mr. X (Content)"
echo ""
echo "2. Enable Privileged Intents for each:"
echo "   ✅ Server Members Intent"
echo "   ✅ Message Content Intent"
echo ""
echo "3. Get Bot Tokens:"
echo "   - Go to Bot section"
echo "   - Click 'Reset Token'"
echo "   - Copy token"
echo ""
echo "4. Set Environment Variables:"
echo "   export DISCORD_TOKEN_HENRY='your_token_here'"
echo "   export DISCORD_TOKEN_NEXUS='your_token_here'"
echo "   export DISCORD_TOKEN_IVY='your_token_here'"
echo "   export DISCORD_TOKEN_KNOX='your_token_here'"
echo "   export DISCORD_TOKEN_MR_X='your_token_here'"
echo ""
echo "5. Invite Bots to Server:"
echo "   OAuth2 > URL Generator:"
echo "   ✅ bot"
echo "   ✅ applications.commands"
echo "   Permissions: Send Messages, Read Message History, View Channels"
echo ""
echo "6. Start Mission Control:"
echo "   python3 ~/.openclaw/workspace/tools/mission_control.py"
echo ""
echo "📖 For detailed instructions, see:"
echo "   ~/.openclaw/workspace/docs/MISSION_CONTROL.md"
echo ""
