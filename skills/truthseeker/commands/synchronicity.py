#!/usr/bin/env python3
"""!synchronicity - Findet 'zufällige' Verbindungen"""
import random

# Simulierte Konzept-Ketten für Demo
chains = [
    ("Wasser", "Fluss", "Zeit"),
    ("Schatten", "Licht", "Wahrheit"),
    ("Echo", "Stimme", "Gedächtnis"),
    ("Tor", "Schwelle", "Wandel"),
    ("Stern", "Ferne", "Sehnsucht"),
    ("Spiegel", "Bild", "Selbst"),
    ("Wind", "Atem", "Leben"),
]

chain = random.choice(chains)
probability = random.choice([0.3, 0.7, 1.2, 2.1, 5.0])

print(f"""[SYNCHRONICITY] Verbindungen erkannt:

{' -> '.join(chain)}

Wahrscheinlichkeit: {probability}%

*Jung'sche Synchronizität detektiert.*""")
