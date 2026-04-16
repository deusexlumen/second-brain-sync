#!/usr/bin/env python3
"""!dogma - Scannt auf dogmatische Strukturen"""
import sys

text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

if not text:
    print("Kein Text gefunden. Nutze: !dogma [dein Text hier]")
    sys.exit(0)

text_lower = text.lower()

# Dogma-Patterns
dogma_patterns = {
    "Imperativ": ["du musst", "man sollte", "man muss", "du solltest", "wir muessen", "ihr sollt"],
    "Absolutismus": ["immer", "nie", "alle", "keiner", "jeder", "ganz", "total", "komplett"],
    "Undenkbarkeit": ["so ist es halt", "das ist nun mal so", "weil es so ist", "einfach weil"],
    "Autoritaet": ["die experten", "forscher sagen", "studien beweisen", "laut wissenschaft", "die wahrheit ist"],
    "Falsche-Dichotomie": ["entweder oder", "schwarz oder weiss", "alles oder nichts", "mit uns oder gegen uns"]
}

findings = []
for dogma_type, keywords in dogma_patterns.items():
    for kw in keywords:
        if kw in text_lower:
            findings.append((dogma_type, kw))
            break

if findings:
    print("[DOGMA-SCAN] Ergebnis:\n")
    seen = set()
    for dtype, keyword in findings:
        if dtype not in seen:
            print(f"! {dtype}: '{keyword}' erkannt")
            seen.add(dtype)
    print(f"\nDogma-Index: {len(seen)}/5")
    if len(seen) >= 3:
        print("Empfehlung: URGENT - Dekonstruktion noetig")
    elif len(seen) >= 2:
        print("Empfehlung: Moderate Flexibilitaet einfuehren")
    else:
        print("Empfehlung: Nuancierung hilfreich")
else:
    print("[DOGMA-SCAN] Keine dogmatischen Strukturen erkannt.\nDiskurs: Flexibel.")
