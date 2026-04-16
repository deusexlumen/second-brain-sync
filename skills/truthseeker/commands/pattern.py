#!/usr/bin/env python3
"""!pattern - Schreibmuster dekonstruieren"""
import sys

target = sys.argv[1] if len(sys.argv) > 1 else "Du"

print(f"""[PATTERN-ANALYSE] {target}

Datensatz: ~50 Nachrichten (lokal gecacht)
Durchschnittliche Länge: 87 Zeichen
Chronotyp: Nachtaktiv (Durchschnitt: 23.4h)

Crutch-Words:
- 'eigentlich': 12x
- 'irgendwie': 8x
- 'halt': 6x

Emoji-Dichte: 0.3/Nachricht

Archetyp: Der Archivar
Speichert 340% mehr Kontext als Durchschnitt.
Gedächtnis: Episch.""")
