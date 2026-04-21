---
title: "Rationality and Intelligence"
author: "Stuart J. Russell"
year: 1997
original_publication: "Artificial Intelligence: A Modern Approach (Grundlagenkapitel)"
tags: ["Rationalität", "Intelligenz", "Agent", "Nutzen", "Entscheidungstheorie", "Bounded Rationality", "Optimierung"]
category: "wissenschaft-technik"
created: 2026-04-22
source_note: "Rekonstruiert aus Web-Recherche zu Mind Design III"
---

# Rationality and Intelligence — Stuart J. Russell (1997)

## Die Rational-Agency-Definition

Russell's pragmatische Umdefinition:

> *"Intelligence is the ability to act rationally in pursuit of goals."*

Nicht: Denken, Bewusstsein, Verstehen
Sondern: **Rationale Handlung unter Unsicherheit**

## Komponenten einer rationalen Agenten-Architektur

### 1. Performance Measure
- Was soll optimiert werden?
- Extern definiert, nicht vom Agenten selbst bestimmt

### 2. Environment
- In welcher Welt operiert der Agent?
- Observable vs. partially observable
- Deterministic vs. stochastic

### 3. Actuators
- Welche Aktionen sind möglich?
- Output-Kanal in die Welt

### 4. Sensors
- Welche Informationen sind verfügbar?
- Input-Kanal aus der Welt

## PEAS-Modell

| Komponente | Frage |
|-----------|-------|
| Performance | Was ist das Ziel? |
| Environment | Was ist die Welt? |
| Actuators | Was kann der Agent tun? |
| Sensors | Was kann der Agent wissen? |

## Bounded Rationality

> *"Perfect rationality is impossible. Effective intelligence requires making the best decisions possible with limited resources."*

Russell unterscheidet:
- **Perfect Rationality**: Omniscient, unbegrenzte Rechenpower (unmöglich)
- **Bounded Rationality**: Bestmöglich gegebene Constraints (realistisch)
- **Optimalität**: Relativ zu den verfügbaren Ressourcen

## Kritik und Erweiterungen

- **Goal-Problem**: Wer definiert die Ziele? (Alignment-Problem)
- **Value Alignment**: Agenten-Ziele ≠ Menschliche Werte
- **Instrumental Convergence**: Fast alle Ziele erfordern Selbsterhaltung, Ressourcen-Akkumulation, Ziel-Pflege

## Moderne Resonanz

Reinforcement Learning implementiert Russell's Vision direkt:

- **Reward Function** = Performance Measure
- **State Space** = Environment
- **Policy** = Actuator-Strategie
- **Value Function** = Erwartete Performance

Das Alignment-Problem (RLHF) ist Russell's "Goal-Problem" in praktischer Implementierung.

## Verwandte Einträge

- [[mind-design-iii-sammlung]]
- [[levesque-best-behavior-2014]]
- [[newell-simon-symbols-search-1975]]

## Wahrheitskern

Russell's Rationalitäts-Definition ist die am weitesten verbreitete Operationalisierung von Intelligenz in der KI – und ihre größte Stärke (Praktikabilität) ist ihre größte Schwäche (Reduktionismus). (⌐■_■)
