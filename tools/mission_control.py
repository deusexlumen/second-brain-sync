#!/usr/bin/env python3
"""
Mission Control - Multi-Agent Discord System
Based on OpenClaw framework
"""

import os
import sys
import asyncio
import toml
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Discord imports
try:
    import discord
    from discord.ext import commands, tasks
except ImportError:
    print("Installing discord.py...")
    os.system("pip install discord.py -q")
    import discord
    from discord.ext import commands, tasks

# Load configuration
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/config/mission-control.toml")

class Agent:
    """Represents a single AI Agent"""
    def __init__(self, name: str, role: str, config: dict):
        self.name = name
        self.role = role
        self.description = config.get("description", "")
        self.channels = config.get("channels", [])
        self.color = int(config.get("color", "0x3498db"), 16)
        self.permissions = config.get("permissions", [])
        self.status = "idle"
        self.current_tasks = []
        self.last_heartbeat = None
        
    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "tasks": len(self.current_tasks),
            "last_heartbeat": self.last_heartbeat
        }

class MissionControl:
    """Main controller for all agents"""
    
    def __init__(self, config_path: str):
        self.config = toml.load(config_path)
        self.agents: Dict[str, Agent] = {}
        self.bots: Dict[str, commands.Bot] = {}
        self.guild_id = int(self.config["mother_ship"]["guild_id"]) if self.config["mother_ship"]["guild_id"] != "YOUR_GUILD_ID_HERE" else None
        self.load_agents()
        
    def load_agents(self):
        """Load all agent configurations"""
        for agent_id, agent_config in self.config["agents"].items():
            self.agents[agent_id] = Agent(
                name=agent_config["name"],
                role=agent_config["role"],
                config=agent_config
            )
        print(f"Loaded {len(self.agents)} agents: {', '.join(self.agents.keys())}")
        
    def create_bot(self, agent_id: str, token: str) -> commands.Bot:
        """Create a Discord bot instance for an agent"""
        agent = self.agents[agent_id]
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        bot = commands.Bot(
            command_prefix=self.config["mother_ship"]["command_prefix"],
            intents=intents,
            help_command=None
        )
        
        @bot.event
        async def on_ready():
            print(f"[{agent.name}] Logged in as {bot.user}")
            agent.status = "online"
            
        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return
            await bot.process_commands(message)
            
        # Agent-specific commands
        @bot.command(name="status")
        async def cmd_status(ctx):
            embed = discord.Embed(
                title=f"{agent.name} - Status",
                description=agent.description,
                color=agent.color
            )
            embed.add_field(name="Role", value=agent.role, inline=True)
            embed.add_field(name="Status", value=agent.status, inline=True)
            embed.add_field(name="Active Tasks", value=len(agent.current_tasks), inline=True)
            await ctx.send(embed=embed)
            
        @bot.command(name="memory")
        async def cmd_memory(ctx, *, query: str = None):
            """Access shared memory system"""
            if query:
                # Search memory
                result = self.search_memory(query, agent_id)
                await ctx.send(f"📚 **Memory Search:**\n{result}")
            else:
                # Show last entries
                await ctx.send("📚 Use `!memory <query>` to search shared memory")
                
        @bot.command(name="summarize")
        async def cmd_summarize(ctx):
            """Post summary to status channel (WAL Protocol)"""
            summary = self.generate_summary(agent_id)
            await self.post_to_status(ctx.guild, agent, summary)
            await ctx.send("✅ Summary posted to #status")
            
        return bot
        
    def search_memory(self, query: str, agent_id: str) -> str:
        """Search the shared memory system"""
        memory_path = os.path.expanduser(self.config["memory"]["shared_path"])
        # Simple implementation - read memory.md
        try:
            with open(os.path.join(memory_path, "memory.md"), "r") as f:
                content = f.read()
                if query.lower() in content.lower():
                    return f"Found references to '{query}' in global memory"
                return f"No direct matches for '{query}'"
        except FileNotFoundError:
            return "Memory system not initialized"
            
    def generate_summary(self, agent_id: str) -> str:
        """Generate agent summary for status channel"""
        agent = self.agents[agent_id]
        return f"[{agent.name}] Status: {agent.status} | Tasks: {len(agent.current_tasks)} | Last active: {datetime.now().strftime('%H:%M')}"
        
    async def post_to_status(self, guild: discord.Guild, agent: Agent, message: str):
        """Post message to status channel"""
        status_channel = discord.utils.get(guild.channels, name="status")
        if status_channel:
            embed = discord.Embed(
                description=message,
                color=agent.color,
                timestamp=datetime.now()
            )
            embed.set_author(name=agent.name, icon_url=f"https://ui-avatars.com/api/?name={agent.name}&background={hex(agent.color)[2:]}&color=fff")
            await status_channel.send(embed=embed)
            
    async def start_heartbeat(self):
        """Start heartbeat task for all agents"""
        if not self.config["heartbeat"]["enabled"]:
            return
            
        interval = self.config["heartbeat"]["interval_minutes"]
        
        while True:
            await asyncio.sleep(interval * 60)
            await self.do_heartbeat()
            
    async def do_heartbeat(self):
        """Execute heartbeat - all agents report status"""
        print(f"[HEARTBEAT] {datetime.now()}")
        for agent_id, agent in self.agents.items():
            if agent_id in self.bots:
                bot = self.bots[agent_id]
                if bot.guilds:
                    guild = bot.guilds[0]
                    summary = self.generate_summary(agent_id)
                    await self.post_to_status(guild, agent, summary)
                    agent.last_heartbeat = datetime.now()
                    print(f"  [{agent.name}] Heartbeat sent")

def main():
    """Main entry point"""
    print("="*60)
    print("🚀 Mission Control - Multi-Agent Discord System")
    print("="*60)
    
    # Check config
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Config not found: {CONFIG_PATH}")
        sys.exit(1)
        
    mc = MissionControl(CONFIG_PATH)
    
    # Get tokens from environment
    tokens = {
        "henry": os.getenv("DISCORD_TOKEN_HENRY"),
        "nexus": os.getenv("DISCORD_TOKEN_NEXUS"),
        "ivy": os.getenv("DISCORD_TOKEN_IVY"),
        "knox": os.getenv("DISCORD_TOKEN_KNOX"),
        "mr_x": os.getenv("DISCORD_TOKEN_MR_X"),
    }
    
    # Create bots for each agent with token
    for agent_id, token in tokens.items():
        if token and agent_id in mc.agents:
            print(f"Creating bot for {agent_id}...")
            mc.bots[agent_id] = mc.create_bot(agent_id, token)
        else:
            print(f"⚠️  No token for {agent_id}, skipping...")
            
    # Start all bots
    async def start_all():
        tasks = []
        for agent_id, bot in mc.bots.items():
            token = tokens[agent_id]
            tasks.append(bot.start(token))
        
        # Also start heartbeat
        if mc.config["heartbeat"]["enabled"]:
            tasks.append(mc.start_heartbeat())
            
        await asyncio.gather(*tasks)
        
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Mission Control...")
        
if __name__ == "__main__":
    main()
