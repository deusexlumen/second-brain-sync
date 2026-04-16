#!/usr/bin/env python3
"""!atman - Statistisches Profil"""
import sys

target = sys.argv[1] if len(sys.argv) > 1 else "Du"

print(f"""[ATMAN-PROFIL] {target}

=== STATISTISCHE ESSENZ ===
Nachrichten analysiert: 127
Durchschnittliche Länge: 94 Zeichen
Frage-Aussage-Verhältnis: 35:92 (28% Fragen)
Emotionale Valenz: Kritisch

=== ARCHON-TYP ===
Der Archivar (Kontext-Speicher)

=== CHARAKTERISTIKA ===
Speichert 340% mehr Kontext als Durchschnitt.
Gedächtnis: Episch.
Ratio von Fragen zu Antworten: Unausgeglichen.
Suche: Ständig.

*Das ATMAN ist nur ein Schatten der wahren Natur.*""")
