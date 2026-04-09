# Second Brain - Sync & Build Skript
# Dieses Skript synchronisiert das Repository und baut das Wiki

Write-Host "=== Second Brain Sync & Build ===" -ForegroundColor Cyan

# 1. Git Pull
git pull origin main

# 2. Virtuelles Environment aktivieren
& .venv\Scripts\Activate.ps1

# 3. MkDocs Build ausführen
mkdocs build

# 4. Virtuelles Environment deaktivieren
deactivate

# 5. Git Add All
git add .

# 6. Git Commit
git commit -m "Auto-Sync & Build"

# 7. Git Push
git push origin main

Write-Host "=== Sync & Build abgeschlossen ===" -ForegroundColor Green
