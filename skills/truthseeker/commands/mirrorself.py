#!/usr/bin/env python3
"""!mirrorself - Konfrontiert mit eigenen Wiederholungen"""
import random

phrases = [
    ("'Eigentlich...'", "12.03.", 7),
    ("'Ich meinte...'", "15.03.", 5),
    ("'Das ist halt so'", "20.03.", 4),
    ("'Verstehst du?'", "22.03.", 9),
]

print("[MIRROR-SELF]\n")
print("Du sagtest:\n")

for phrase, date, count in phrases[:3]:
    print(f"{phrase}")
    print(f"  -> Erstmals: {date} | Wiederholt: {count}x\n")

print("*Das Spiegel-Selbst erkennt sich selbst.*")
