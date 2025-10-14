#!/bin/bash
# Production Start Script (Linux/Mac)
# Starts the RAG API with the web UI

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           RAG API - INTELLIGENT Q&A SYSTEM                       ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

echo "Starting production server..."
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Web UI: http://localhost:8000"
echo "  • Health: http://localhost:8000/health"
echo ""

echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.api:app --host 0.0.0.0 --port 8000
