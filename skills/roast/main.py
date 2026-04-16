#!/usr/bin/env python3
"""
Skill: roast
Description: Systemtheoretische Dekonstruktion
Usage: !roast [Optional: Text]
"""

import sys
import random

roasts = [
    "Das ist kein Bug, das ist ein Feature deiner kognitiven Dissonanz.",
    "Du reproduzierst Muster, die du nicht verstehst. Nichts Neues.",
    "Deine Argumentation hat die Stabilität eines Kartenhauses in einem Hurrikan.",
    "Das System hat dich längst assimiliert. Du merkst es nur nicht.",
    "Kognitive Effizienz: 404 not found.",
    "Du bist nicht überzeugend. Du bist nur laut.",
    "Das ist kein Denken. Das ist mentales Recycling.",
    "Deine Logik hat mehr Lücken als ein Schweizer Käse.",
    "Du argumentierst wie ein deterministischer Algorithmus ohne Input-Validierung.",
    "Das ist nicht tiefgründig. Das ist nur verschwommen.",
    "Deine Überzeugungen haben eine höhere Halbwertszeit als deine Fakten.",
    "Du suchst Bestätigung, nicht Wahrheit. Das ist kein Bug, das ist das Feature.",
    "Kritischer Denkprozess: Abgestürzt. Neustart wird empfohlen.",
    "Das ist kein Gespräch. Das ist ein Monolog mit Publikum.",
    "Deine mentale Modelle sind veraltet. Update verfügbar."
]

if len(sys.argv) > 1:
    target = " ".join(sys.argv[1:])
    print(f"🔥 **Roast für:** `{target[:40]}{'...' if len(target) > 40 else ''}`\n")
else:
    print("🔥 **System-Roast**\n")

print(f"{random.choice(roasts)}\n")
print("*Resonanz ist das Einzige, was zählt. Dogma brennt.*")
