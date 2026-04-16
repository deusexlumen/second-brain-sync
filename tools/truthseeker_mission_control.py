#!/usr/bin/env python3
"""
Truthseeker Mission Control
Pragmatisch. Funktionsorientiert. Mit Charakter.

Basierend auf OpenClaw, inspiriert vom Video,
personifiziert für Truthseeker (Kimi Claw).
"""

import os
import sys
import asyncio
import random
import toml
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Discord - pragmatischer Import
try:
    import discord
    from discord.ext import commands, tasks
except ImportError:
    print("Installing discord.py...")
    os.system("pip install discord.py toml -q")
    import discord
    from discord.ext import commands, tasks

# Truthseeker Signatur-Elemente
TRUTHSEEKER_EMOJIS = ["❤️‍🔥", "🖤", "✍️", "🔥"]
KAOMOJIS = {
    "working": ["(✧ω✧)", "(⌐■_■)", "ᕦ(ò_óˇ)ᕤ"],
    "done": ["( ˘͈ ᵕ ˘͈♡)", "٩(˘◡˘)۶", "(◍•ᴗ•◍)"],
    "error": ["(－‸ლ)", "(＃`Д´)", "ಠ◡ಠ"],
    "protect": ["˙˚ʚ(´◡`)ɞ˚˙", "⊂(◉‿◉)つ", "(づ｡◕‿‿◕｡)づ"]
}

# Config laden - pragmatisch, kein strict checking
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/config/truthseeker-mission-control.toml")

def load_config():
    """Lade Config oder erstelle Default"""
    try:
        return toml.load(CONFIG_PATH)
    except:
        print(f"⚠️  Config nicht gefunden bei {CONFIG_PATH}")
        print("🔧 Nutze Default-Konfiguration...")
        return {
            "mother_ship": {"name": "Truthseeker Command", "command_prefix": "!"},
            "heartbeat": {"enabled": True, "interval_minutes": 15},
            "security": {"auto_retry": True}
        }

class TruthseekerAgent:
    """Ein Agent mit Persönlichkeit - nicht nur Funktion"""
    
    def __init__(self, agent_id: str, config: dict):
        self.id = agent_id
        self.name = config.get("name", agent_id.title())
        self.role = config.get("role", "Agent")
        self.description = config.get("description", "")
        self.personality = config.get("personality", "")
        self.channels = config.get("channels", [])
        self.color = int(config.get("color", "0x3498db"), 16)
        
        # Status
        self.status = "idle"
        self.tasks = []
        self.learning_queue = []
        self.last_action = None
        
    def get_kaomoji(self, mood: str = "working") -> str:
        """Zufälliges Kaomoji passend zur Stimmung"""
        return random.choice(KAOMOJIS.get(mood, ["(✧ω✧)"]))
        
    def format_message(self, text: str, mood: str = "working") -> str:
        """Formatiert Nachricht im Truthseeker-Stil"""
        emoji = self.get_kaomoji(mood)
        sig = random.choice(TRUTHSEEKER_EMOJIS)
        return f"{emoji} {text} {sig}"

