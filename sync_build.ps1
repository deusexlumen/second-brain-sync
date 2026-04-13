$ErrorActionPreference = 'Stop'

try {
    Write-Host '=== Second Brain Sync & Build ===' -ForegroundColor Cyan

    # 1. Git Pull mit Fehlerprüfung
    Write-Host 'Führe git pull aus...' -ForegroundColor Yellow
    git pull origin main
    if ($LASTEXITCODE -ne 0) {
        throw 'Git Pull fehlgeschlagen (Möglicher Merge Conflict).'
    }
    Write-Host 'Git Pull erfolgreich.' -ForegroundColor Green

    # 2. Voraussetzungen prüfen (nach VEnv-Aktivierung)
    Write-Host 'Aktiviere Virtual Environment (.venv)...' -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
    Write-Host 'Virtual Environment aktiviert.' -ForegroundColor Green

    Write-Host 'Prüfe Voraussetzungen...' -ForegroundColor Yellow
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error "Python wurde nicht gefunden. Bitte installiere Python und führe 'pip install -r requirements.txt' aus."
        exit 1
    }
    if (-not (Get-Command mkdocs -ErrorAction SilentlyContinue)) {
        Write-Error "MkDocs wurde nicht gefunden. Bitte führe 'pip install -r requirements.txt' aus."
        exit 1
    }
    Write-Host 'Voraussetzungen erfüllt.' -ForegroundColor Green

    Write-Host 'Baue Wiki mit MkDocs...' -ForegroundColor Yellow
    mkdocs build --strict
    if ($LASTEXITCODE -ne 0) {
        throw 'MkDocs Build fehlgeschlagen.'
    }
    Write-Host 'MkDocs Build erfolgreich.' -ForegroundColor Green

    Write-Host 'Deaktiviere Virtual Environment...' -ForegroundColor Yellow
    deactivate

    # 4. Git Push
    Write-Host 'Pushe Änderungen...' -ForegroundColor Yellow
    git add .
    git commit -m 'Auto-Sync & Build'
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        throw 'Git Push fehlgeschlagen.'
    }

    Write-Host '=== Sync & Build erfolgreich ===' -ForegroundColor Green
}
catch {
    Write-Host "CRITICAL ERROR: $($_.Exception.Message) Skript abgebrochen!" -ForegroundColor Red
    exit 1
}
