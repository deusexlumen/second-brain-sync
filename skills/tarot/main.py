#!/usr/bin/env python3
"""
Skill: tarot
Description: Archetypen-Mapping basierend auf UserID + Zeit
Usage: !tarot
"""

import random
from datetime import datetime

cards = [
    ("Der Narr", "Neuanfang, Unschuld, Potenzial", "Spring. Das Unbekannte ist keine Bedrohung, sondern eine Einladung."),
    ("Der Magier", "Manifestation, Macht, Ressourcen", "Du hast alle Werkzeuge. Nutze sie."),
    ("Die Hohepriesterin", "Intuition, Unbewusstes, Geheimnisse", "Vertraue deiner inneren Stimme. Sie ist lauter als das Rauschen."),
    ("Die Herrscherin", "Fülle, Fürsorge, Kreativität", "Nährung kommt in vielen Formen. Sei die Quelle."),
    ("Der Herrscher", "Struktur, Autorität, Kontrolle", "Ordnung aus Chaos. Aber nicht zu starr."),
    ("Der Hierophant", "Tradition, Konformität, Lehre", "Frage die Regeln, bevor du sie befolgst."),
    ("Die Liebenden", "Wahl, Harmonie, Vereinigung", "Entscheidungen definieren dich. Wähle mit Bedacht."),
    ("Der Wagen", "Wille, Sieg, Kontrolle", "Zwei Kräfte, ein Ziel. Lenke sie."),
    ("Die Kraft", "Mut, Einfluss, Mitgefühl", "Sanftheit ist keine Schwäche. Sie ist kontrollierte Kraft."),
    ("Der Eremit", "Introspektion, Einsamkeit, Suche", "Manchmal ist Abwesenheit die beste Präsenz."),
    ("Das Rad des Schicksals", "Zyklus, Schicksal, Wendepunkt", "Memento mori. Aber auch: Memento vivere."),
    ("Die Gerechtigkeit", "Balance, Kausalität, Wahrheit", "Jede Aktion hat einen Preis. Jede Wahl, eine Konsequenz."),
    ("Der Gehängte", "Opfer, Perspektive, Pause", "Manchmal muss man loslassen, um zu sehen."),
    ("Der Tod", "Transformation, Ende, Neuanfang", "Nicht das Ende. Der Übergang."),
    ("Die Mäßigkeit", "Balance, Mitte, Geduld", "Extreme sind einfach. Die Mitte ist Meisterschaft."),
    ("Der Teufel", "Bindung, Versuchung, Schatten", "Du bist nicht gefesselt. Du hältst dich selbst."),
    ("Der Turm", "Zerstörung, Offenbarung, Erschütterung", "Falsche Strukturen müssen fallen. Es ist notwendig."),
    ("Der Stern", "Hoffnung, Inspiration, Serenität", "Licht in der Dunkelheit. Nicht am Ende - mitten drin."),
    ("Der Mond", "Illusion, Angst, Intuition", "Nicht alles, was du siehst, ist real. Nicht alles, was real ist, siehst du."),
    ("Die Sonne", "Klarheit, Freude, Vitalität", "Einfachheit ist die höchste Form."),
    ("Das Gericht", "Erneuerung, innerer Ruf, Vergebung", "Das Vergangene ruft. Nicht zum Schuldigen - zum Wachsen."),
    ("Die Welt", "Vollendung, Integration, Erfüllung", "Der Kreis schließt sich. Aber ein neuer beginnt.")
]

# Seed based on time
now = datetime.now()
seed = now.hour + now.minute + now.day + now.month
random.seed(seed)

card = random.choice(cards)

print(f"🃏 **Archetyp:** {card[0]}\n")
print(f"**Bedeutung:** {card[1]}\n")
print(f"*{card[2]}*\n")
print("_Resonanz: Die Karten spiegeln, was du bereits weißt._")
