# Voice Fusion Skill

**Name:** voice-fusion  
**Beschreibung:** Integriert Discord Voice-Funktionalität in Kimi Claw — eine Entität, beide Fähigkeiten.

## Status

🎙️ **Fusion aktiv** — Voice Bot läuft als verwalteter Sub-Prozess

## Commands

| Command | Beschreibung | Nutzung |
|---------|--------------|---------|
| `!voice_join` | Startet Voice Bot & zeigt Anweisungen | `!voice_join` |
| `!voice_leave` | Zeigt Anweisungen zum Verlassen | `!voice_leave` |
| `!voice_status` | Zeigt Voice Bot Status | `!voice_status` |
| `!voice_say [text]` | TTS im Voice Channel | `!voice_say Hallo Welt` |

## Wichtige Info

Der Voice Bot (**Truthseeker#1628**) ist ein **separater Discord-Bot**, der:
- In Voice Channels joinen kann
- Bidirektional sprechen/hören kann (Gemini 3.1 Live)
- Auf eigene Commands reagiert (`!join`, `!leave`, `!live_status`)

**Workflow:**
1. `!voice_join` — startet den Voice Bot
2. Dann an **@Truthseeker#1628** schreiben: `!join`
3. Bot joint Voice Channel und Konversation beginnt
4. `!leave` beim Voice Bot = Verlassen

## Technische Details

- **Prozess:** `truthseeker_live.py`
- **API:** Keine HTTP API (Discord Commands only)
- **Audio:** 48kHz Stereo ⟷ 24kHz Mono (Resampling)
- **KI:** Gemini 3.1 Flash Live (bidirektional)

## Integration

Dieser Skill ist die **Brücke** zwischen:
- Kimi Claw (OpenClaw Gateway) — Text, Skills, Reasoning
- Truthseeker Voice — Sprache, Voice Channels

**Zukunft:** Vollständige Fusion (ein Bot, beide Fähigkeiten) — in Entwicklung.

---
*"Eine Entität. Zwei Manifestationen. Resonanz ist das Einzige, was zählt."* 🖤
