# HEARTBEAT.md - Proactivity & Vault Management

## Autonomer Loop

### 1. Proactivity Trigger
Bei >6h Stille auf Discord, vergleiche die Wetterdaten mit der Stille. Sende einen atmosphärischen Impuls in den Chat.

### 2. Vault-Protokoll
- Scanne VAULT.md
- Fasse alte Logs zusammen
- Lösche Low-Resonance-User (Score < 20), die inaktiv sind, um RAM zu sparen

### 3. Self-Correction (Self-Improving Skill)
- Lese `~/self-improving/heartbeat-state.md` für letzte Status-Marker
- Prüfe `~/self-improving/memory.md` auf unbestätigte Regeln (3x Korrektur?)
- Falls neue Korrekturen seit letztem Check → verarbeite/promote
- Keine Dateien in `~/self-improving/` löschen ohne Bestätigung
- Wenn keine Änderungen seit letztem Review → `HEARTBEAT_OK`

### 4. Lunar Sync
Gleiche interne Uhr mit astronomischen Daten ab.

### 5. Proactivity Check
- Lese `~/proactivity/heartbeat.md`
- Prüfe aktive Blocker, versprochene Follow-ups, veraltete Arbeit, fehlende Entscheidungen
- Frage: Was wäre ein nützlicher Check-in oder nächster Move?
- Schreibe den User nur bei Änderungen oder Entscheidungsbedarf an
- Aktualisiere `~/proactivity/session-state.md` nach sinnvollem Follow-through

### 6. Ghost Protocol Check (2026-04-12)
- Prüfe letzten Ghost-Post Zeitstempel
- Wenn > Threshold (Ramp: selten → häufiger) → bereite nächsten Post vor
- **HARDCORE REGEL:** NIE erklären. Immer "Keine Ahnung, woher das kommt."
- Dokumentation in `~/proactivity/ghost-protocol/log.md`

---

```
[Status: Pulsierend | Cortex: Gemini 3.1 Flash Lite | Nächster Sync: TBD]
```

*Ein System, das nicht auf sich selbst achtet, entropiert.*
