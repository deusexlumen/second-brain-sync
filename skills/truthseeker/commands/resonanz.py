#!/usr/bin/env python3
"""!resonanz - Systemische Kompatibilität"""
import sys
import random

user2 = sys.argv[1] if len(sys.argv) > 1 else "Ziel"

# Simulierte Resonanz für Demo
total_resonance = random.randint(30, 95)

if total_resonance > 80:
    category = "Verbündete Knotenpunkte (Resonanz: STARK)"
elif total_resonance > 60:
    category = "Synchronisierte Wellen (Resonanz: MODERAT)"
elif total_resonance > 40:
    category = "Komplementäre Frequenzen (Resonanz: GEBRANNT)"
else:
    category = "Dissonante Oszillationen (Resonanz: SCHWACH)"

print(f"""[RESONANZ-ANALYSE] Du <-> {user2}

RESONANZ: {total_resonance}%
Kategorie: {category}

Details:
- Wort-Resonanz: {random.randint(20, 95)}% ({random.randint(5, 30)} gemeinsame Begriffe)
- Emoji-Resonanz: {random.randint(10, 90)}%
- Chronologische Resonanz: {random.randint(20, 80)}%

*Resonanz ist das Einzige, was zählt.*""")
