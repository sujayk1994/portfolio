#!/bin/bash

echo "🚀 Starting Portfolio Application..."

# Start Flask backend
echo "✅ Starting Flask backend on port 5000..."
cd backend && PORT=5000 uv run python app.py
