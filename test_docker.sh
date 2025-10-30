#!/bin/bash
# Test Docker deployment locally before cloud deployment

echo "🧪 Testing Elliott Wave Trading Bot Docker Setup"
echo "==============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️ docker-compose not found, using 'docker compose' instead"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️ Please edit .env file with your API credentials before continuing"
    echo "   Then run this script again"
    exit 1
fi

echo "✅ Environment file found"

# Check if configuration exists
if [ ! -f bot_config.json ]; then
    echo "📊 Creating bot configuration..."
    python enhanced_bot_config.py
fi

echo "✅ Bot configuration ready"

# Build the Docker image
echo "🔨 Building Docker image..."
$COMPOSE_CMD build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Test the container
echo "🧪 Testing container startup..."
$COMPOSE_CMD up -d

# Wait a moment for startup
sleep 5

# Check if container is running
if docker ps | grep -q elliott_wave_trading_bot; then
    echo "✅ Container is running successfully"
    
    # Show logs for 10 seconds
    echo "📋 Showing logs (first 10 seconds)..."
    timeout 10 $COMPOSE_CMD logs -f elliott-wave-bot
    
    echo ""
    echo "🎉 Docker setup test completed successfully!"
    echo ""
    echo "📊 Container Status:"
    docker ps --filter name=elliott_wave_trading_bot --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    echo "💡 Next steps:"
    echo "   1. View full logs: $COMPOSE_CMD logs -f elliott-wave-bot"
    echo "   2. Stop bot: $COMPOSE_CMD down"
    echo "   3. Deploy to cloud: Follow DOCKER_DEPLOYMENT.md"
    
else
    echo "❌ Container failed to start"
    echo "📋 Checking logs..."
    $COMPOSE_CMD logs elliott-wave-bot
    $COMPOSE_CMD down
    exit 1
fi