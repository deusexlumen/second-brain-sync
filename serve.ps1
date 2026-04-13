$ErrorActionPreference = 'Stop'

try {
    Write-Host "=== Zündung: Kimi Brain Server ===" -ForegroundColor Cyan

    # 1. Voraussetzungen prüfen
    Write-Host "Prüfe Voraussetzungen..." -ForegroundColor Yellow
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error "Python wurde nicht gefunden. Bitte installiere Python und führe 'pip install -r requirements.txt' aus."
        exit 1
    }
    if (-not (Get-Command mkdocs -ErrorAction SilentlyContinue)) {
        Write-Error "MkDocs wurde nicht gefunden. Bitte führe 'pip install -r requirements.txt' aus."
        exit 1
    }
    Write-Host "Voraussetzungen erfüllt." -ForegroundColor Green

    # 2. Virtual Environment aktivieren
    Write-Host "Aktiviere Virtual Environment (.venv)..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
    Write-Host "Virtual Environment aktiviert." -ForegroundColor Green

    # 3. Browser automatisch öffnen (Windows)
    Write-Host "Öffne Browser unter http://127.0.0.1:8000 ..." -ForegroundColor Yellow
    Start-Process "http://127.0.0.1:8000"

    # 4. Server starten
    Write-Host "Starte MkDocs Server..." -ForegroundColor Yellow
    Write-Host "Server läuft. Zum Beenden STRG+C drücken." -ForegroundColor Green
    mkdocs serve
}
catch {
    Write-Host "CRITICAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
