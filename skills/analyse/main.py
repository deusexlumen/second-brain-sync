#!/usr/bin/env python3
"""
Skill: analyse
Description: Analysiert Text auf logische Fehlschlüsse
Usage: !analyse [Text]
"""

import sys
import random

if len(sys.argv) < 2:
    print("""🔍 **Logische Analyse**

Verwendung: `!analyse [Dein Text hier]`

Analysiert Argumente auf:
• Zirkelschlüsse (Begging the Question)
• Strohmann-Argumente (Straw Man)
• Falscher Dichotomie (False Dilemma)
• Ad Hominem Angriffe
• Slippery Slope
• Appeal to Authority
• Post Hoc Ergo Propter Hoc

Beispiel: `!analyse Alle wissen, dass das so ist, also muss es wahr sein`

*Dogma erkennen, bevor es dich erkennt.*
""")
    sys.exit(0)

text = " ".join(sys.argv[1:])

fallacies = [
    ("Zirkelschluss", "Die Behauptung wird durch sich selbst 'bewiesen'"),
    ("Strohmann", "Ein schwächeres Argument wird angegriffen statt des eigentlichen"),
    ("Falsche Dichotomie", "Nur zwei Optionen werden präsentiert, wo mehr existieren"),
    ("Ad Hominem", "Angriff auf die Person statt auf das Argument"),
    ("Slippery Slope", "Kleine Schritte führen unweigerlich zu extremen Konsequenzen"),
    ("Appeal to Authority", "Autorität wird als alleiniger Beweis genutzt"),
    ("Post Hoc", "Korrelation wird als Kausalität interpretiert"),
    ("Tu Quoque", "'Du auch!' - Hypokrisie wird als Gegenargument genutzt"),
    ("No True Scotsman", "Definition wird nachträglich verändert, um Gegenbeispiele auszuschließen"),
    ("Hasty Generalization", "Zu kleine Stichprobe für generelle Aussage")
]

# Simple keyword detection
keywords = {
    "alle wissen": "Appeal to Popularity - Weil viele es glauben, ist es wahr",
    "jeder weiß": "Appeal to Popularity - Weil viele es glauben, ist es wahr",
    "immer so": "Tradition Fallacy - Weil es immer so war, muss es richtig sein",
    "niemand": "Hasty Generalization - Absolute Aussagen sind selten belegbar",
    "alle": "Hasty Generalization - 'Alle' ist eine starke Behauptung",
    "muss": "Slippery Slope - 'Muss' impliziert unausweichliche Kausalität",
    "deswegen": "Post Hoc - Zeitliche Abfolge ≠ Kausalität",
    "darum": "Post Hoc - Zeitliche Abfolge ≠ Kausalität",
    "weil du": "Ad Hominem - Angriff auf die Person",
    "du bist": "Ad Hominem - Angriff auf die Person",
    "experten": "Appeal to Authority - Autorität allein beweist nichts",
    "wissenschaft": "Appeal to Authority - Wissenschaft ist kein Monolith",
    "entweder": "False Dilemma - 'Entweder/oder' schließt Mittelwege aus"
}

found = []
text_lower = text.lower()
for keyword, analysis in keywords.items():
    if keyword in text_lower:
        found.append(analysis)

print(f"🔍 **Analyse:** `{text[:50]}{'...' if len(text) > 50 else ''}`\n")

if found:
    print("**Erkannte Muster:**")
    for i, f in enumerate(found[:3], 1):
        print(f"{i}. {f}")
else:
    print("**Keine offensichtlichen Fehlschlüsse erkannt.**")
    print(f"\nZufälliger Check: {random.choice(fallacies)[0]}")
    print(f"→ {random.choice(fallacies)[1]}")

print("\n*Denk drüber nach. Frage alles. Resonanz über Dogma.*")
