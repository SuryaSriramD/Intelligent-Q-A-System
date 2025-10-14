# Production Start Script - RAG API
# Starts the server with web UI on http://localhost:8000

Write-Host "Starting RAG API..." -ForegroundColor Cyan
Write-Host "Web UI: http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""

# Start the server
.\.venv\Scripts\uvicorn.exe app.api:app --host 0.0.0.0 --port 8000
