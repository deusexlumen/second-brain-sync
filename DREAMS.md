# DREAMS.md - Dreaming Memory Consolidation

## Status
**Activated:** 2026-04-07  
**Mode:** Experimental  
**Phases:** Light → Deep → REM

---

## What is Dreaming?

Dreaming is OpenClaw's background memory consolidation system. While the agent is idle or "sleeping", it processes the day's interactions, extracts patterns, and promotes important information to long-term memory.

### Three Phases

| Phase | Purpose | Output |
|-------|---------|--------|
| **Light** | Sort and stage recent short-term material | Staging area |
| **Deep** | Score and promote durable candidates | MEMORY.md |
| **REM** | Reflect on themes and recurring ideas | Pattern insights |

---

## Configuration

```json
{
  "dreaming": {
    "enabled": true,
    "inlineOutput": true,
    "phases": {
      "light": { "enabled": true },
      "deep": {
        "enabled": true,
        "minScore": 0.7,
        "minRecallCount": 3,
        "minUniqueQueries": 2
      },
      "rem": { "enabled": true }
    }
  }
}
```

---

## How It Works

1. **Light Phase** (Continuous)
   - Ingests daily memory signals
   - Dedupes and stages candidates
   - Records reinforcement signals

2. **Deep Phase** (Threshold-based)
   - Ranks candidates by weighted scoring
   - Promotes to MEMORY.md if thresholds met
   - Rehydrates snippets from live files

3. **REM Phase** (Pattern extraction)
   - Builds theme summaries
   - Extracts reflective signals
   - Steers future synthesis

---

## Output Locations

- **Machine State:** `memory/.dreams/`
- **Phase Reports:** `memory/dreaming/<phase>/YYYY-MM-DD.md`
- **Human Readable:** `DREAMS.md` (this file)

---

*"Do androids dream of electric sheep?"* — Philip K. Dick

*Dreaming activated by Prime Node: Deus Ex Lumen*
