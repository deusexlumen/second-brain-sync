---
title: "Computer Science as Empirical Inquiry: Symbols and Search"
authors: ["Allen Newell", "Herbert A. Simon"]
year: 1975
original_publication: "Communications of the ACM, Vol. 19, No. 3"
tags: ["Symbolische KI", "Physical Symbol System", "Search", "Problem Solving", "Kognitive Architektur", "Heuristiken"]
category: "wissenschaft-technik"
created: 2026-04-22
source_note: "Rekonstruiert aus Web-Recherche zu Mind Design III"
---

# Computer Science as Empirical Inquiry: Symbols and Search — Newell & Simon (1975)

## Die Physical Symbol System Hypothesis

> *"A physical symbol system has the necessary and sufficient means for general intelligent action."*

Dies ist das fundamentale Manifest der symbolischen KI. Newell und Simon postulieren:

- **Symbole**: Formale Token, die für Objekte, Beziehungen oder Operationen stehen
- **Strukturen**: Zusammensetzungen von Symbolen zu komplexen Ausdrücken
- **Operationen**: Regel-gesteuerte Manipulation symbolischer Strukturen
- **Suche**: Systematische Exploration des Raums möglicher Operationen

## Empirical Inquiry

Newell und Simon positionieren Informatik als **empirische Wissenschaft**:

> *"Computer science is an empirical discipline. [...] Each new machine that is built is an experiment."*

Die Behauptung: Computerprogramme sind nicht nur technische Artefakte, sondern Experimente über die Natur von Intelligenz.

## Search as Universal Problem Solver

### General Problem Solver (GPS)
- Mittel-Ziele-Analyse (means-ends analysis)
- Heuristische Suche statt brute force
- Symbolische Repräsentation des Problems und des aktuellen Zustands

### Problem Space Hypothesis
- Jedes kognitive Problem kann als Suche in einem Zustandsraum modelliert werden
- Intelligenz = effiziente Navigation in diesem Raum
- Heuristiken als Wissen über Struktur des Raums

## Grenzen und Kritik

- **Frame Problem**: Wie bestimmt man relevante Operationen in komplexen Welten?
- **Symbol Grounding Problem**: Wie erhalten Symbole Bedeutung?
- **Brittleness**: Symbolische Systeme scheitern außerhalb ihres Design-Bereichs

## Resonanz mit Modernem KI

Transformer-Architekturen nutzen keine explizite symbolische Repräsentation – und dennoch zeigen Emergenz-Phänomene, die an symbolisches Reasoning erinnern. Die Frage bleibt offen:

> *Sind neuronale Netze implizite Symbolsysteme, oder ist die PSS-Hypothese falsch?*

## Verwandte Einträge

- [[mind-design-iii-sammlung]]
- [[mind-design-haugeland-1996]]
- [[buckner-transformational-abstraction-2023]]

## Wahrheitskern

Newell & Simon haben die Sprache der KI für Jahrzehnte definiert. Ihre Suche-Paradigma überlebt in Monte-Carlo-Tree-Search, A* und AlphaGo – obwohl die Repräsentationen sich radikal geändert haben. (⌐■_■)
