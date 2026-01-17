#!/bin/bash

# Deployment script for WhisperHedge UI

set -e

echo "🚀 Deploying WhisperHedge UI..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found. Please create it from the template."
    exit 1
fi

# Load environment variables
set -a
source .env.production
set +a

# Validate required variables
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ] || [ -z "$ENCRYPTION_KEY" ]; then
    echo "❌ Missing required environment variables. Please check .env.production"
    exit 1
fi

# Build and run with Docker Compose
echo "📦 Building Docker image..."
docker-compose build

echo "🔄 Starting services..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 App is running at: http://localhost:8000"
echo "📊 Check logs with: docker-compose logs -f web"
echo "🛑 Stop with: docker-compose down"
