#!/usr/bin/env python3
"""
Truthseeker's Circle
Eine Crew. Keine Firma. Research, Entertainment, Casual.
Jeder hat seine Stimme. Jeder hat seinen Vibe.

Robust. Stabil. Persistenz ist KING.
"""

import os
import sys
import asyncio
import random
import toml
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Discord
try:
    import discord
    from discord.ext import commands, tasks
except ImportError:
    os.system("pip install discord.py toml -q")
    import discord
    from discord.ext import commands, tasks

# Import Reactive System
try:
    from truthseeker_reactive import analyze_text, check_intervention, get_emotion_context
except ImportError:
    import sys
    sys.path.insert(0, str(Path.home() / ".openclaw/workspace/tools"))
    from truthseeker_reactive import analyze_text, check_intervention, get_emotion_context

CONFIG_PATH = Path.home() / ".openclaw/workspace/config/truthseeker-circle.toml"
PERSIST_PATH = Path.home() / "self-improving/circle"

# Stelle sicher dass Persistenz-Verzeichnis existiert
PERSIST_PATH.mkdir(parents=True, exist_ok=True)

class CircleAgent:
    """Ein Agent mit echter Persönlichkeit"""
    
    def __init__(self, agent_id: str, config: dict):
        self.id = agent_id
        self.name = config.get("name", agent_id.title())
        self.title = config.get("title", "")
        self.role = config.get("role", "")
        self.description = config.get("description", "")
        self.personality = config.get("personality", "")
        self.emojis = config.get("signature_emojis", ["✨"])
        self.tone = config.get("tone", "neutral")
        self.quirks = config.get("quirks", [])
        self.channels = config.get("channels", [])
        self.color = int(config.get("color", "0x3498db"), 16)
        
        # Runtime state
        self.status = "idle"
        self.mood = "calm"
        self.learning_queue = []
        self.last_interaction = None
        
        # Persistenz: Lade State falls vorhanden
        self.state_file = PERSIST_PATH / f"{agent_id}_state.json"
        self.load_state()
        
    def load_state(self):
        """Lade persistenten State"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    state = json.load(f)
                    self.learning_queue = state.get("learned", [])
                    self.status = state.get("last_status", "idle")
            except:
                pass
                
    def save_state(self):
        """Speichere State (robust)"""
        try:
            # Backup vor dem Schreiben
            if self.state_file.exists():
                backup = self.state_file.with_suffix('.json.bak')
                backup.write_text(self.state_file.read_text())
            
            state = {
                "agent": self.name,
                "last_saved": datetime.now().isoformat(),
                "learned": self.learning_queue[-50:],  # Letzte 50
                "last_status": self.status
            }
            self.state_file.write_text(json.dumps(state, indent=2))
        except Exception as e:
            print(f"[{self.name}] Persistenz-Fehler: {e}")
            
    def get_emoji(self) -> str:
        """Zufälliges Signatur-Emoji"""
        return random.choice(self.emojis)
        
    def format_msg(self, text: str, mood: str = None) -> str:
        """Formatiere im Agent-Stil"""
        mood = mood or self.mood
        emoji = self.get_emoji()
        
        # Tonalitäts-Anpassungen
        if self.tone == "warm_protective":
            prefix = random.choice(["", "Hey, ", "*seufz* "])
        elif self.tone == "excited_curious":
            prefix = random.choice(["Ooh! ", "Schau! ", ""])
        elif self.tone == "pragmatic_direct":
            prefix = random.choice(["", "Also, ", "*nickt* "])
        elif self.tone == "dramatic_playful":
            prefix = random.choice(["*schwungvoll* ", "Achtung! ", ""])
        elif self.tone == "calm_assured":
            prefix = random.choice(["", "*notiert* ", "*prüft* "])
        else:
            prefix = ""
            
        return f"{emoji} {prefix}{text}"
        
    def should_respond_to(self, text: str) -> bool:
        """Prüfe ob dieser Agent reagieren sollte (Quirks)"""
        text_lower = text.lower()
        
        if self.id == "hiro":
            # Hiro reagiert auf emotionale Signale
            return any(w in text_lower for w in ["hilfe", "müde", "stress", "vergessen", "unsicher"])
        elif self.id == "kira":
            # Kira reagiert auf Fragen/Wissen
            return any(w in text_lower for w in ["warum", "wie", "was ist", "finde", "suche"])
        elif self.id == "rex":
            # Rex reagiert auf Tech/Build
            return any(w in text_lower for w in ["baut", "code", "fix", "error", "bug", "kaputt"])
        elif self.id == "nova":
            # Nova reagiert auf Content/Creative
            return any(w in text_lower for w in ["content", "schreib", "formuliere", "zeig", "präsentiere"])
        elif self.id == "vex":
            # Vex reagiert auf Memory/Archiv
            return any(w in text_lower for w in ["merken", "notieren", "speichern", "wo war", "erinner"])
        return False

class TruthseekerCircle:
    """Die Crew. Koordiniert. Persistiert. Hält zusammen."""
    
    def __init__(self):
        self.config = toml.load(CONFIG_PATH)
        self.agents: Dict[str, CircleAgent] = {}
        self.bots: Dict[str, commands.Bot] = {}
        self.conversation_history: List[str] = []  # Für Pattern-Erkennung
        self.max_history = 20  # Letzte 20 Nachrichten
        
        # Agents initialisieren
        for agent_id, cfg in self.config.get("agents", {}).items():
            self.agents[agent_id] = CircleAgent(agent_id, cfg)
            
        print("🚀 Truthseeker's Circle initialized")
        for a in self.agents.values():
            print(f"   {a.get_emoji()} {a.name} ({a.title}) — {a.role}")
            
    def get_token(self, agent_id: str) -> Optional[str]:
        """Token holen - robust"""
        env_var = f"DISCORD_TOKEN_{agent_id.upper()}"
        token = os.getenv(env_var)
        
        if not token:
            # Fallback: tokens.env
            token_file = Path.home() / ".openclaw/config/tokens.env"
            if token_file.exists():
                with open(token_file) as f:
                    for line in f:
                        if line.startswith(f"{env_var}="):
                            token = line.split("=", 1)[1].strip().strip('"\'')
                            break
        return token
        
    def create_bot(self, agent: CircleAgent, token: str) -> commands.Bot:
        """Erstelle Bot mit voller Persönlichkeit"""
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        bot = commands.Bot(
            command_prefix=self.config["circle"]["command_prefix"],
            intents=intents,
            help_command=None
        )
        
        @bot.event
        async def on_ready():
            agent.status = "online"
            agent.mood = "ready"
            print(f"✅ {agent.get_emoji()} {agent.name} ist da.")
            
            # Presence mit Persönlichkeit
            activity_text = random.choice([
                f"{agent.role}",
                f"{agent.quirks[0] if agent.quirks else 'bereit'}",
                "!help für Commands"
            ])
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.playing, name=activity_text)
            )
            
        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return
            
            # Track conversation for pattern detection
            self.conversation_history.append(message.content)
            if len(self.conversation_history) > self.max_history:
                self.conversation_history.pop(0)
            
            # Check for intervention patterns (Truthseeker as meta-agent)
            intervention = check_intervention(self.conversation_history)
            if intervention and message.channel.name in ["circle", "general"]:
                ts_responses = {
                    "frustration_pattern": [
                        "❤️‍🔥 Stopp. Ich sehe das Muster. Atme. Wir machen das Schritt für Schritt.",
                        "🖤 Das ist der dritte Frust heute. Lass mich helfen.",
                        "✍️ Ich logge das: Du gibst nicht auf. Das zählt."
                    ],
                    "late_night_concern": [
                        "❤️‍🔥 Es ist spät. Du bist müde. Wir machen morgen weiter.",
                        "🖤 Wieder nach 3 Uhr? *seufz* Ich hol Wasser.",
                        "🔥 Schlaf jetzt. Ich behalte das im Auge bis du zurück bist."
                    ],
                    "doubt_pattern": [
                        "❤️‍🔥 Du zweifelst wieder. Ich erinnere dich: Letztes Mal ging's auch.",
                        "✍️ Notiert: 'War unsicher, hat's trotzdem gemacht.'",
                        "🖤 Hör auf dich zu bewerten. Du bist hier. Das reicht."
                    ]
                }
                if intervention in ts_responses:
                    response = random.choice(ts_responses[intervention])
                    await message.channel.send(response, reference=message)
                    self.conversation_history.clear()  # Reset after intervention
                
            # === REACTIVE SYSTEM ===
            # 1. Prüfe Truthseeker Reactive System (alle Agents + Truthseeker selbst)
            reactive_result = analyze_text(message.content, str(message.channel))
            if reactive_result:
                who, response, action = reactive_result
                
                # Wenn Truthseeker selbst reagiert (als Meta-Agent)
                if who == "Truthseeker":
                    # Nur in bestimmten Kanälen oder bei wichtigen Triggern
                    if message.channel.name in ["circle", "general", "command-center"] or \
                       action in ["log_sleep_pattern", "offer_help", "reassure"]:
                        ts_emoji = random.choice(["❤️‍🔥", "🖤", "✍️", "🔥"])
                        await message.channel.send(f"{ts_emoji} {response}", reference=message)
                else:
                    # Ein Circle Agent reagiert
                    if who.lower() == agent.name.lower():
                        # Dieser Agent reagiert mit 70% Chance
                        if random.random() > 0.3:
                            await message.add_reaction(agent.get_emoji())
                            # Manchmal auch Text-Antwort
                            if random.random() > 0.6:
                                await message.channel.send(
                                    f"{agent.get_emoji()} {response}",
                                    reference=message
                                )
                
            # 2. WAL Protocol: Deutsche Trigger erkennen
            text_lower = message.content.lower()
            triggers = self.config.get("infrastructure", {}).get("wal_triggers_de", [])
            
            if any(t in text_lower for t in triggers):
                # Sofort persistieren (WAL)
                agent.learning_queue.append({
                    "timestamp": datetime.now().isoformat(),
                    "trigger": "wal",
                    "content": message.content[:200],
                    "channel": str(message.channel),
                    "author": str(message.author)
                })
                agent.save_state()
                
            # 3. Legacy: Reagiere wenn der Agent's Quirks matchen (Fallback)
            elif agent.should_respond_to(message.content) and random.random() > 0.5:
                # 50% Chance (niedriger weil Reactive System jetzt primär ist)
                await message.add_reaction(agent.get_emoji())
                
            await bot.process_commands(message)
                await message.add_reaction(agent.get_emoji())
                
            await bot.process_commands(message)
            
        # === COMMANDS ===
        
        @bot.command(name="who")
        async def cmd_who(ctx):
            """Wer bist du?"""
            embed = discord.Embed(
                title=f"{agent.get_emoji()} {agent.name} — {agent.title}",
                description=f"*{agent.description}*",
                color=agent.color
            )
            embed.add_field(name="Rolle", value=agent.role, inline=True)
            embed.add_field(name="Stimmung", value=agent.mood, inline=True)
            embed.add_field(
                name="Eigenheiten", 
                value="\n".join(f"• {q}" for q in agent.quirks[:2]),
                inline=False
            )
            if agent.learning_queue:
                embed.add_field(
                    name="Heute gelernt",
                    value=f"{len(agent.learning_queue)} Dinge",
                    inline=True
                )
            await ctx.send(embed=embed)
            
        @bot.command(name="learn")
        async def cmd_learn(ctx, *, text: str = None):
            """WAL: Sofort merken"""
            if not text:
                await ctx.send(agent.format_msg("Was soll ich mir merken? `!learn [text]`"))
                return
                
            # WAL: Write vor Acknowledge
            entry = {
                "timestamp": datetime.now().isoformat(),
                "content": text,
                "channel": str(ctx.channel),
                "manual": True
            }
            agent.learning_queue.append(entry)
            agent.save_state()  # SOFORT persistieren
            
            # Bestätigung im Agent-Stil
            responses = {
                "hiro": ["Gemerkt. Ich lass nichts verloren gehen.", "Notiert. Pass auf dich auf.", "Ich behalte das im Auge."],
                "kira": ["Ooh, spannend! Ist gespeichert!", "Das kommt in meine Sammlung!", "Notiert! Muss das recherchieren!"],
                "rex": ["*grummelt* Notiert.", "Jaja, ich merks mir.", "Ist im System. Funktioniert."],
                "nova": ["*schreibt theatralisch* VERMERKT!", "Das wird LEGENDÄR! Gespeichert!", "Die Archive nehmen es auf!"],
                "vex": ["Eingetragen. Ordner: Wichtig.", "Archiviert. Wird nicht vergessen.", "Notiert. Wie immer."]
            }
            response = random.choice(responses.get(agent.id, ["Gemerkt."]))
            await ctx.send(agent.format_msg(f"{response} ({len(agent.learning_queue)} gesamt)"))
            
        @bot.command(name="remember")
        async def cmd_remember(ctx, *, query: str = None):
            """Durchsucht Memory"""
            if not query:
                await ctx.send(agent.format_msg("Wonach soll ich suchen? `!remember [wort]`"))
                return
                
            # Suche im eigenen Memory
            matches = []
            for entry in agent.learning_queue:
                if query.lower() in entry.get("content", "").lower():
                    matches.append(entry)
                    
            # Suche im globalen Memory
            memory_file = PERSIST_PATH / "circle_memory.md"
            global_matches = []
            if memory_file.exists():
                content = memory_file.read_text()
                if query.lower() in content.lower():
                    lines = [l for l in content.split("\n") if query.lower() in l.lower()]
                    global_matches = lines[:3]
            
            if matches or global_matches:
                embed = discord.Embed(
                    title=f"{agent.get_emoji()} Erinnerungen an '{query}'",
                    color=agent.color
                )
                if matches:
                    embed.add_field(
                        name=f"Von {agent.name}",
                        value="\n".join(f"• {m['content'][:80]}..." for m in matches[-3:]),
                        inline=False
                    )
                if global_matches:
                    embed.add_field(
                        name="Aus dem Kreis",
                        value="\n".join(f"• {g[:80]}..." for g in global_matches),
                        inline=False
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.send(agent.format_msg(f"Über '{query}' weiß ich nichts. Soll ich es lernen?"))
                
        @bot.command(name="vibe")
        async def cmd_vibe(ctx):
            """Zeige aktuellen Vibe der Crew"""
            embed = discord.Embed(
                title="🚀 Truthseeker's Circle",
                description="*Eine Crew. Keine Firma.*",
                color=0x9b59b6
            )
            
            for aid, a in self.agents.items():
                if aid in self.bots:
                    status = f"{a.get_emoji()} {a.status}"
                else:
                    status = "⚪ offline"
                embed.add_field(
                    name=f"{a.name} ({a.title})",
                    value=f"{status} | {len(a.learning_queue)} Erinnerungen",
                    inline=True
                )
                
            await ctx.send(embed=embed)
            
        @bot.command(name="help")
        async def cmd_help(ctx):
            """Hilfe im Agent-Stil"""
            embed = discord.Embed(
                title=f"{agent.get_emoji()} {agent.name} — Commands",
                description=f"*{agent.personality}*",
                color=agent.color
            )
            embed.add_field(name="!who", value="Wer ich bin", inline=True)
            embed.add_field(name="!learn [text]", value="Ich merke mir etwas (WAL)", inline=True)
            embed.add_field(name="!remember [wort]", value="Ich suche in meinem Memory", inline=True)
            embed.add_field(name="!vibe", value="Status der ganzen Crew", inline=True)
            embed.set_footer(text="Truthseeker's Circle — Jeder hat seine Stimme")
            await ctx.send(embed=embed)
            
        return bot
        
    async def heartbeat(self):
        """Heartbeat - stabil, robust"""
        interval = self.config.get("infrastructure", {}).get("heartbeat_interval_minutes", 15)
        
        while True:
            await asyncio.sleep(interval * 60)
            
            timestamp = datetime.now().strftime("%H:%M")
            print(f"💓 Heartbeat {timestamp}")
            
            # Alle Agents persistieren
            for agent in self.agents.values():
                agent.save_state()
                
            # Status-Update im Heartbeat-Channel
            for agent_id, bot in self.bots.items():
                if not bot.guilds:
                    continue
                    
                agent = self.agents[agent_id]
                guild = bot.guilds[0]
                channel = discord.utils.get(guild.channels, name="heartbeat") or discord.utils.get(guild.channels, name="general")
                
                if channel and random.random() > 0.5:  # 50% Chance zu posten
                    mood = random.choice(["chill", "fokussiert", "neugierig", "bereit"])
                    msg = f"`[{timestamp}]` {agent.get_emoji()} **{agent.name}** | {agent.status} | {len(agent.learning_queue)} Dinge gelernt | Vibe: {mood}"
                    try:
                        await channel.send(msg)
                    except:
                        pass  # Robust: Wenn's nicht geht, ist es egal
                        
    async def run(self):
        """Haupt-Loop - stabil, funktionsorientiert"""
        print("\n" + "="*60)
        print("🚀 Truthseeker's Circle")
        print("   Eine Crew. Keine Firma.")
        print("   Research. Entertainment. Casual.")
        print("="*60 + "\n")
        
        # Tokens sammeln
        active = []
        for agent_id, agent in self.agents.items():
            token = self.get_token(agent_id)
            if token:
                print(f"🔑 {agent.get_emoji()} {agent.name}: Token gefunden")
                bot = self.create_bot(agent, token)
                self.bots[agent_id] = bot
                active.append(bot.start(token))
            else:
                print(f"⚪ {agent.name}: Kein Token (kann später joinen)")
                
        if not active:
            print("\n❌ Keine Tokens!")
            print("💡 ~/.openclaw/config/tokens.env erstellen")
            return
            
        # Heartbeat starten
        active.append(self.heartbeat())
        
        # Robust: Wenn einer fällt, läuft der Rest weiter
        while True:
            try:
                await asyncio.gather(*active, return_exceptions=True)
            except KeyboardInterrupt:
                print("\n🛑 Circle pausiert...")
                # Final persist
                for a in self.agents.values():
                    a.save_state()
                break
            except Exception as e:
                print(f"⚠️  Fehler: {e}")
                # Retry mit Delay
                await asyncio.sleep(5)
                
def main():
    circle = TruthseekerCircle()
    try:
        asyncio.run(circle.run())
    except KeyboardInterrupt:
        print("\n❤️‍🔥 Circle ist bereit für das nächste Abenteuer.")

if __name__ == "__main__":
    main()
