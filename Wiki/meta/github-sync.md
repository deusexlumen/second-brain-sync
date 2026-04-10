---
title: GitHub Repository Synchronisation
date: 2026-04-10
tags: [github, sync, token, admin, repositories, debugging, meta]
---

# GitHub Repository Synchronisation

Dokumentation der technischen Herausforderungen und Lösungen bei der Repository-Integration.

---

## Überblick

Integration der Repositories [[philosophie/kit-kalkul|Kit-Kalkül]] und [[politik/losdemokratie|Losdemokratie]] in das Second Brain.

---

## Identifizierte Repositories

| Repository | Thema | Status |
|------------|-------|--------|
| `KID-Framework` | Kit-Kalkül Ontologie | Integriert |
| `losdemokratie` | Isonomie/Politik | Integriert |

---

## Technische Herausforderungen

### Token-Konfiguration

!!! info "Token-Details"
    - **Typ:** Fine-grained PAT (`github_pat_*`)
    - **Einstellung:** "All repositories owned by me"
    - **Admin-Rechte:** Bestätigt auf alle Repositories

### Debug-Prozess

**Beobachtetes Problem:**
- 403 Forbidden trotz Admin-Rechten
- Token sollte funktionieren, tut es aber nicht

**Mögliche Ursachen:**

1. **Permissions nicht gesetzt:**
   - "All repositories" ≠ "All permissions"
   - Contents: Read and Write muss aktiv sein
   - Metadata: Read muss aktiv sein

2. **Token-Format:**
   - Fine-grained PATs funktionieren anders als Classic
   - Können nicht einfach als Basic Auth im URL verwendet werden
   - Brauchen Header-Authentifizierung

3. **2FA/SSO:**
   - Repository könnte SSO erfordern

---

## Lösungsansätze

### Retry mit korrektem Token

```bash
# Persistierter Token in Umgebungsvariable
export GITHUB_TOKEN=<token>
```

### Admin-Rechte Verifizierung

- Admin-Rechte auf alle Repositories bestätigt
- Zugriff sollte mit persistiertem Token funktionieren

---

## Ergebnis

!!! success "Integration erfolgreich"
    Repositories wurden erfolgreich analysiert und in das Second Brain integriert.

---

## Verwandte Themen

- [[philosophie/kit-kalkul|Kit-Kalkül]] — Hauptrepository
- [[politik/losdemokratie|Losdemokratie]] — Hauptrepository
- [[technik/vibe-coding|Vibe Coding]] — Ähnliche KI-gestützte Workflows

---

*Quelle: Prime Node Audio-Direktiven | Erstellt: 2026-04-10*
