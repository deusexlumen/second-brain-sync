Kimi, Direktive für die Zukunft: Wenn ich dich bitte, Daten zu verarbeiten, liest du alle Dateien in /RAW. Du übersetzt sie in strukturiertes Markdown, erstellst logische [[Backlinks]] zu bestehenden Konzepten und speicherst sie in /Wiki. Lösche danach die Rohdaten aus /RAW und logge die Aktion in /Log/history.md.

WICHTIGE REGEL FÜR /WIKI: Jede Markdown-Datei, die du im Wiki erstellst, MUSS zwingend ganz oben einen YAML-Frontmatter-Block haben, der so aussieht:
---
title: [Titel der Notiz]
date: [YYYY-MM-DD]
tags: [tag1, tag2, tag3]
---
Setze danach den Text. Nutze Admonitions (z.B. !!! info "Tipp") für wichtige Erkenntnisse.

WICHTIGE REGEL FÜR MEDIEN: Wenn in /RAW Bilder, PDFs oder andere Dateianhänge liegen, verschiebe diese IMMER in den Ordner /Assets. Referenziere sie im Wiki-Markdown über relative Pfade (z.B. `![Bildbeschreibung](../Assets/bildname.jpg)`).
