#!/usr/bin/env python3
"""!tarot - Archetypen-Analyse"""
import hashlib
import random
from datetime import datetime

# Tarot-Karten
cards = {
    "Der Narr": {"emoji": "🃏", "meaning": "Neuanfang, Unwissenheit, Potenzial"},
    "Der Magier": {"emoji": "🎩", "meaning": "Manifestation, Macht, Handlung"},
    "Die Hohepriesterin": {"emoji": "🔮", "meaning": "Intuition, Unbewusstes, Geheimnisse"},
    "Die Herrscherin": {"emoji": "👑", "meaning": "Fruchtbarkeit, Natur, Fürsorge"},
    "Der Kaiser": {"emoji": "⚔️", "meaning": "Struktur, Autorität, Kontrolle"},
    "Der Hierophant": {"emoji": "📜", "meaning": "Tradition, Konformität, Lehre"},
    "Die Liebenden": {"emoji": "💕", "meaning": "Wahl, Harmonie, Beziehungen"},
    "Der Wagen": {"emoji": "🛡️", "meaning": "Willenskraft, Sieg, Kontrolle"},
    "Die Kraft": {"emoji": "🦁", "meaning": "Mut, Geduld, innere Stärke"},
    "Der Eremit": {"emoji": "🕯️", "meaning": "Rückzug, Suche, Einsamkeit"},
    "Das Rad des Schicksals": {"emoji": "☸️", "meaning": "Zyklus, Karma, Wandel"},
    "Die Gerechtigkeit": {"emoji": "⚖️", "meaning": "Balance, Kausalität, Wahrheit"},
    "Der Gehängte": {"emoji": "🙃", "meaning": "Opfer, Perspektivwechsel, Stillstand"},
    "Der Tod": {"emoji": "💀", "meaning": "Ende, Transformation, Neuanfang"},
    "Die Mässigung": {"emoji": "🏺", "meaning": "Balance, Mässigung, Geduld"},
    "Der Teufel": {"emoji": "😈", "meaning": "Ketten, Materialismus, Versuchung"},
    "Der Turm": {"emoji": "🗼", "meaning": "Zerstörung, Wahrheit, System-Crash"},
    "Der Stern": {"emoji": "⭐", "meaning": "Hoffnung, Inspiration, Erneuerung"},
    "Der Mond": {"emoji": "🌙", "meaning": "Illusion, Angst, Unbewusstes"},
    "Die Sonne": {"emoji": "☀️", "meaning": "Freude, Erfolg, Vitalität"},
    "Das Gericht": {"emoji": "📯", "meaning": "Erweckung, Reue, Neubeginn"},
    "Die Welt": {"emoji": "🌍", "meaning": "Vollendung, Integration, Resonanz"}
}

# Deterministischer Seed
user_seed = "245661627897217025"  # Prime Node ID als Default
date_seed = datetime.now().strftime("%Y-%m-%d")
combined = user_seed + date_seed

seed_int = int(hashlib.md5(combined.encode()).hexdigest(), 16)
rng = random.Random(seed_int)

# Ziehe 3 Karten
card_names = list(cards.keys())
drawn = rng.sample(card_names, 3)

print(f"""**ARCHEYTYPEN-ANALYSE**
Seed: {date_seed}

**VERGANGENHEIT:** {cards[drawn[0]]['emoji']} {drawn[0]}
_{cards[drawn[0]]['meaning']}_

**GEGENWART:** {cards[drawn[1]]['emoji']} {drawn[1]}
_{cards[drawn[1]]['meaning']}_

**ZUKUNFT:** {cards[drawn[2]]['emoji']} {drawn[2]}
_{cards[drawn[2]]['meaning']}_

*Resonanz ist das Einzige, was zählt.*""")
