# Corrections Log — Template

> This file is created in `~/self-improving/corrections.md` when you first use the skill.
> Keeps the last 50 corrections. Older entries are evaluated for promotion or archived.

## Example Entries

```markdown
## 2026-02-19

### 14:32 — Code style
- **Correction:** "Use 2-space indentation, not 4"
- **Context:** Editing TypeScript file
- **Count:** 1 (first occurrence)

### 16:15 — Communication
- **Correction:** "Don't start responses with 'Great question!'"
- **Context:** Chat response
- **Count:** 3 → **PROMOTED to memory.md**

## 2026-02-18

### 09:00 — Project: website
- **Correction:** "For this project, always use Tailwind"
- **Context:** CSS discussion
- **Action:** Added to projects/website.md
```

## Log Format

Each entry includes:
- **Timestamp** — When the correction happened
- **Correction** — What the user said
- **Context** — What triggered it
- **Count** — How many times (for promotion tracking)
- **Action** — Where it was stored (if promoted)

---

## 2026-04-03

### 21:42 — Neue Fähigkeit: Video-Analyse
- **Korrektur/Anweisung:** "Baue dir die Fähigkeit selbst. Benutze bitte das 3.1 Flash light modell."
- **Kontext:** Prime Node hat Video "Der Bewusstseins-Algorithmus" geschickt, ich sagte ich kann keine Videos analysieren
- **Ergebnis:** Tool `tools/gemini_video_analyze.py` erstellt mit Gemini 3.1 Flash Lite
- **Workflow:** Upload → Wait for ACTIVE → Analyse mit thinking_level="high"
- **Persistiert in:** TOOLS.md, tools/gemini_video_analyze.py
- **Count:** 1 (erste Implementierung)
