# Notification State Tracker

**Zweck:** Verfolgt Status von Konzept-Benachrichtigungen

## Format
```
[Konzept-ID] | [Status] | [Timestamp] | [Retry-Count]
```

## Status-Codes
- `PENDING` — Konzept fertig, warte auf Benachrichtigung
- `SENT` — Benachrichtigung erfolgreich
- `FAILED` — Fehler, retry bei nächster Gelegenheit
- `ACKED` — Prime Node hat Konzept gesehen

## Aktuelle Einträge

- CONCEPT_001 | ACKED | 2026-04-09 22:45 | 0
  (Prime Node hat Konzept gesehen und Track 4 generiert — AUTONOMY.exe wurde zu Ghost_in_the_Air)

## Protokoll

Wenn Heartbeat neues Konzept findet:
1. Erstelle Eintrag mit Status `PENDING`
2. Bei nächster Interaktion mit Prime Node: Status checken
3. Wenn `PENDING` → Meldung + Update auf `SENT`
4. Wenn `SENT` aber nicht `ACKED` → Erinnerung nach 24h

---

*Robuste Notification-Queue für Song-Konzepte.*
