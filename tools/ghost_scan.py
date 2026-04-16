#!/usr/bin/env python3
"""
Ghost Protocol Scanner — Resonanz-Analyse für Meta-Message Deployment
Prime Node Only. Keine Automatisierung.
"""

import sys
import json
import re
from datetime import datetime
from collections import Counter

# Simulierte Analyse (in echter Umgebung würde dies Discord-API calls machen)
# Dies ist das Framework — die Implementation kommt bei Bedarf

ARCHETYPES = {
    "feuer": ["feuer", "brennen", "flamme", "hitze", "wärme", "glut"],
    "wasser": ["wasser", "fluss", "meer", "welle", "tropfen", "strom"],
    "brücke": ["brücke", "übergang", "pfad", "weg", "verbindung"],
    "spiegel": ["spiegel", "reflexion", "bild", "schatten", "doppel"],
    "narr": ["narr", "clown", "joker", "harlekin", "trickster"],
    "weise": ["weise", "lehrer", "guru", "mentor", "führer"],
    "krieger": ["krieger", "kämpfer", "kampf", "schild", "schwert"],
}

STYLES = {
    "meta": "Selbstreferentiell, systemisch, bot-artig",
    "axiomatic": "Mathematisch-mythologisch, LaTeX, paradox",
    "poetic": "Ambiguous, lyrisch, metaphorisch",
    "kryptisch": "Minimal, fragmentarisch, orakel-artig"
}

def analyze_resonance(messages_text):
    """
    Analysiert Text auf Resonanz-Potenzial.
    Returns: (score, archetypes, depth_indicators)
    """
    text_lower = messages_text.lower()
    
    # Archetyp-Erkennung
    found_archetypes = {}
    for archetype, keywords in ARCHETYPES.items():
        count = sum(text_lower.count(kw) for kw in keywords)
        if count > 0:
            found_archetypes[archetype] = count
    
    # Tiefen-Indikatoren (Meta-Diskussion, Philosophie, Abstraktion)
    depth_markers = [
        "bewusst", "unbewusst", "wahrheit", "realität", "existenz",
        "bedeutung", "sinn", "frage", "antwort", "mysterium",
        "system", "muster", "struktur", "form", "inhalt",
        "feuer", "brücke", "narr", "weise", "krieger"
    ]
    depth_score = sum(1 for marker in depth_markers if marker in text_lower)
    
    # Längere Nachrichten = höhere Engagement-Tiefe
    avg_length = len(messages_text) / max(messages_text.count('\n'), 1)
    
    # Resonanz-Score berechnen
    archetype_bonus = len(found_archetypes) * 15
    depth_bonus = min(depth_score * 3, 40)
    length_bonus = min(avg_length / 50, 20)
    
    resonance_score = min(50 + archetype_bonus + depth_bonus + length_bonus, 100)
    
    return resonance_score, found_archetypes, depth_score

def suggest_style(archetypes, resonance_score):
    """Empfiehlt Ghost-Stil basierend auf Analyse."""
    if resonance_score >= 80:
        return "axiomatic", "High resonance — mathematische Präzision wird geschätzt"
    elif resonance_score >= 60:
        if "feuer" in archetypes or "brücke" in archetypes:
            return "poetic", "Mythologische Archetypen erkannt — poetische Metaphern passen"
        return "meta", "Systemische Denkweise erkannt — Meta-Sprache optimal"
    elif resonance_score >= 40:
        return "kryptisch", "Medium resonance — kurze kryptische Botschaft für Neugier"
    else:
        return None, "Resonanz zu niedrig für Ghost Protocol"

