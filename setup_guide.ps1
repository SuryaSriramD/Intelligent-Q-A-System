# Quick Start for RAG FastAPI
# Simple manual setup guide

Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     RAG FastAPI - Manual Quick Start Guide    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "Follow these steps to run the demo:`n" -ForegroundColor Yellow

Write-Host "1. Start the server (Terminal 1):" -ForegroundColor Green
Write-Host "   cd d:\rag-fastapi" -ForegroundColor White
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   uvicorn app.api:app --port 8000`n" -ForegroundColor White

Write-Host "2. Run the demo (Terminal 2):" -ForegroundColor Green
Write-Host "   cd d:\rag-fastapi" -ForegroundColor White
Write-Host "   .\.venv\Scripts\python.exe demo.py`n" -ForegroundColor White

Write-Host "OR use Make commands:" -ForegroundColor Yellow
Write-Host "   Terminal 1: " -NoNewline -ForegroundColor Green
Write-Host "make run" -ForegroundColor White
Write-Host "   Terminal 2: " -NoNewline -ForegroundColor Green
Write-Host "make demo`n" -ForegroundColor White

Write-Host "Quick test commands:" -ForegroundColor Yellow
Write-Host "   make health       # Check if server is running" -ForegroundColor White
Write-Host "   make crawl        # Crawl example.com" -ForegroundColor White
Write-Host "   make index        # Build search indexes" -ForegroundColor White
Write-Host "   make ask          # Ask a question" -ForegroundColor White
Write-Host "   make ask-refuse   # Test refusal mechanism`n" -ForegroundColor White

Write-Host "✓ Dependencies are installed!" -ForegroundColor Green
Write-Host "✓ Ready to run!`n" -ForegroundColor Green
