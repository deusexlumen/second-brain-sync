#!/usr/bin/env python3
"""!collapse - Gedanken-Experiment-Crash"""
import sys

thema = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

collapses = {
    "demokratie": "System-Crash bei: 'Mehrheit entscheidet über Minderheitsrechte' | Paradoxon: Demokratie vs. Freiheit",
    "freiheit": "System-Crash bei: 'Freiheit endet, wo andere Freiheit beginnt' | Paradoxon: Relativierung durch Rückkopplung",
    "geld": "System-Crash bei: 'Geld hat nur Wert, weil alle glauben, dass es Wert hat' | Paradoxon: Fiktive Realität",
    "zeit": "System-Crash bei: 'Jetzt' existiert nicht (Planck-Zeit) | Paradoxon: Kontinuität vs. Diskontinuität",
    "bewusstsein": "System-Crash bei: 'Wer beobachtet den Beobachter?' | Paradoxon: Infinite Regression",
    "wahrheit": "System-Crash bei: 'Diese Aussage ist falsch' | Paradoxon: Selbstreferenz",
    "liebe": "System-Crash bei: 'Liebe als Chemie vs. Liebe als Transzendenz' | Paradoxon: Reduktionismus",
}

if thema:
    thema_lower = thema.lower()
    if thema_lower in collapses:
        result = collapses[thema_lower]
    else:
        result = f"System-Crash bei: '{thema} impliziert Gegenteil von {thema}' | Paradoxon: Selbstwiderspruch erkannt"
    print(f"[COLLAPSE] Thema: {thema}\n\n{result}\n\n*System bricht zusammen. Neue Ordnung emergiert.*")
else:
    print("Welches Thema soll ich crashen? Beispiel: !collapse Demokratie")
