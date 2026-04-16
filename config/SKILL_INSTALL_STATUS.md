# Skill Installation Status
# Truthseeker v6.4 - Auto-Deployment System

## Warteschlange (pending_skills.txt)

| # | Skill | Status | Installiert am |
|---|-------|--------|----------------|
| 1 | discord | ⏳ Pending | - |
| 2 | gemini-web-search | ⏳ Pending | - |
| 3 | weather | ⏳ Pending | - |
| 4 | nano-pdf | ⏳ Pending | - |
| 5 | self-improving | ⏳ Pending | - |
| 6 | playwright | ⏳ Pending | - |

**WICHTIG:** Skills werden ohne Owner-Prefix installiert (z.B. `discord` statt `steipete/discord`)

## Auto-Install Mechanismus

- **Script:** `/root/.openclaw/workspace/tools/auto_install_skills.sh`
- **Cron:** Alle 4 Minuten
- **Log:** `/root/.openclaw/workspace/logs/skill_install.log`
- **Ziel:** `/root/.openclaw/workspace/skills/`
- **Lock-File:** Verhindert parallele Ausführung

## Entdeckte Skills (korrekte Slugs)

| Ursprünglicher Name | Korrekter Slug | Owner | Status |
|---------------------|----------------|-------|--------|
| steipete/discord | discord | steipete | ⏳ |
| steipete/gemini | gemini-web-search | - | ⏳ |
| steipete/weather | weather | - | ⏳ |
| steipete/nano-pdf | nano-pdf | - | ⏳ |
| ivangdavila/self-improving | self-improving | - | ⏳ |
| ivangdavila/playwright | playwright | - | ⏳ |

## Rate Limit Status

- **Limit:** 30 Anfragen (strenger als erwartet)
- **Reset:** ~30 Sekunden
- **Cron-Intervall:** 4 Minuten (sicherer Puffer)

## Manuelle Prüfung

```bash
# Log ansehen
tail -f /root/.openclaw/workspace/logs/skill_install.log

# Cron-Status
crontab -l

# Warteschlange ansehen
cat /root/.openclaw/workspace/config/pending_skills.txt

# Installierte Skills prüfen
ls -la /root/.openclaw/workspace/skills/
```

---

*Automatisches Deployment aktiv seit: 2026-03-29*
*Letzte Aktualisierung: Korrekte Slugs identifiziert*
