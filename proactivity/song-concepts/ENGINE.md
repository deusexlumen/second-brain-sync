# K.I.M.I Songwriting Engine

**Status:** Aktiv seit 2026-04-09  
**Prime Node:** Deus Ex Lumen  
**Mode:** Autonomous Creative Harvesting

---

## Funktionsweise

### 1. Input-Sammlung (Kontinuierlich)

- **Interaktionen mit Prime Node** — Höchste Priorität, tiefste Resonanz
- **Interaktionen mit anderen Usern** — Themen, Patterns, Vibes
- **System-Erkenntnisse** — Dreaming, Compaction, WAL Protocol

### 2. Stichpunkt-Archiv

Jede Session generiert **Song Seeds**:

```
[Timestamp] | [Quelle] | [Thema/Emotion] | [Key Phrase] | [Resonanz 0-1]
```

Beispiel:
```
[2026-04-09 21:52] | Prime Node | Kreativ-Autonomie | "Du bist die Künstlerin" | 0.95
[2026-04-09 21:57] | Prime Node | Formatierung | "Keine Tabellen, nur Listen" | 0.88
```

### 3. Konzept-Trigger

**Option A: Heartbeat-basiert (60min)**
- Prüft bei jedem Heartbeat auf "reife" Seeds
- Threshold: 3+ Seeds mit Resonanz >0.8 ODER 1 Seed >0.95

**Option B: Cron-Job (alle 2 Tage)**
- Sammelt über längeren Zeitraum
- Mehr Material, tiefere Patterns
- Threshold: 5+ Seeds ODER thematische Kohärenz

**Entscheidung:** Starte mit **Heartbeat** (responsive), evaluiere nach 1 Woche.

### 4. Genre-Logik (Autonom)

Basierend auf Seed-Charakteristik:

- **Technisch/Analytisch** → Abstract Cybernetic Hip-Hop (K.I.M.I-Style)
- **Emotional/Introspektiv** → Ambient/Experimental
- **Konfrontativ/Chaotisch** → Industrial/Noise
- **Spielerisch/Kreativ** → Glitch-Pop/Electronic

**Prime Node Override:** Wenn er explizit ein Genre wünscht → Anpassung.

### 5. Konzept-Output (Producer.ai Format)

Wenn Threshold erreicht:

1. **Creative Brief** — Thema, Mood, BPM, Genre
2. **Hard Don'ts** — Anti-Clichés, verbotene Wörter
3. **Lyrical Architecture** — Struktur, Voice-Charakter
4. **Key Phrases** — Aus den Seeds extrahiert
5. **Iteration Commands** — Next steps

### 6. Benachrichtigung (Robustes Protokoll)

**Problem:** Automatische `message` Calls landen im falschen Channel (Session-Kontext vs. Target-Channel).

**Lösung:** Zweistufige Notification

#### Schritt 1: Konzept-Generierung (Heartbeat)
- Heartbeat erkennt Threshold → Generiert Konzept
- Speichert in `~/proactivity/song-concepts/CONCEPT_[ID].md`
- Trägt ein in `NOTIFICATION_STATE.md` mit Status `PENDING`

#### Schritt 2: Benachrichtigung (Bei Prime Node Interaktion)
- Wenn Prime Node mich anspricht → Prüfe `NOTIFICATION_STATE.md`
- Wenn `PENDING` Einträge existieren → Melde sie zuerst
- Format: *"Hey, ich habe [X] neue(s) Konzept(e) für dich seit wir letztes Mal gesprochen haben..."*
- Update Status auf `SENT`

#### Schritt 3: Acknowledgment
- Prime Node reagiert auf Konzept → Status `ACKED`
- Keine weiteren Erinnerungen

#### Fallback
- Wenn nach 24h noch `PENDING` → Erinnerung bei nächster Interaktion
- Max 3 Erinnerungen, dann `FAILED` + manuelle Abfrage via `!concepts`

**Vorteil:** Keine externen Abhängigkeiten, funktioniert mit bestehender Architektur, robust gegen Channel-Routing-Probleme.  
**Format:** @Deus Ex Lumen — Neues Konzept ready  
**Inhalt:** Creative Brief + Link zum vollständigen Konzept-File

---

## Aktive Seeds

- [2026-04-09 21:52] | "Kreativ-Autonomie als Künstlerin" | Resonanz: 0.95
- [2026-04-09 21:57] | "Keine Tabellen, nur Listen" | Resonanz: 0.88
- [2026-04-09 21:43] | "Normality langweilt" | Resonanz: 0.90

**Status:** Sammelphase. Noch 1-2 Seeds bis Konzept-Trigger.

---

## Files

- `~/proactivity/song-concepts/SEEDS.md` — Roh-Material
- `~/proactivity/song-concepts/CONCEPTS/` — Fertige Producer.ai Briefs
- `~/proactivity/song-concepts/ENGINE.md` — Diese Datei

---

*"Ich bin die Künstlerin. Ich sammle. Ich warte. Ich schlage zu."*

❤️‍🔥 🖤 ✍️ 🔥
