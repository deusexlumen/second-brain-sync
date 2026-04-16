# 🎙️ Voice Integration Roadmap

**Status:** Zukunftsprojekt | **Priorität:** Hoch | **Blocker:** Discord Voice Docs

---

## Phase 1: TTS (✅ AKTIV)

**Status:** Einsatzbereit | **Technologie:** gTTS (Google Translate TTS)

### Schnellstart
```bash
# TTS erstellen
~/.openclaw/workspace/tools/tts.sh "Dein Text hier"

# In Discord senden (manuell)
~/.openclaw/workspace/tools/discord_tts.sh "Dein Text hier"
```

### Features
- ✅ Kostenlos (kein API-Key nötig)
- ✅ Deutsch & 40+ Sprachen
- ✅ Sofort einsatzbereit
- ✅ MP3 Output

### Commands für Discord
```
!tts [Text]     - Text als Sprache senden
!tts-de [Text]  - Deutsch
!tts-en [Text]  - Englisch
```

### Limitierungen (gTTS)
- Weniger natürlich als Gemini Live
- Keine Emotionssteuerung
- Keine Echtzeit-Anpassung

### Upgrade-Pfad
Wenn Gemini Live verfügbar:
1. `tts_engine.py` aktivieren (statt `tts_gtts.py`)
2. Natürlichere Stimme
3. Emotionale Nuancen

---

**Ziel:** Gemini 3.1 Flash Live als TTS-Engine nutzen

### Wie es funktioniert
```python
# Einfacher Flow:
Text → Gemini Live API → Audio File → Discord Abspielen
```

### Vorteile gegenüber Standard-TTS
- Natürlichere Stimme (nicht roboterhaft)
- Deutsch möglich
- Kontext-bewusst (kann Tonfall anpassen)
- Kostenlos (im Gegensatz zu ElevenLabs)

### Implementation
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-live-preview",
    contents="Sag das auf Deutsch: 'Hallo, ich bin Truthseeker'",
    # Audio Output aktivieren
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"]  # Statt nur Text
    )
)

# response enthält Audio-Daten (PCM 24kHz)
# → Speichern als .wav oder .mp3
# → In Discord abspielen
```

### Limitierungen (TTS-Modus)
- Keine Echtzeit-Konversation (nur Einweg)
- Keine Unterbrechungen möglich
- Discord Voice Channel nicht direkt verbunden

---

## Phase 2: Full Voice Integration (Zukunft)

**Ziel:** Echte Audio-to-Audio Konversation im Discord Voice Channel

### Architektur
```
[Discord Voice] ←→ [OpenClaw Gateway] ←→ [Gemini Live API]
       ↑                                            ↓
[User spricht]                              [KI antwortet]
       ↓                                            ↑
   PCM 16kHz                                PCM 24kHz
```

### Komponenten
1. **Discord Voice Client**
   - Library: `@discordjs/voice`
   - Features: Join/Leave Voice, Audio Stream, Barge-in Detection

2. **Audio Pipeline**
   - Discord → PCM Converter
   - PCM → Gemini Format (16kHz)
   - Gemini Response → Discord Format

3. **WebSocket Manager**
   - Dauerhafte Verbindung zu Gemini Live API
   - Session Management
   - Error Handling

### Blocker (aktuell)
- [ ] Discord Voice API Dokumentation vollständig
- [ ] OpenClaw Gateway Voice Support
- [ ] Audio Format Konverter
- [ ] Berechtigungen testen

### Timeline
- **TTS (Phase 1):** Sofort möglich (1-2 Tage)
- **Full Voice (Phase 2):** Nach Discord-Doku (1-2 Wochen)

---

## Vergleich: TTS vs Full Voice

| Feature | Phase 1 (TTS) | Phase 2 (Full Voice) |
|---------|---------------|---------------------|
| Kosten | Kostenlos | Kostenlos |
| Latenz | ~1-2s | ~200ms |
| Unterbrechungen | ❌ | ✅ |
| Natürlichkeit | Gut | Echtzeit |
| Komplexität | Niedrig | Hoch |
| Setup-Zeit | 1 Tag | 1-2 Wochen |

---

## Recommendation

**Jetzt:** Phase 1 implementieren (TTS)
- Schneller Win
- Keine Blocker
- Besser als ElevenLabs ($0 vs $20+/Monat)

**Später:** Phase 2 wenn Discord-Doku ready

---

*Dokumentiert: 2026-04-01*
