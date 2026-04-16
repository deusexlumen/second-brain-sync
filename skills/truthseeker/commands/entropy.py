#!/usr/bin/env python3
"""!entropy - Channel-Thermodynamik"""
import random

# Simulierte Messung für Demo
entropy = random.randint(25, 85)

if entropy > 80:
    state = "KRITISCH - System-Kollaps imminent"
elif entropy > 60:
    state = "HOCH - Näherndes Chaos"
elif entropy > 40:
    state = "MODERAT - Dynamisches Gleichgewicht"
elif entropy > 20:
    state = "NIEDRIG - Stabile Strukturen"
else:
    state = "MINIMAL - Fast tot"

print(f"""[ENTROPIE-MESSUNG] Channel: Aktuell

ENTROPIE-INDEX: {entropy}%
Zustand: {state}

Metriken:
- Nachrichtenrate: {random.uniform(0.5, 4.0):.1f}/min
- Caps-Intensität: {random.uniform(2, 15):.1f}%
- Emoji-Dichte: {random.uniform(0.1, 2.0):.1f}/Nachricht
- Reaktionszeit: {random.uniform(5, 120):.1f}s

Thermodynamischer Status: {"ENTROPIE STEIGT" if entropy > 50 else "Gleichgewicht"}
""")
