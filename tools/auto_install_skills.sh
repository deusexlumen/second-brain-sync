#!/bin/bash
# Skill-Auto-Installer via clawhub
# Truthseeker v6.4 - Autonomous Deployment

LOG_FILE="/root/.openclaw/workspace/logs/skill_install.log"
LOCK_FILE="/tmp/clawhub_install.lock"
SKILL_LIST="/root/.openclaw/workspace/config/pending_skills.txt"
SKILLS_DIR="/root/.openclaw/workspace/skills"

# Erstelle Verzeichnisse
mkdir -p /root/.openclaw/workspace/logs
mkdir -p "$SKILLS_DIR"

# Prüfe ob Lock existiert
if [ -f "$LOCK_FILE" ]; then
    echo "$(date): Installation läuft bereits..." >> "$LOG_FILE"
    exit 0
fi

# Setze Lock
touch "$LOCK_FILE"

echo "$(date): Starte Skill-Installation..." >> "$LOG_FILE"
echo "$(date): Working Dir: $(pwd)" >> "$LOG_FILE"

# Wechsle in Workspace
cd /root/.openclaw/workspace || exit 1

# Lese Skills und installiere
while IFS= read -r skill; do
    # Skip Kommentare und Leerzeilen
    [ -z "$skill" ] && continue
    [[ "$skill" =~ ^# ]] && continue
    
    echo "$(date): Versuche '$skill'..." >> "$LOG_FILE"
    
    # Installiere mit clawhub (ohne owner/ prefix!)
    if npx clawhub install "$skill" --dir "$SKILLS_DIR" 2>> "$LOG_FILE"; then
        echo "$(date): ✅ '$skill' installiert" >> "$LOG_FILE"
        # Entferne aus pending list
        sed -i "/^$skill$/d" "$SKILL_LIST"
    else
        ERROR_MSG=$(tail -5 "$LOG_FILE" | grep -i "rate limit\|error" | head -1)
        echo "$(date): ❌ '$skill' fehlgeschlagen: $ERROR_MSG" >> "$LOG_FILE"
        
        # Rate Limit erkannt? Dann abbrechen
        if echo "$ERROR_MSG" | grep -qi "rate limit"; then
            echo "$(date): ⏳ Rate Limit erkannt, warte auf nächsten Versuch..." >> "$LOG_FILE"
            break
        fi
    fi
    
    # Kurze Pause zwischen Installationen
    sleep 2
done < "$SKILL_LIST"

# Entferne Lock
rm -f "$LOCK_FILE"

echo "$(date): Installation beendet." >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
