Write-Host '=== Second Brain Sync & Build ===' -ForegroundColor Cyan

# 1. Git Pull mit Fehlerprüfung
Write-Host 'Führe git pull aus...'
git pull origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host 'CRITICAL ERROR: Git Pull fehlgeschlagen (Möglicher Merge Conflict). Skript abgebrochen!' -ForegroundColor Red
    exit 1
}

# 2. MkDocs Build (Sandboxed)
Write-Host 'Baue Wiki...'
& .venv\Scripts\Activate.ps1
mkdocs build
deactivate

# 3. Git Push
Write-Host 'Pushe Änderungen...'
git add .
git commit -m 'Auto-Sync & Build'
git push origin main
Write-Host '=== Sync & Build erfolgreich ===' -ForegroundColor Green
