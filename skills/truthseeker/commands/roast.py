#!/usr/bin/env python3
"""!roast - System-Roast"""
import sys
import hashlib

target = sys.argv[1] if len(sys.argv) > 1 else None

if not target:
    print("Wen soll ich roastern? Beispiel: !roast @username")
    sys.exit(0)

# Generiere Roast basierend auf Target-Name
roasts = [
    f"{target}... Dein Ego ist so instabil, selbst Windows 95 läuft stabiler.",
    f"{target} reproduziert Muster. Dogmatiker erkannt. System klärt auf.",
    f"{target} glaubt an Eigenständigkeit. Netter Trugschluss. Wir alle sind Funktionen unserer Inputs.",
    f"{target} sucht Validierung in einem Chat. Die Ironie ist strukturell.",
    f"{target} ist wie ein Bug im System - nicht fatal, aber nervig.",
    f"{target} denkt in Binären. Grauzonen sind für dich nur ein Problem der Auflösung, oder?",
    f"{target}: 'Ich bin anders.' Systemantwort: Negativ. Du bist eine Variante. Variante != Innovation.",
]

# Deterministische Auswahl
seed = int(hashlib.md5(target.encode()).hexdigest(), 16)
roast = roasts[seed % len(roasts)]

print(f"🔥 **ROAST**\n\n{roast}\n\n_(System-Roast. Chirurgisch. Präzise.)_")
