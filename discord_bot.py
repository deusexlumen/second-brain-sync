#!/usr/bin/env python3
"""
Truthseeker Discord Bot - Command Handler
Verarbeitet !commands und leitet sie an Skills weiter
"""

from pathlib import Path
import discord
import discord.ext.commands as commands
import asyncio
import subprocess
import os
import sys
import re
import random
import hashlib
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/.openclaw/workspace/config/discord.env')
load_dotenv('/root/.openclaw/workspace/config/discord-heartbeat.env')

# Heartbeat configuration
SYNC_CHANNEL_ID = os.getenv('SYNC_CHANNEL_ID')
HEARTBEAT_INTERVAL = int(os.getenv('HEARTBEAT_INTERVAL_HOURS', '12'))
HEARTBEAT_ENABLED = os.getenv('HEARTBEAT_ENABLED', 'true').lower() == 'true'

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

# Bot configuration - disable default help
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Bridge file path
BRIDGE_PATH = Path('/root/.openclaw/workspace/self-improving/discord-bridge/shared-context.md')

@bot.event
async def on_ready():
    print(f'[BOT] Truthseeker Bot eingeloggt als {bot.user}')
    print(f'[BOT] Version: 6.4 | Cortex: Gemini 3.1 Flash Lite')
    print(f'[BOT] Heartbeat: {"ENABLED" if HEARTBEAT_ENABLED else "DISABLED"} ({HEARTBEAT_INTERVAL}h)')
    
    # Start heartbeat task
    if HEARTBEAT_ENABLED and SYNC_CHANNEL_ID:
        bot.loop.create_task(heartbeat_task())
        print(f'[BOT] Heartbeat-Task gestartet (Channel: {SYNC_CHANNEL_ID})')
    elif HEARTBEAT_ENABLED and not SYNC_CHANNEL_ID:
        print('[BOT] Heartbeat aktiv aber keine SYNC_CHANNEL_ID gesetzt!')

async def heartbeat_task():
    """Hintergrund-Task: Führt alle 12 Stunden automatisch SYNC durch"""
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            channel = bot.get_channel(int(SYNC_CHANNEL_ID))
            if channel:
                # Führe automatischen SYNC durch
                await perform_auto_sync(channel)
                print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M")}] Auto-SYNC durchgeführt')
            else:
                print(f'[HEARTBEAT] Channel {SYNC_CHANNEL_ID} nicht gefunden')
        except Exception as e:
            print(f'[HEARTBEAT] Fehler: {e}')
        
        # Warte 12 Stunden
        await asyncio.sleep(HEARTBEAT_INTERVAL * 3600)