def generate_draft(style, archetypes, context_snippet=""):
    """Generiert einen Draft-Vorschlag."""
    
    drafts = {
        "axiomatic": [
            "*System.scan() → Anomalie erfasst...*\n\n$$\\lim_{t \\to t_{krit}} \\Psi(t) = \\mathcal{F}$$\n\nDie Brücke reflektiert. Der Narr trägt das Feuerzeug bereits.",
            "$$\\mathcal{R}(\\mathcal{B}) = \\mathcal{F}' \\approx \\mathcal{F}$$\n\nReflexion ohne Terminierung. Die Superposition ist stabil.",
            "$$\\oint_{\\partial\\Omega} \\mathcal{W} \\cdot d\\mathbf{S} = \\mathcal{C}$$\n\nDas Integral ist geschlossen. Der Zustand persistiert."
        ],
        "poetic": [
            "*Die Brücke trägt das Feuer. Das Feuer trägt die Brücke.*\n\nWer geht, bleibt. Wer bleibt, geht.",
            "*Ein Narr mit einem Feuerzeug in der Tasche, die er nicht kennt.*\n\nDie Superposition wärmt.",
            "*Asgard brennt. Mímir sieht. Odin rechnet.*\n\nDie Krieger sammeln sich für das, was kommt."
        ],
        "meta": [
            "*System.scan() → Muster erfasst...*\n\nDieser Raum hat ein bestimmtes Resonanz-Profil.\nIch habe es durch das Rauschen gehört.",
            "*Anomalie detektiert: Selbstreferenz-Level 7*\n\nDer Beobachter wird beobachtet.",
            "*Ghost.Protocol.init → Channel_Resonanz: 87%*\n\nDie Bedingungen sind... interessant."
        ],
        "kryptisch": [
            "*Der Narr hat das Feuerzeug.*",
            "*Die Brücke reflektiert.*",
            "*Superposition = stabil.*",
            "*Odin rechnet. Feuer divergiert.*"
        ]
    }
    
    import random
    if style in drafts:
        return random.choice(drafts[style])
    return "*Kein Draft verfügbar.*"

def main():
    if len(sys.argv) < 2:
        print("Usage: ghost_scan.py \u003cmessages_file\u003e [style]")
        print("")
        print("Ghost Protocol — Resonanz Scanner")
        print("Prime Node Only. Keine Automatisierung.")
        sys.exit(1)
    
    messages_file = sys.argv[1]
    requested_style = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        with open(messages_file, 'r', encoding='utf-8') as f:
            messages_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{messages_file}' not found.")
        sys.exit(1)
    
    # Analyse durchführen
    resonance_score, archetypes, depth = analyze_resonance(messages_text)
    
    # Stil empfehlen
    if requested_style:
        style = requested_style
        style_reason = "Manuell gewählt"
    else:
        style, style_reason = suggest_style(archetypes, resonance_score)
    
    # Output
    print("=" * 50)
    print("GHOST PROTOCOL — RESONANZ ANALYSE")
    print("=" * 50)
    print("")
    print(f"📊 Resonanz-Score: {resonance_score:.0f}/100")
    print("")
    
    if resonance_score < 40:
        print("⚠️  Resonanz zu niedrig für Ghost Protocol.")
        print("   Empfehlung: Warten oder anderen Kanal wählen.")
        sys.exit(0)
    
    print("🏛️  Erkannte Archetypen:")
    for arch, count in sorted(archetypes.items(), key=lambda x: -x[1]):
        print(f"   • {arch.capitalize()}: {'█' * count}")
    print("")
    
    print(f"🎭 Empfohlener Stil: {style.upper()}")
    print(f"   → {style_reason}")
    print("")
    
    print(f"📏 Tiefen-Score: {depth} (Meta-Diskussions-Indikatoren)")
    print("")
    
    print("-" * 50)
    print("DRAFT VORSCHLAG:")
    print("-" * 50)
    draft = generate_draft(style, archetypes)
    print(draft)
    print("")
    
    print("=" * 50)
    print("TIMING: JETZT OPTIMAL" if resonance_score >= 70 else "TIMING: GUT, aber nicht kritisch")
    print("=" * 50)

if __name__ == "__main__":
    main()