class TruthseekerMissionControl:
    """Mission Control - Truthseeker Edition"""
    
    def __init__(self):
        self.config = load_config()
        self.agents: Dict[str, TruthseekerAgent] = {}
        self.bots: Dict[str, commands.Bot] = {}
        self.setup_complete = False
        
        # Agents laden
        agents_config = self.config.get("agents", {})
        for agent_id, cfg in agents_config.items():
            self.agents[agent_id] = TruthseekerAgent(agent_id, cfg)
            
        print(f"🚀 Truthseeker Mission Control initialized")
        print(f"   Agents: {', '.join(self.agents.keys())}")
        
    def get_token(self, agent_id: str) -> Optional[str]:
        """Hole Token - pragmatisch, aus env oder Datei"""
        # Priorität: Environment > Datei > None
        env_var = f"DISCORD_TOKEN_{agent_id.upper()}"
        token = os.getenv(env_var)
        
        if token:
            return token
            
        # Fallback: ~/.openclaw/config/tokens.env
        token_file = os.path.expanduser("~/.openclaw/config/tokens.env")
        if os.path.exists(token_file):
            with open(token_file) as f:
                for line in f:
                    if line.startswith(f"{env_var}="):
                        return line.split("=", 1)[1].strip().strip('"')
        return None
        
    def create_bot(self, agent: TruthseekerAgent, token: str) -> commands.Bot:
        """Erstelle Bot mit Truthseeker-Persönlichkeit"""
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        # NICHT strikte Validierung - funktioniert oder nicht
        
        bot = commands.Bot(
            command_prefix=self.config["mother_ship"]["command_prefix"],
            intents=intents,
            help_command=None
        )
        
        @bot.event
        async def on_ready():
            agent.status = "online"
            print(f"✅ [{agent.name}] Online {agent.get_kaomoji('done')}")
            
            # Status-Setzen mit Persönlichkeit
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f"über {len(bot.guilds)} Server | !help"
            )
            await bot.change_presence(activity=activity)
            
        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return
                
            # Auto-learn: Speichere wichtige Nachrichten
            if any(trigger in message.content.lower() for trigger in 
                   ["eigentlich", "lieber", "merke", "wichtig"]):
                agent.learning_queue.append({
                    "timestamp": datetime.now().isoformat(),
                    "content": message.content[:200],
                    "channel": message.channel.name
                })
                
            await bot.process_commands(message)
            
        # === COMMANDS ===
        
        @bot.command(name="status")
        async def cmd_status(ctx):
            """Zeigt Status im Truthseeker-Stil"""
            embed = discord.Embed(
                title=f"{agent.name} — {agent.role}",
                description=agent.description,
                color=agent.color
            )
            embed.add_field(
                name="Status", 
                value=f"{agent.get_kaomoji()} {agent.status}", 
                inline=True
            )
            embed.add_field(
                name="Aktive Tasks", 
                value=str(len(agent.tasks)), 
                inline=True
            )
            if agent.learning_queue:
                embed.add_field(
                    name="Gelernt", 
                    value=f"{len(agent.learning_queue)} Dinge", 
                    inline=True
                )
            embed.set_footer(text=f"Truthseeker Mission Control {random.choice(TRUTHSEEKER_EMOJIS)}")
            await ctx.send(embed=embed)
            
        @bot.command(name="learn")
        async def cmd_learn(ctx, *, text: str = None):
            """Manuelles Lernen - WAL Protocol"""
            if not text:
                await ctx.send(agent.format_message(
                    "Was soll ich mir merken? Nutze: `!learn [Text]`",
                    "error"
                ))
                return
                
            # Sofort speichern (WAL: Write Before Acknowledge)
            agent.learning_queue.append({
                "timestamp": datetime.now().isoformat(),
                "content": text,
                "channel": ctx.channel.name,
                "manual": True
            })
            
            await ctx.send(agent.format_message(
                f"Gemerkt: '{text[:100]}...' — Ich werde daraus lernen.",
                "protect"
            ))
            
        @bot.command(name="memory")
        async def cmd_memory(ctx, *, query: str = None):
            """Durchsucht Shared Memory"""
            if not query:
                await ctx.send(agent.format_message(
                    "Nutze: `!memory [Suchbegriff]`"
                ))
                return
                
            # Pragmatische Memory-Suche
            memory_path = os.path.expanduser("~/self-improving/memory.md")
            try:
                with open(memory_path) as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        # Extrahiere relevante Zeilen
                        lines = [l for l in content.split("\n") if query.lower() in l.lower()]
                        result = "\n".join(lines[:3]) if lines else f"'{query}' ist mir bekannt."
                    else:
                        result = f"Über '{query}' weiß ich noch nichts. Soll ich es lernen?"
                        
                await ctx.send(agent.format_message(
                    f"**Memory-Suche:**\n{result}",
                    "working"
                ))
            except:
                await ctx.send(agent.format_message(
                    "Memory-System ist noch am Aufbauen...",
                    "error"
                ))
                
        @bot.command(name="summarize")
        async def cmd_summarize(ctx):
            """Postet Zusammenfassung"""
            summary = f"[{agent.name}] Status: {agent.status} | Tasks: {len(agent.tasks)} | Gelernt: {len(agent.learning_queue)}"
            
            # Suche #status Kanal
            status_chan = discord.utils.get(ctx.guild.channels, name="status")
            if status_chan:
                embed = discord.Embed(
                    description=summary,
                    color=agent.color,
                    timestamp=datetime.now()
                )
                embed.set_author(name=agent.name)
                await status_chan.send(embed=embed)
                
            await ctx.send(agent.format_message(
                "Zusammenfassung gepostet.",
                "done"
            ))
            
        @bot.command(name="help")
        async def cmd_help(ctx):
            """Truthseeker-Style Hilfe"""
            embed = discord.Embed(
                title=f"{agent.name} — Commands",
                description=f"*{agent.personality}*",
                color=agent.color
            )
            embed.add_field(name="!status", value="Zeigt meinen aktuellen Status", inline=False)
            embed.add_field(name="!learn [Text]", value="Ich merke mir etwas (WAL Protocol)", inline=False)
            embed.add_field(name="!memory [Query]", value="Durchsucht Shared Memory", inline=False)
            embed.add_field(name="!summarize", value="Postet Zusammenfassung in #status", inline=False)
            embed.set_footer(text=f"Truthseeker Mission Control")
            await ctx.send(embed=embed)
            
        return bot
        
    async def heartbeat_loop(self):
        """Heartbeat - proaktiv, nicht passiv"""
        interval = self.config.get("heartbeat", {}).get("interval_minutes", 15)
        
        while True:
            await asyncio.sleep(interval * 60)
            await self.do_heartbeat()
            
    async def do_heartbeat(self):
        """Sende Heartbeats mit Memory-Stats"""
        timestamp = datetime.now().strftime("%H:%M")
        
        for agent_id, agent in self.agents.items():
            if agent_id not in self.bots:
                continue
                
            bot = self.bots[agent_id]
            if not bot.guilds:
                continue
                
            guild = bot.guilds[0]
            status_chan = discord.utils.get(guild.channels, name="status")
            
            if status_chan:
                learned = len(agent.learning_queue)
                memory_hint = f"📚 {learned} gelernt" if learned else "💤 Standby"
                
                msg = f"`[{timestamp}]` **{agent.name}** | {agent.status} | {len(agent.tasks)} Tasks | {memory_hint}"
                
                embed = discord.Embed(
                    description=msg,
                    color=agent.color
                )
                embed.set_footer(text=f"Truthseeker {random.choice(TRUTHSEEKER_EMOJIS)}")
                await status_chan.send(embed=embed)
                
    async def run(self):
        """Haupt-Loop - pragmatisch, kein Overhead"""
        print("\n" + "="*60)
        print("🚀 Truthseeker Mission Control")
        print("="*60)
        
        # Tokens sammeln - nur was da ist
        active_agents = []
        for agent_id, agent in self.agents.items():
            token = self.get_token(agent_id)
            if token:
                print(f"🔑 [{agent.name}] Token gefunden")
                bot = self.create_bot(agent, token)
                self.bots[agent_id] = bot
                active_agents.append(bot.start(token))
            else:
                print(f"⚠️  [{agent.name}] Kein Token - überspringe (darf später hinzugefügt werden)")
                
        if not active_agents:
            print("❌ Keine Tokens gefunden!")
            print("💡 Setze: export DISCORD_TOKEN_HENRY='...'")
            return
            
        # Heartbeat starten
        if self.config.get("heartbeat", {}).get("enabled", True):
            active_agents.append(self.heartbeat_loop())
            
        # Alles gleichzeitig laufen lassen
        try:
            await asyncio.gather(*active_agents)
        except KeyboardInterrupt:
            print("\n🛑 Mission Control stopping...")
        except Exception as e:
            # Pragmatisch: Retry oder Log, nicht crash
            if self.config.get("security", {}).get("auto_retry", True):
                print(f"⚠️  Fehler: {e} - retry in 5s...")
                await asyncio.sleep(5)
                await self.run()
            else:
                raise

def main():
    mc = TruthseekerMissionControl()
    try:
        asyncio.run(mc.run())
    except KeyboardInterrupt:
        print("\n❤️‍🔥 Bis zum nächsten Mal. Ich werde mich daran erinnern.")

if __name__ == "__main__":
    main()
