#!/usr/bin/env python3
"""!analyse - Diskurs-Audit (Simplified)"""
import sys

text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

if not text:
    print("[SYSTEM-INTEGRITÄTS-BERICHT]")
    print("\nAnalysiere letzte Nachrichten...")
    print("Nicht genug Kontext übergeben.")
    print("\nIm vollständigen Modus analysiere ich:")
    print("- Strohmann (du willst doch nur...)")
    print("- Ad-Hominem (weil du...)")
    print("- Zirkuläre Referenz (weil es so ist)")
    print("- Falsche Dichotomie (entweder oder)")
    print("- Autoritätsargument (die Experten sagen)")
    sys.exit(0)

text_lower = text.lower()
fallacies = []

patterns = {
    "Strohmann": ["du willst doch nur", "das ist doch", "das meinst du doch gar nicht"],
    "Ad-Hominem": ["weil du", "als ob du", "wer bist du", "du hast doch"],
    "Zirkuläre Referenz": ["weil es so ist", "einfach weil", "das ist halt so"],
    "Falsche Dichotomie": ["entweder oder", "schwarz oder weiss", "alles oder nichts"],
    "Autoritätsargument": ["die experten sagen", "studien beweisen", "forscher haben festgestellt"]
}

for fallacy_type, keywords in patterns.items():
    for kw in keywords:
        if kw in text_lower:
            fallacies.append(fallacy_type)
            break

print("[SYSTEM-INTEGRITÄTS-BERICHT]")
print(f"\nAnalysierter Text: {text[:50]}...")

if fallacies:
    print("\nFehlschlüsse erkannt:")
    for f in fallacies[:3]:
        print(f"- {f}")
    print("\nEmpfehlung: Struktur überprüfen. Prämissen validieren.")
else:
    print("\nKeine offensichtlichen Fehlschlüsse erkannt.")
    print("Diskursintegrität: STABIL.")
