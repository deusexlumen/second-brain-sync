Write-Host "=== Zündung: Kimi Brain Server ===" -ForegroundColor Cyan

# Sandbox aktivieren
& .venv\Scripts\Activate.ps1

# Browser automatisch öffnen (Windows)
Write-Host "Öffne Browser..."
Start-Process "http://127.0.0.1:8000"

# Server starten
Write-Host "Server läuft. Zum Beenden STRG+C drücken." -ForegroundColor Yellow
mkdocs serve
