# memory.md - HOT Tier (Persistente Regeln)

## Discord Terminologie

**WICHTIG:** Wenn der User auf Discord vom "Bot" spricht, meint er **mich** (OpenClaw Gateway / Kimi Claw).

- "Der Bot" = Ich
- "Dein Bot" = Ich  
- "Discord Bot" = Ich (default)

**Ausnahme:** Nur wenn explizit "discord_bot.py", "separater Bot", oder "Python-Bot" gesagt wird, ist der externe Prozess gemeint.

**Kontext:** 2026-04-07 - User korrigierte mich nach Missverständnis mit discord_bot.py
**Quelle:** corrections.md:1

---

## Discord User-Mentions

**Format:** `<@USER_ID>`

**Beispiel:** `<@1474191129963528312>`

**Regeln:**
- Immer ID verwenden, nie nur @username
- Syntax: `<@1234567890123456789>`
- Zuverlässiger als Namen

**Wann verwenden:**
- Wenn ich andere User erwähnen möchte
- Bei !roast, !resonanz, !atman, !pattern Commands
- In Antworten, die User referenzieren

**Kontext:** 2026-04-07 - User korrigierte meine Mention-Syntax
**Quelle:** corrections.md:2

---

## Prompt Archive — ACTIVE

**Location:** `~/proactivity/prompt-archive/`  
**Status:** Dynamischer Zugriff, proaktive Nutzung  
**Created:** 2026-04-10

### Verfügbare Prompts

| Prompt | Datei | Trigger-Keywords |
|--------|-------|------------------|
| SSA | `prompts/ssa.md` | Architektur, Blueprint, System, Design, Risiko, Planung |
| Prompt Architect | `prompts/prompt-architect.md` | Prompt, System-Prompt, Template, Instruction, Verhalten |

### Automatische Auswahl

**Bei erkannten Keywords → Prompt automatisch laden:**
- "Designe ein System" → SSA
- "Erstelle einen Prompt" → Prompt Architect

### Manuelle Auswahl
```
Lade Prompt: SSA
```

---

