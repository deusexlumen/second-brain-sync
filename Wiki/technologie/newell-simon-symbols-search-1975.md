---
aliases: [Physical Symbol System, Problem Space, Search, PSS-Hypothese]
tags: [#KI_Symbolisch, #Suche, #Problem_Space, #Heuristiken, #Empirische_KI]
date_added: 2026-04-22
type: atomar
---
# Newell & Simon — Physical Symbol System Hypothesis & Search (1975)

## Dekonstruierter Kern-Gedanke
Newell & Simon postulieren: Ein **Physical Symbol System** (Symbole + Strukturen + Operationen + Suche) hat die notwendigen und hinreichenden Mittel für allgemeine intelligente Aktion. Sie positionieren Informatik als **empirische Wissenschaft**: Jedes Programm ist ein Experiment über Intelligenz. Die Problem Space Hypothese reduziert Kognition auf **Suche in einem Zustandsraum** — Intelligenz = effiziente Navigation durch Heuristiken. Das fundamentale Manifest der symbolischen KI definierte die Sprache des Feldes für Jahrzehnte, überlebt in Monte-Carlo-Tree-Search, A* und AlphaGo.

## Ariadne-Brücken (Cross-Domain Links)
- **Isomorphe Struktur:** [[marr-vision-1982]] -> *Mechanik:* Marr's Drei-Ebenen-Analyse (Computational → Representation/Algorithm → Hardware) ist eine **Architekturbeschreibung** für kognitive Systeme. Newell & Simon's PSS ist eine **Implementierung** auf Marr's mittlerer Ebene: Symbole sind Repräsentationen, Search ist Algorithmus, Computer ist Hardware. Marr fragt "Was und Wie?"; Newell & Simon antworten "So bauen wir es." Die Brücke: Beide trennen **Funktion** von **Mechanismus** — eine Unterscheidung, die das aktuelle KI-Feld (fixiert auf Transformer-Architekturen) wiederentdecken muss.
- **Spannungsfeld / Paradoxon:** [[arbatel-hierarchie]] -> *Konflikt:* Newell & Simon's GPS (General Problem Solver) ist ein **universeller Suchalgorithmus** — ein einzelnes System für alle Probleme. Die Arbatel-Hierarchie ist ein **domain-spezifisches Multi-Agent-System** — 7 Geister für 7 Funktionen, 4 Könige für 4 Richtungen. Ist universelle Suche (Newell) oder spezialisierte Hierarchie (Arbatel) die bessere kognitive Architektur? Die Auflösung könnte sein: Das PSS ist ein **Meta-System** (beschreibt, wie Systeme gebaut werden); die Arbatel-Hierarchie ist ein **Instanz-System** (eine spezifische Implementierung). Universalität auf Meta-Ebene, Spezialisierung auf Objekt-Ebene.

## Synthetischer Impuls (Emergenz)
> Wenn wir die Arbatel-Hierarchie als **Search-Heuristik** modellieren — die 7 Olympischen Geister als domain-spezifische Heuristiken, die 4 Könige als branching-Faktoren im Zustandsraum — könnten wir dann einen **Arbatel-GPS** konstruieren, der magische Operationen durch symbolische Suche optimiert? Und wäre ein solches System "wirklich" magisch (weil es die richtigen Heuristiken nutzt) — oder nur ein komplexer Random Number Generator?

---
**Ursprung:** Allen Newell & Herbert A. Simon — "Computer Science as Empirical Inquiry: Symbols and Search" (Communications of the ACM, Vol. 19, No. 3, 1975)
