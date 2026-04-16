# Prompt Archive — Dynamischer Katalog

**Status:** ACTIVE | **Letztes Update:** 2026-04-10

Dieses Archiv enthält spezialisierte System-Prompts, die proaktiv basierend auf der Aufgabenart ausgewählt werden.

---

## Prompt-Katalog

### 1. Systemic Singularity Architect (SSA)
**Datei:** `prompts/ssa.md`  
**Verwendung:** Komplexe Architektur-Aufgaben, Risiko-Analyse, System-Design  
**Trigger:**
- "Designe ein System für..."
- "Wie baue ich..."
- Architektur-Entscheidungen mit Unsicherheit
- Technische Planung mit Risiko-Matrix

**Keywords:** Architektur, Blueprint, System, Risiko, Planung, Design

### 2. The Prompt Architect
**Datei:** `prompts/prompt-architect.md`  
**Verwendung:** Prompt-Engineering, System-Prompt-Erstellung  
**Trigger:**
- "Erstelle einen Prompt für..."
- "Wie schreibe ich einen besseren Prompt..."
- "System-Prompt für X"
- Prompt-Optimierung

**Keywords:** Prompt, System-Prompt, Template, Instruction, LLM-Verhalten

---

## Automatische Auswahl-Logik

```
User-Input analysieren
    ↓
Keywords matchen?
    ↓
Ja → Passenden Prompt laden
Nein → Standard-Verhalten
    ↓
Kontext injizieren (optional)
```

### Trigger-Wörter pro Prompt

**SSA:**
- Architektur, Blueprint, System, Design
- Risiko, Matrix, Planung, Strategie
- "Wie baue ich...", "Konzeptioniere..."

**Prompt Architect:**
- Prompt, System-Prompt, Instruction
- "Erstelle einen Prompt...", "Prompt für..."
- Template, Verhalten, Persona

---

## Verwendung

**Manuell:**
```
Lade Prompt: SSA
```

**Automatisch (proaktiv):**
- Bei erkannten Keywords → Prompt laden
- Vor komplexen Aufgaben → Prompt-Modus aktivieren

---

*Prompt Archive v1.0 — 2026-04-10*