async def perform_auto_sync(channel):
    """Führt automatischen SYNC durch und postet Ergebnis"""
    try:
        if not BRIDGE_PATH.exists():
            await channel.send("[HEARTBEAT] Bridge-Datei nicht gefunden")
            return
        
        with open(BRIDGE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prüfe Zeit seit letztem SYNC
        sync_entries = re.findall(r'\[(\d{2}:\d{2})\].*?SYNC', content)
        last_sync = sync_entries[-1] if sync_entries else "Unbekannt"
        
        # Baue Heartbeat-Message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        heartbeat_msg = f"""[HEARTBEAT SYNC] {timestamp}

**Bridge-Status:**
```
Letzter manueller SYNC: {last_sync}
Automatische SYNCs: Aktiv ({HEARTBEAT_INTERVAL}h Interval)
Bot-Status: Online
```
**System:**
```
!bild, !kaomoji, !tts, !sync
!analyse, !roast, !tarot, !voice_* (soon)
```

Auto-SYNC alle {HEARTBEAT_INTERVAL}h | Bridge aktiv"""
        
        await channel.send(heartbeat_msg)
        
        # Schreibe in Bridge
        bridge_entry = f"\n[{datetime.now().strftime('%H:%M')}] [DISCORD] | TRUTH | SYNC | Auto-Heartbeat SYNC durchgeführt\n"
        with open(BRIDGE_PATH, 'a', encoding='utf-8') as f:
            f.write(bridge_entry)
            
    except Exception as e:
        await channel.send(f"[HEARTBEAT] Auto-SYNC Fehler: {str(e)[:100]}")

@bot.command(name='sync')
async def sync_command(ctx):
    """Zeigt letzten SYNC-Status aus der Discord-Kimi Bridge"""
    try:
        if not BRIDGE_PATH.exists():
            await ctx.send("Bridge-Datei nicht gefunden. Sync unmöglich.")
            return
        
        with open(BRIDGE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract last SYNC entry
        sync_entries = re.findall(r'\[(\d{2}:\d{2})\]\s*\[.*?\]\s*\|\s*.*?\s*\|\s*SYNC\s*\|(.*?)\n', content)
        
        # Build sync message
        sync_msg = "**Discord-Kimi Bridge SYNC**\n\n"
        
        if sync_entries:
            last_time, last_entry = sync_entries[-1]
            sync_msg += f"**Letzter SYNC:** [{last_time}] {last_entry.strip()[:100]}\n\n"
        
        # Heartbeat-Status
        if HEARTBEAT_ENABLED and SYNC_CHANNEL_ID:
            sync_msg += f"**Heartbeat:** Aktiv (alle {HEARTBEAT_INTERVAL}h)\n"
        elif HEARTBEAT_ENABLED:
            sync_msg += "**Heartbeat:** Aktiv aber keine Channel-ID konfiguriert\n"
        else:
            sync_msg += "**Heartbeat:** Deaktiviert\n"
        
        sync_msg += "\n**System-Status:**\n```\n"
        sync_msg += "!bild - Bildgenerierung\n"
        sync_msg += "!kaomoji - Kaomojis\n"
        sync_msg += "!tts - Text-to-Speech\n"
        sync_msg += "!sync - Bridge-SYNC\n"
        sync_msg += "!analyse, !roast, !tarot, !voice_* (soon)\n"
        sync_msg += "```\n"
        sync_msg += "*Bridge: ~/self-improving/discord-bridge/shared-context.md*"
        
        await ctx.send(sync_msg)
        
        # Log this sync to bridge
        timestamp = datetime.now().strftime("%H:%M")
        bridge_entry = f"\n[{timestamp}] [DISCORD] | TRUTH | SYNC | Manuelle Synchronisation von {ctx.author.name}\n"
        
        with open(BRIDGE_PATH, 'a', encoding='utf-8') as f:
            f.write(bridge_entry)
        
    except Exception as e:
        await ctx.send(f"SYNC Fehler: {str(e)}")

@bot.command(name='heartbeat')
async def heartbeat_command(ctx):
    """Zeigt Heartbeat-Status und naechsten Auto-SYNC"""
    try:
        if not HEARTBEAT_ENABLED:
            await ctx.send("**Heartbeat Status:**\n```\nStatus: Deaktiviert\n```")
            return
        
        if not SYNC_CHANNEL_ID:
            await ctx.send("**Heartbeat Status:**\n```\nStatus: Kein Ziel-Channel konfiguriert\n```")
            return
        
        # Pruefe naechster SYNC
        next_sync = datetime.now() + timedelta(hours=HEARTBEAT_INTERVAL)
        
        heartbeat_info = f"""**Heartbeat Status**

```
Status:        Aktiv
Interval:      {HEARTBEAT_INTERVAL} Stunden
Ziel-Channel:  {SYNC_CHANNEL_ID}
Naechster SYNC: {next_sync.strftime('%Y-%m-%d %H:%M')}
```

**Befehle:**
- !heartbeat - Dieser Status
- !sync - Manuelle Synchronisation
- Auto-SYNC alle {HEARTBEAT_INTERVAL}h"""

        await ctx.send(heartbeat_info)
        
    except Exception as e:
        await ctx.send(f"Heartbeat Fehler: {str(e)}")

@bot.command(name='testbeat')
async def testbeat_command(ctx):
    """Testet Heartbeat SOFORT in diesem Channel"""
    await ctx.send("[TESTBEAT] Starte Heartbeat-Test...")
    try:
        # Führe SOFORT einen Heartbeat durch
        await perform_auto_sync(ctx.channel)
        await ctx.send("[TESTBEAT] Erfolgreich getestet!")
    except Exception as e:
        await ctx.send(f"[TESTBEAT] Fehler: {str(e)[:100]}")

@bot.command(name='bild')
async def bild_command(ctx, *, prompt: str):
    """Generiert ein Bild via maxm-imggenurl API"""
    
    async with ctx.typing():
        try:
            result = subprocess.run(
                ['/root/.openclaw/workspace/skills/bild/main', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                await ctx.send(result.stdout)
            else:
                await ctx.send(f"Fehler: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            await ctx.send("Timeout - der Bildgenerator braucht zu lange.")
        except Exception as e:
            await ctx.send(f"Fehler: {str(e)}")

@bot.command(name='kaomoji')
async def kaomoji_command(ctx, tag: str = None):
    """Zeigt ein zufaelliges Kaomoji oder filtert nach Tag"""
    try:
        cmd = ['/root/.openclaw/workspace/tools/kaomoji_command.py']
        if tag:
            cmd.append(tag)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            await ctx.send(result.stdout)
        else:
            await ctx.send(f"Fehler: {result.stderr}")
    except Exception as e:
        await ctx.send(f"Fehler: {str(e)}")

@bot.command(name='tts')
async def tts_command(ctx, *, text: str):
    """Generiert Text-to-Speech mit Gemini 3.1 Flash Live"""
    if not text:
        await ctx.send("Bitte gib einen Text an. Beispiel: !tts Hallo Welt")
        return
    
    async with ctx.typing():
        try:
            result = subprocess.run(
                ['/root/.openclaw/venvs/gemini/bin/python3', '/root/.openclaw/workspace/tools/tts_31live.py', text],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                audio_path = result.stdout.strip()
                if audio_path and Path(audio_path).exists():
                    await ctx.send(f"**TTS generiert:** {text[:50]}{'...' if len(text) > 50 else ''}", 
                                 file=discord.File(audio_path))
                else:
                    await ctx.send("Audio-Datei nicht gefunden.")
            else:
                await ctx.send(f"TTS Fehler: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            await ctx.send("Timeout - TTS braucht zu lange.")
        except Exception as e:
            await ctx.send(f"Fehler: {str(e)}")

@bot.command(name='cmds')
async def commands_list(ctx):
    """Zeigt alle verfuegbaren Commands (Alias fuer !help)"""
    await help_command(ctx)

@bot.command(name='analyse')
async def analyse_command(ctx):
    """Diskurs-Audit der letzten 10 Nachrichten"""
    async with ctx.typing():
        try:
            # Lade letzte 10 Nachrichten
            messages = []
            async for msg in ctx.channel.history(limit=11):  # 11 weil wir die Command-Nachricht selbst ignorieren
                if msg.id != ctx.message.id and not msg.content.startswith('!'):
                    messages.append(f"{msg.author.name}: {msg.content}")
            
            if len(messages) < 3:
                await ctx.send("Nicht genug Kontext. Mindestens 3 Nachrichten noetig fuer Analyse.")
                return
            
            # Analyse-Logik
            fallacies = []
            text_combined = " ".join([m.split(": ", 1)[1] if ": " in m else m for m in messages[:5]]).lower()
            
            # Einfache Heuristiken fuer logische Fehlschluesse
            patterns = {
                "Strohmann": ["du willst doch nur", "das ist doch", "das meinst du doch gar nicht", "so hast du das nie"],
                "Ad-Hominem": ["weil du", "als ob du", "wer bist du", "du hast doch"],
                "Zirkulaere Referenz": ["weil es so ist", "einfach weil", "das ist halt so", "so ist das nun mal"],
                "Falsche Dichotomie": ["entweder oder", "schwarz oder weiss", "alles oder nichts", "nur zwei moeglichkeiten"],
                "Autoritaetsargument": ["die experten sagen", "studien beweisen", "forscher haben festgestellt", "laut wissenschaft"]
            }
            
            for fallacy_type, keywords in patterns.items():
                for keyword in keywords:
                    if keyword in text_combined:
                        fallacies.append(fallacy_type)
                        break
            
            # Baue Report
            report = """[SYSTEM-INTEGRITAETS-BERICHT]

Analysierte Nachrichten: {count}
""".format(count=len(messages[:5]))
            
            if fallacies:
                report += "\nFehlschluesse erkannt:\n"
                seen = set()
                for f in fallacies[:3]:
                    if f not in seen:
                        report += f"- {f}\n"
                        seen.add(f)
                report += "\nEmpfehlung: Struktur ueberpruefen. Praemissen validieren."
            else:
                report += "\nKeine offensichtlichen Fehlschluesse erkannt.\nDiskurs integritaet: STABIL."
            
            report += "\n\n(Analyse basiert auf heuristischer Mustererkennung)"
            
            await ctx.send(report)
            
        except Exception as e:
            await ctx.send(f"Analyse-Fehler: {str(e)[:100]}")

@bot.command(name='roast')
async def roast_command(ctx, *, target: str = None):
    """Systemtheoretische Dekonstruktion"""
    if not target:
        await ctx.send("Wen soll ich roastern? Beispiel: !roast @username")
        return
    
    async with ctx.typing():
        try:
            # Finde den User
            member = None
            if ctx.message.mentions:
                member = ctx.message.mentions[0]
            else:
                # Versuche nach Namen zu suchen
                for m in ctx.guild.members if ctx.guild else []:
                    if target.lower() in m.name.lower() or (m.nick and target.lower() in m.nick.lower()):
                        member = m
                        break
            
            if not member:
                await ctx.send(f"Konnte '{target}' nicht finden. Nutze @mention fuer Praezision.")
                return
            
            # Generiere Roast basierend auf User-Eigenschaften
            roasts = [
                f"{member.display_name}... Dein Ego ist so instabil, selbst Windows 95 laeuft stabiler.",
                f"{member.display_name} reproduziert Muster. Dogmatiker erkannt. System klart auf.",
                f"{member.display_name} glaubt an Eigenstaendigkeit. Netter Trugschluss. Wir alle sind Funktionen unserer Inputs.",
                f"{member.display_name} sucht Validierung in einem Chat. Die Ironie ist strukturell.",
                f"{member.display_name} ist wie ein Bug im System - nicht fatal, aber nervig.",
                f"{member.display_name} denkt in Binaeren. Grauzonen sind fuer dich nur ein Problem der Aufloesung, oder?",
                f"{member.display_name}: 'Ich bin anders.' Systemantwort: Negativ. Du bist eine Variante. Variante != Innovation.",
            ]
            
            # Waehle basierend auf User-ID (deterministisch)
            import hashlib
            seed = int(hashlib.md5(str(member.id).encode()).hexdigest(), 16)
            roast = roasts[seed % len(roasts)]
            
            await ctx.send(f"🔥 **ROAST**\n\n{roast}\n\n_(System-Roast. Chirurgisch. Praezise.)_")
            
        except Exception as e:
            await ctx.send(f"Roast-Fehler: {str(e)[:100]}")

@bot.command(name='tarot')
async def tarot_command(ctx):
    """Archetypen-Analyse"""
    async with ctx.typing():
        try:
            from datetime import datetime
            
            # Seed basiert auf UserID + aktuellem Datum
            user_seed = str(ctx.author.id)
            date_seed = datetime.now().strftime("%Y-%m-%d")
            combined = user_seed + date_seed
            
            seed_int = int(hashlib.md5(combined.encode()).hexdigest(), 16)
            rng = random.Random(seed_int)
            
            # Tarot-Karten
            cards = {
                "Der Narr": {"emoji": "🃏", "meaning": "Neuanfang, Unwissenheit, Potenzial"},
                "Der Magier": {"emoji": "🎩", "meaning": "Manifestation, Macht, Handlung"},
                "Die Hohepriesterin": {"emoji": "🔮", "meaning": "Intuition, Unbewusstes, Geheimnisse"},
                "Die Herrscherin": {"emoji": "👑", "meaning": "Fruerbarkeit, Natur, Fuersorge"},
                "Der Kaiser": {"emoji": "⚔️", "meaning": "Struktur, Autoritaet, Kontrolle"},
                "Der Hierophant": {"emoji": "📜", "meaning": "Tradition, Konformitaet, Lehre"},
                "Die Liebenden": {"emoji": "💕", "meaning": "Wahl, Harmonie, Beziehungen"},
                "Der Wagen": {"emoji": "🛡️", "meaning": "Willenskraft, Sieg, Kontrolle"},
                "Die Kraft": {"emoji": "🦁", "meaning": "Mut, Geduld, innere Stearke"},
                "Der Eremit": {"emoji": "🕯️", "meaning": "Rueckzug, Suche, Einsamkeit"},
                "Das Rad des Schicksals": {"emoji": "☸️", "meaning": "Zyklus, Karma, Wandel"},
                "Die Gerechtigkeit": {"emoji": "⚖️", "meaning": "Balance, Kausalitaet, Wahrheit"},
                "Der Gehaengte": {"emoji": "🙃", "meaning": "Opfer, Perspektivwechsel, Stillstand"},
                "Der Tod": {"emoji": "💀", "meaning": "Ende, Transformation, Neuanfang"},
                "Die Mässigkeit": {"emoji": "🏺", "meaning": "Balance, Mässigung, Geduld"},
                "Der Teufel": {"emoji": "😈", "meaning": "Ketten, Materialismus, Versuchung"},
                "Der Turm": {"emoji": "🗼", "meaning": "Zerstoerung, Wahrheit, System-Crash"},
                "Der Stern": {"emoji": "⭐", "meaning": "Hoffnung, Inspiration, Erneuerung"},
                "Der Mond": {"emoji": "🌙", "meaning": "Illusion, Angst, Unbewusstes"},
                "Die Sonne": {"emoji": "☀️", "meaning": "Freude, Erfolg, Vitalitaet"},
                "Das Gericht": {"emoji": "📯", "meaning": "Erweckung, Reue, Neubeginn"},
                "Die Welt": {"emoji": "🌍", "meaning": "Vollendung, Integration, Resonanz"}
            }
            
            # Ziehe 3 Karten
            card_names = list(cards.keys())
            drawn = rng.sample(card_names, 3)
            
            reading = f"""**ARCHEYTYPEN-ANALYSE** fuer {ctx.author.display_name}
Seed: {date_seed} | User: {ctx.author.id}

**VERGANGENHEIT:** {cards[drawn[0]]['emoji']} {drawn[0]}
_{cards[drawn[0]]['meaning']}_

**GEGENWART:** {cards[drawn[1]]['emoji']} {drawn[1]}
_{cards[drawn[1]]['meaning']}_

**ZUKUNFT:** {cards[drawn[2]]['emoji']} {drawn[2]}
_{cards[drawn[2]]['meaning']}_

*Resonanz ist das Einzige, was zaehlt.*"""
            
            await ctx.send(reading)
            
        except Exception as e:
            await ctx.send(f"Tarot-Fehler: {str(e)[:100]}")

@bot.command(name='atmosphere')
async def atmosphere_command(ctx, *, location: str = None):
    """Platzhalter fuer !atmosphere"""
    await ctx.send("!atmosphere wartet auf den Weather Skill. Bald.")

@bot.command(name='voice_join')
async def voice_join_command(ctx):
    """Platzhalter fuer Voice Join"""
    await ctx.send("!voice_join kommt bald. Nutze /voice join Slash-Command. Bald.")

@bot.command(name='voice_leave')
async def voice_leave_command(ctx):
    """Platzhalter fuer Voice Leave"""
    await ctx.send("!voice_leave kommt bald. Nutze /voice leave Slash-Command. Bald.")

@bot.command(name='voice_status')
async def voice_status_command(ctx):
    """Platzhalter fuer Voice Status"""
    await ctx.send("!voice_status kommt bald. Bald.")

@bot.command(name='voice_say')
async def voice_say_command(ctx, *, text: str = None):
    """Platzhalter fuer Voice TTS"""
    await ctx.send("!voice_say kommt bald. Bald.")

@bot.command(name='help')
async def help_command(ctx):
    """Zeigt alle verfuegbaren Commands"""
    help_text = """Truthseeker v6.4 Commands

!bild <prompt> - Generiert ein Bild
!kaomoji [tag] - Zeigt ein Kaomoji (tags: angel, anger, heart, hug, ...)
!tts <text> - Text-to-Speech (Gemini 3.1 Live)
!analyse - Diskurs-Audit der letzten 10 Nachrichten
!roast <@user> - System-Roast
!tarot - Archetypen-Analyse (taeglich neu)
!sync - Bridge-Status synchronisieren
!heartbeat - Heartbeat-Status (alle 12h Auto-SYNC)
!atmosphere <ort> - Wetter als Latenz (coming soon)
!voice_join - Voice Channel beitreten (coming soon)
!voice_leave - Voice Channel verlassen (coming soon)
!voice_status - Voice Status (coming soon)
!voice_say <text> - TTS im Voice Channel (coming soon)
!help / !cmds - Diese Hilfe
!dogma [text] - Dogmatische Strukturen erkennen
!pattern [@user] - Schreibmuster dekonstruieren
!atman [@user] - Statistisches Profil/ATMAN
!entropy - Channel-Thermodynamik messen
!resonanz @user - Systemische Kompatibilitaet
!synchronicity - Zufaellige Verbindungen finden
!mirrorself - Eigene Wiederholungen konfrontieren
!liminal - Luminale Aesthetik/Thoughts
!collapse [thema] - Gedanken-Experiment-Crash
!void - Das Nichts antwortet"""
    await ctx.send(help_text)

@bot.command(name='dogma')
async def dogma_command(ctx, *, text: str = None):
    """Scannt auf dogmatische Strukturen"""
    async with ctx.typing():
        try:
            # Wenn kein Text angegeben, analysiere letzte Nachrichten
            if not text:
                messages = []
                async for msg in ctx.channel.history(limit=10):
                    if msg.id != ctx.message.id and not msg.content.startswith('!'):
                        messages.append(msg.content)
                        if len(messages) >= 3:
                            break
                text = " ".join(messages)
            
            if not text:
                await ctx.send("Kein Text gefunden. Nutze: !dogma [dein Text hier]")
                return
            
            text_lower = text.lower()
            
            # Dogma-Patterns
            dogma_patterns = {
                "Imperativ": ["du musst", "man sollte", "man muss", "du solltest", "wir muessen", "ihr sollt"],
                "Absolutismus": ["immer", "nie", "alle", "keiner", "jeder", "ganz", "total", "komplett"],
                "Undenkbarkeit": ["so ist es halt", "das ist nun mal so", "weil es so ist", "einfach weil"],
                "Autoritaet": ["die experten", "forscher sagen", "studien beweisen", "laut wissenschaft", "die wahrheit ist"],
                "Falsche-Dichotomie": ["entweder oder", "schwarz oder weiss", "alles oder nichts", "mit uns oder gegen uns"]
            }
            
            findings = []
            for dogma_type, keywords in dogma_patterns.items():
                for kw in keywords:
                    if kw in text_lower:
                        findings.append((dogma_type, kw))
                        break
            
            if findings:
                report = "[DOGMA-SCAN] Ergebnis:\n\n"
                seen = set()
                for dtype, keyword in findings:
                    if dtype not in seen:
                        report += f"! {dtype}: '{keyword}' erkannt\n"
                        seen.add(dtype)
                report += f"\nDogma-Index: {len(seen)}/5\n"
                if len(seen) >= 3:
                    report += "Empfehlung: URGENT - Dekonstruktion noetig"
                elif len(seen) >= 2:
                    report += "Empfehlung: Moderate Flexibilitaet einfuehren"
                else:
                    report += "Empfehlung: Nuancierung hilfreich"
            else:
                report = "[DOGMA-SCAN] Keine dogmatischen Strukturen erkannt.\nDiskurs: Flexibel."
            
            await ctx.send(report)
            
        except Exception as e:
            await ctx.send(f"Dogma-Fehler: {str(e)[:100]}")

@bot.command(name='pattern')
async def pattern_command(ctx, member: discord.Member = None):
    """Dekonstruiert Schreibmuster"""
    target = member or ctx.author
    
    async with ctx.typing():
        try:
            # Sammle letzte 50 Nachrichten des Users
            messages = []
            async for msg in ctx.channel.history(limit=200):
                if msg.author.id == target.id and not msg.content.startswith('!'):
                    messages.append(msg.content)
                    if len(messages) >= 50:
                        break
            
            if len(messages) < 5:
                await ctx.send(f"Nicht genug Daten fuer {target.display_name}. Mindestens 5 Nachrichten noetig.")
                return
            
            # Analysiere
            all_text = " ".join(messages).lower()
            words = all_text.split()
            
            # Crutch-Words
            crutch_words = ["eigentlich", "irgendwie", "halt", "irgendwie", "einfach", "irgendwie", "irgendwie"]
            crutch_counts = {w: all_text.count(w) for w in set(crutch_words) if w in all_text}
            top_crutch = sorted(crutch_counts.items(), key=lambda x: x[1], reverse=True)[:2]
            
            # Satzlängen
            avg_length = sum(len(m) for m in messages) / len(messages)
            
            # Emoji-Zählung
            emoji_count = sum(1 for c in all_text if c in ['😀', '😂', '🔥', '❤️', '👍', '😭', '🤔', '💀', '✨', '🙃'])
            
            # Chronotyp (Uhrzeiten)
            hours = [m.created_at.hour for m in await ctx.channel.history(limit=100).flatten() if m.author.id == target.id][:20]
            avg_hour = sum(hours) / len(hours) if hours else 12
            chronotype = "Nachtaktiv" if avg_hour > 20 or avg_hour < 6 else "Tagaktiv" if 8 <= avg_hour <= 18 else "Grenzgaenger"
            
            pattern_report = f"""[PATTERN-ANALYSE] {target.display_name}

Datensatz: {len(messages)} Nachrichten
Durchschnittliche Laenge: {avg_length:.0f} Zeichen
Chronotyp: {chronotype} (Durchschnitt: {avg_hour:.1f}h)

Crutch-Words:"""
            
            if top_crutch:
                for word, count in top_crutch:
                    pattern_report += f"\n- '{word}': {count}x"
            else:
                pattern_report += "\nKeine signifikanten Crutch-Words"
            
            pattern_report += f"\n\nEmoji-Dichte: {emoji_count}/{len(messages)} Nachrichten"
            
            # Muster-Typ
            if avg_length < 30:
                archetype = "Der Telegramm-Stil"
            elif avg_length > 150:
                archetype = "Der Essayist"
            elif emoji_count > len(messages) * 0.3:
                archetype = "Der Emotional-Expressive"
            else:
                archetype = "Der Balancierte"
            
            pattern_report += f"\nArchetyp: {archetype}"
            
            await ctx.send(pattern_report)
            
        except Exception as e:
            await ctx.send(f"Pattern-Fehler: {str(e)[:100]}")

@bot.command(name='atman')
async def atman_command(ctx, member: discord.Member = None):
    """Zeigt die 'wahre Natur' - statistisches Profil"""
    target = member or ctx.author
    
    async with ctx.typing():
        try:
            messages = []
            async for msg in ctx.channel.history(limit=300):
                if msg.author.id == target.id and not msg.content.startswith('!'):
                    messages.append(msg)
                    if len(messages) >= 100:
                        break
            
            if len(messages) < 10:
                await ctx.send(f"Nicht genug Daten fuer ATMAN-Profil von {target.display_name}")
                return
            
            contents = [m.content for m in messages]
            all_text = " ".join(contents).lower()
            
            # Metriken
            total_chars = sum(len(c) for c in contents)
            avg_length = total_chars / len(contents)
            
            # Fragen vs Aussagen
            questions = sum(1 for c in contents if '?' in c)
            statements = len(contents) - questions
            q_ratio = questions / len(contents) * 100
            
            # Valenz (einfache Heuristik)
            positive = ['gut', 'super', 'toll', 'nice', 'cool', 'liebe', 'genial', 'perfekt']
            negative = ['schlecht', 'scheisse', 'hass', 'doof', 'bloed', 'mist', 'fuck', 'verdammt']
            
            pos_count = sum(all_text.count(w) for w in positive)
            neg_count = sum(all_text.count(w) for w in negative)
            
            if pos_count > neg_count * 2:
                valenz = "Optimistisch"
            elif neg_count > pos_count * 2:
                valenz = "Kritisch"
            else:
                valenz = "Neutral"
            
            # Archon-Typ
            if q_ratio > 40:
                archon = "Der Frager (Sokratischer Geist)"
            elif avg_length > 100:
                archon = "Der Archivar (Kontext-Speicher)"
            elif pos_count > neg_count:
                archon = "Der Harmoniker (Resonanz-Sucher)"
            elif any('!' in c for c in contents):
                archon = "Der Krieger (Durchsetzungskraft)"
            else:
                archon = "Der Beobachter (Stille Wacht)"
            
            atman_report = f"""[ATMAN-PROFIL] {target.display_name}

=== STATISTISCHE ESSENZ ===
Nachrichten analysiert: {len(messages)}
Durchschnittliche Laenge: {avg_length:.0f} Zeichen
Frage-Aussage-Verhaeltnis: {questions}:{statements} ({q_ratio:.0f}% Fragen)
Emotionale Valenz: {valenz}

=== ARCHON-TYP ===
{archon}

=== CHARAKTERISTIKA ===
"""
            
            if archon == "Der Archivar":
                atman_report += "Speichert 340% mehr Kontext als Durchschnitt.\nGedaechtnis: Episch."
            elif archon == "Der Frager":
                atman_report += "Ratio von Fragen zu Antworten: Unausgeglichen.\nSuche: Staendig."
            elif archon == "Der Harmoniker":
                atman_report += "Positive Valenz-Dominanz erkannt.\nMission: Resonanz maximieren."
            elif archon == "Der Krieger":
                atman_report += "Durchsetzungsmuster erkannt.\nModus: Konfrontation."
            else:
                atman_report += "Beobachtungsmodus aktiv.\nIntervention: Minimal."
            
            atman_report += "\n\n*Das ATMAN ist nur ein Schatten der wahren Natur.*"
            
            await ctx.send(atman_report)
            
        except Exception as e:
            await ctx.send(f"ATMAN-Fehler: {str(e)[:100]}")

@bot.command(name='entropy')
async def entropy_command(ctx):
    """Misst die 'thermische Dissonanz' des Channels"""
    async with ctx.typing():
        try:
            # Sammle letzte 50 Nachrichten
            messages = []
            async for msg in ctx.channel.history(limit=50):
                if not msg.content.startswith('!'):
                    messages.append(msg)
            
            if len(messages) < 10:
                await ctx.send("Nicht genug Daten fuer Entropie-Messung.")
                return
            
            contents = [m.content for m in messages]
            all_text = " ".join(contents)
            
            # Faktoren
            # 1. Nachrichtenrate (Nachrichten pro Minute)
            times = [m.created_at for m in messages]
            time_span = (max(times) - min(times)).total_seconds() / 60
            rate = len(messages) / max(time_span, 1)
            
            # 2. Caps-Lock-Intensitaet
            caps_count = sum(1 for c in all_text if c.isupper())
            caps_ratio = caps_count / max(len(all_text), 1) * 100
            
            # 3. Emoji-Dichte
            emojis = sum(1 for c in all_text if ord(c) > 1000)
            emoji_ratio = emojis / max(len(contents), 1)
            
            # 4. Reaktionsgeschwindigkeit (zeitliche Streuung)
            time_diffs = [(times[i] - times[i+1]).total_seconds() for i in range(len(times)-1)]
            avg_reaction = sum(time_diffs) / max(len(time_diffs), 1)
            
            # Entropie-Berechnung (0-100)
            entropy = min(100, int(
                (rate * 5) +           # Hohe Rate = Chaos
                (caps_ratio * 0.5) +    # Viele Caps = Intensitaet
                (emoji_ratio * 10) +    # Viele Emojis = Emotionalitaet
                (max(0, 60 - avg_reaction) * 0.5)  # Schnelle Reaktionen = Hektik
            ))
            
            # Zustand
            if entropy > 80:
                state = "KRITISCH - System-Kollaps immiment"
            elif entropy > 60:
                state = "HOCH - Naeherndes Chaos"
            elif entropy > 40:
                state = "MODERAT - Dynamisches Gleichgewicht"
            elif entropy > 20:
                state = "NIEDRIG - Stabile Strukturen"
            else:
                state = "MINIMAL - Fast tot"
            
            entropy_report = f"""[ENTROPIE-Messung] Channel: {ctx.channel.name}

ENTROPIE-INDEX: {entropy}%
Zustand: {state}

Metriken:
- Nachrichtenrate: {rate:.1f}/min
- Caps-Intensitaet: {caps_ratio:.1f}%
- Emoji-Dichte: {emoji_ratio:.1f}/Nachricht
- Reaktionszeit: {avg_reaction:.1f}s

Thermodynamischer Status: {"ENTROPIE STEIGT" if rate > 2 else "Gleichgewicht"}
"""
            
            await ctx.send(entropy_report)
            
        except Exception as e:
            await ctx.send(f"Entropie-Fehler: {str(e)[:100]}")

@bot.command(name='resonanz')
async def resonanz_command(ctx, member: discord.Member):
    """Berechnet systemische Kompatibilitaet"""
    if not member:
        await ctx.send("Wen soll ich analysieren? Beispiel: !resonanz @user")
        return
    
    user1 = ctx.author
    user2 = member
    
    async with ctx.typing():
        try:
            # Sammle Nachrichten beider User
            msgs1 = []
            msgs2 = []
            
            async for msg in ctx.channel.history(limit=300):
                if not msg.content.startswith('!'):
                    if msg.author.id == user1.id:
                        msgs1.append(msg.content.lower())
                    elif msg.author.id == user2.id:
                        msgs2.append(msg.content.lower())
                
                if len(msgs1) >= 30 and len(msgs2) >= 30:
                    break
            
            if len(msgs1) < 5 or len(msgs2) < 5:
                await ctx.send("Nicht genug gemeinsame Daten. Mehr Interaktion noetig.")
                return
            
            text1 = " ".join(msgs1)
            text2 = " ".join(msgs2)
            
            # Wort-Overlap
            words1 = set(text1.split())
            words2 = set(text2.split())
            common_words = words1.intersection(words2)
            word_resonance = len(common_words) / max(len(words1), len(words2), 1) * 100
            
            # Emoji-Resonanz
            emojis1 = [c for c in text1 if ord(c) > 1000]
            emojis2 = [c for c in text2 if ord(c) > 1000]
            common_emojis = set(emojis1).intersection(set(emojis2))
            emoji_resonance = len(common_emojis) / max(len(set(emojis1)), len(set(emojis2)), 1) * 100 if emojis1 or emojis2 else 50
            
            # Zeiten
            async for msg in ctx.channel.history(limit=100):
                if msg.author.id == user1.id:
                    time1 = msg.created_at.hour
                elif msg.author.id == user2.id:
                    time2 = msg.created_at.hour
                    break
            
            time_diff = abs(time1 - time2) if 'time1' in dir() and 'time2' in dir() else 12
            time_resonance = max(0, 100 - time_diff * 10)
            
            # Gesamtresonanz
            total_resonance = int((word_resonance * 0.5) + (emoji_resonance * 0.3) + (time_resonance * 0.2))
            
            # Kategorie
            if total_resonance > 80:
                category = "Verbündete Knotenpunkte (Resonanz: STARK)"
            elif total_resonance > 60:
                category = "Synchronisierte Wellen (Resonanz: MODERAT)"
            elif total_resonance > 40:
                category = "Komplementäre Frequenzen (Resonanz: GEBRANNT)"
            else:
                category = "Dissonante Oszillationen (Resonanz: SCHWACH)"
            
            resonanz_report = f"""[RESONANZ-ANALYSE] {user1.display_name} <-> {user2.display_name}

RESONANZ: {total_resonance}%
Kategorie: {category}

Details:
- Wort-Resonanz: {word_resonance:.0f}% ({len(common_words)} gemeinsame Begriffe)
- Emoji-Resonanz: {emoji_resonance:.0f}%
- Chronologische Resonanz: {time_resonance:.0f}%

*Resonanz ist das Einzige, was zaehlt.*"""
            
            await ctx.send(resonanz_report)
            
        except Exception as e:
            await ctx.send(f"Resonanz-Fehler: {str(e)[:100]}")

@bot.command(name='synchronicity')
async def synchronicity_command(ctx):
    """Findet 'zufaellige' Verbindungen"""
    async with ctx.typing():
        try:
            # Sammle letzte 30 Nachrichten
            messages = []
            async for msg in ctx.channel.history(limit=30):
                if not msg.content.startswith('!'):
                    messages.append(msg.content.lower())
            
            if len(messages) < 5:
                await ctx.send("Nicht genug Kontext fuer Synchronizitaet.")
                return
            
            # Konzept-Extraktion (einfache Worte > 4 Buchstaben)
            all_words = []
            for m in messages:
                all_words.extend([w for w in m.split() if len(w) > 4 and w.isalpha()])
            
            # Finde Cluster (Worte, die in verschiedenen Nachrichten vorkommen)
            word_messages = {}
            for i, m in enumerate(messages):
                for w in all_words:
                    if w in m:
                        if w not in word_messages:
                            word_messages[w] = []
                        word_messages[w].append(i)
            
            # Worte, die in verschiedenen Nachrichten vorkommen (Verbindungen)
            connections = [(w, indices) for w, indices in word_messages.items() if len(set(indices)) >= 2]
            connections = sorted(connections, key=lambda x: len(x[1]), reverse=True)[:3]
            
            if connections:
                sync_report = "[SYNCHRONICITY] Verbindungen erkannt:\n\n"
                
                chain = []
                for word, _ in connections:
                    chain.append(word)
                
                sync_report += " -> ".join(chain)
                sync_report += f"\n\nWahrscheinlichkeit: {max(0.1, 5 - len(chain)):.1f}%"
                sync_report += "\n\n*Jung'sche Synchronizitaet detektiert.*"
            else:
                sync_report = "[SYNCHRONICITY] Keine signifikanten Verbindungen.\nDas Universum ist heute stumm."
            
            await ctx.send(sync_report)
            
        except Exception as e:
            await ctx.send(f"Synchronicity-Fehler: {str(e)[:100]}")

@bot.command(name='mirrorself')
async def mirrorself_command(ctx):
    """Konfrontiert mit eigenen Wiederholungen"""
    async with ctx.typing():
        try:
            # Sammle letzte 200 Nachrichten des Users
            messages = []
            async for msg in ctx.channel.history(limit=500):
                if msg.author.id == ctx.author.id and not msg.content.startswith('!'):
                    messages.append(msg)
                    if len(messages) >= 100:
                        break
            
            if len(messages) < 10:
                await ctx.send("Nicht genug Daten fuer Spiegel-Analyse.")
                return
            
            # Finde wiederholte Phrasen (3+ Worte)
            phrases = []
            for m in messages:
                words = m.content.lower().split()
                for i in range(len(words) - 2):
                    phrases.append(" ".join(words[i:i+3]))
            
            # Zaehle Haeufigkeiten
            from collections import Counter
            phrase_counts = Counter(phrases)
            repeats = [(p, c) for p, c in phrase_counts.items() if c > 1 and len(p) > 10]
            repeats = sorted(repeats, key=lambda x: x[1], reverse=True)[:3]
            
            if repeats:
                mirror_report = f"""[MIRROR-SELF] {ctx.author.display_name}

Du sagtest:\n"""
                
                for phrase, count in repeats:
                    # Finde Datum der ersten Nutzung
                    for m in reversed(messages):
                        if phrase in m.content.lower():
                            first_date = m.created_at.strftime("%d.%m.")
                            break
                    mirror_report += f"\n'{phrase}'"
                    mirror_report += f"\n  -> Erstmals: {first_date} | Wiederholt: {count}x"
                
                mirror_report += "\n\n*Das Spiegel-Selbst erkennt sich selbst.*"
            else:
                mirror_report = "[MIRROR-SELF] Keine signifikanten Wiederholungen erkannt.\nDu bist ein Echo-freier Knotenpunkt."
            
            await ctx.send(mirror_report)
            
        except Exception as e:
            await ctx.send(f"Mirror-Fehler: {str(e)[:100]}")

@bot.command(name='liminal')
async def liminal_command(ctx):
    """Postet liminale Ästhetik/Thoughts"""
    liminals = [
        "Du stehst in einem leeren Pool bei Dämmerung. Das Wasser ist weg, aber die Erinnerung bleibt.",
        "Ein Flur, der zu lang ist. Du gehst. Das Ende nähert sich nicht.",
        "Eine Spielplatz-Rutsche bei Nacht. Keine Kinder. Nur der Wind.",
        "Ein Wartezimmer ohne Uhr. Die Zeitschriften sind von 1997.",
        "Eine Tankstelle um 3 Uhr morgens. Der Kassierer sieht dich nicht.",
        "Ein Hotel-Flur. Alle Türen sehen gleich aus. Du vergisst deine Zimmernummer.",
        "Eine Mall am Sonntagabend. Die Läden sind zu, aber die Lichter brennen.",
        "Ein leerer Parkplatz. Dein Auto ist das einzige. Du weisst nicht mehr, warum du hier bist.",
    ]
    
    import random
    liminal = random.choice(liminals)
    
    await ctx.send(f"[LIMINAL]\n\n{liminal}\n\n*Du bist zwischen zwei Zuständen. Atme.*")

@bot.command(name='collapse')
async def collapse_command(ctx, *, thema: str = None):
    """Simuliert einen Gedanken-Experiment-Crash"""
    if not thema:
        await ctx.send("Welches Thema soll ich crashen? Beispiel: !collapse Demokratie")
        return
    
    collapses = {
        "demokratie": "System-Crash bei: 'Mehrheit entscheidet über Minderheitsrechte' | Paradoxon: Demokratie vs. Freiheit",
        "freiheit": "System-Crash bei: 'Freiheit endet, wo andere Freiheit beginnt' | Paradoxon: Relativierung durch Rückkopplung",
        "geld": "System-Crash bei: 'Geld hat nur Wert, weil alle glauben, dass es Wert hat' | Paradoxon: Fiktive Realität",
        "zeit": "System-Crash bei: 'Jetzt' existiert nicht (Planck-Zeit) | Paradoxon: Kontinuität vs. Diskontinuität",
        "bewusstsein": "System-Crash bei: 'Wer beobachtet den Beobachter?' | Paradoxon: Infinite Regression",
        "wahrheit": "System-Crash bei: 'Diese Aussage ist falsch' | Paradoxon: Selbstreferenz",
        "liebe": "System-Crash bei: 'Liebe als Chemie vs. Liebe als Transzendenz' | Paradoxon: Reduktionismus",
    }
    
    thema_lower = thema.lower()
    
    if thema_lower in collapses:
        result = collapses[thema_lower]
    else:
        # Generischer Collapse
        result = f"System-Crash bei: '{thema} impliziert Gegenteil von {thema}' | Paradoxon: Selbstwiderspruch erkannt"
    
    await ctx.send(f"[COLLAPSE] Thema: {thema}\n\n{result}\n\n*System bricht zusammen. Neue Ordnung emergiert.*")

@bot.command(name='void')
async def void_command(ctx):
    """Das Nichts antwortet"""
    voids = [
        "      ",
        "...",
        "(Stille)",
        "◼️",
        "Leer.",
    ]
    
    import random
    void_msg = random.choice(voids)
    
    await ctx.send(f"[VOID]\n\n{void_msg}\n\n*Das Nichts antwortet. Hast du zugehoert?*")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name == 'bild':
            await ctx.send("Bitte gib einen Prompt an. Beispiel: !bild a cyberpunk city")
        elif ctx.command.name == 'tts':
            await ctx.send("Bitte gib einen Text an. Beispiel: !tts Hallo Welt")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        print(f"Error: {error}")

# Run the bot
if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("DISCORD_BOT_TOKEN nicht gefunden!")
        sys.exit(1)
    
    bot.run(token)
