#!/bin/bash

echo "🚀 Starting Portfolio Application Setup..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv sync

# Install NPM packages
echo "📦 Installing NPM packages..."
npm install

# Build Next.js frontend
echo "🔨 Building Next.js frontend..."
npm run build

# Initialize database
echo "🗄️  Initializing database..."
uv run python backend/init_db.py

# Run database migrations
echo "🔄 Running database migrations..."
cd backend && uv run flask db upgrade && cd ..

# Start Flask backend
echo "✅ Starting Flask backend on port 5000..."
PORT=5000 uv run python backend/app.py
