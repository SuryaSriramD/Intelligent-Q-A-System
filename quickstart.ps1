#!/usr/bin/env pwsh
# Quick start script for Windows PowerShell
# Runs the complete demo flow

Write-Host "`n=== RAG FastAPI Quick Start ===" -ForegroundColor Cyan
Write-Host "This will start the server and run the demo`n" -ForegroundColor Gray

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
    
    # Check if dependencies are installed
    $uvicornCheck = & .\.venv\Scripts\python.exe -c "import uvicorn" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Dependencies not installed. Installing..." -ForegroundColor Yellow
        .\.venv\Scripts\pip.exe install -r requirements.txt
    }
}

# Start server in background
Write-Host "`nStarting server..." -ForegroundColor Yellow
$server = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "app.api:app", "--port", "8000" -PassThru -NoNewWindow

Start-Sleep -Seconds 4

# Wait for server to be ready
Write-Host "Waiting for server to be ready..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}

if ($ready) {
    Write-Host "✓ Server is ready!`n" -ForegroundColor Green
    
    # Run demo
    Write-Host "Running demo...`n" -ForegroundColor Cyan
    .\.venv\Scripts\python.exe demo.py
    
    Write-Host "`n`nPress any key to stop the server..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Stop server
    Write-Host "Stopping server..." -ForegroundColor Yellow
    Stop-Process -Id $server.Id -Force
    Write-Host "✓ Server stopped" -ForegroundColor Green
} else {
    Write-Host "✗ Server failed to start!" -ForegroundColor Red
    Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
}

Write-Host "`nDone!`n" -ForegroundColor Cyan
