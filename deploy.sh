#!/bin/bash
# Deploy Elliott Wave Trading Bot to Free Cloud Platforms

echo "🚀 Elliott Wave Trading Bot - Cloud Deployment Script"
echo "====================================================="

# Function to deploy to Railway (Recommended - Easy & Free)
deploy_railway() {
    echo "🚂 Deploying to Railway.app (Free Tier)"
    echo "1. Install Railway CLI: npm install -g @railway/cli"
    echo "2. Login: railway login"
    echo "3. Initialize: railway init"
    echo "4. Deploy: railway up"
    echo ""
    echo "Railway offers 500 hours/month free - perfect for trading bots!"
}

# Function to deploy to Render (Good alternative)
deploy_render() {
    echo "🎨 Deploying to Render.com (Free Tier)"
    echo "1. Push code to GitHub"
    echo "2. Connect Render to your GitHub repo"
    echo "3. Select 'Web Service' and use Docker"
    echo "4. Set environment variables in Render dashboard"
    echo ""
    echo "Render offers 750 hours/month free!"
}

# Function to deploy to Fly.io
deploy_fly() {
    echo "🪰 Deploying to Fly.io (Free Tier)"
    echo "1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/"
    echo "2. Login: flyctl auth login"
    echo "3. Launch: flyctl launch"
    echo "4. Deploy: flyctl deploy"
    echo ""
    echo "Fly.io offers 3 shared-cpu VMs free!"
}

# Function to deploy to Heroku (Container Registry)
deploy_heroku() {
    echo "🟪 Deploying to Heroku (Free tier discontinued but Container Registry available)"
    echo "1. Install Heroku CLI"
    echo "2. Login: heroku login"
    echo "3. Create app: heroku create your-bot-name"
    echo "4. Build and push: heroku container:push web"
    echo "5. Release: heroku container:release web"
    echo ""
    echo "Note: Heroku free tier ended, but paid tiers start at $5/month"
}

echo "Choose deployment platform:"
echo "1) Railway.app (Recommended - 500 hours free)"
echo "2) Render.com (750 hours free)"
echo "3) Fly.io (3 VMs free)"
echo "4) Heroku (Paid but reliable)"
echo "5) Local Docker (Development)"

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        deploy_railway
        ;;
    2)
        deploy_render
        ;;
    3)
        deploy_fly
        ;;
    4)
        deploy_heroku
        ;;
    5)
        echo "🐳 Running locally with Docker"
        echo "Run: docker-compose up -d"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
echo "📋 Pre-deployment checklist:"
echo "✓ Set your .env file with API credentials"
echo "✓ Configure bot_config.json with your trading parameters"
echo "✓ Test locally first: docker-compose up"
echo "✓ Monitor logs: docker logs elliott_wave_trading_bot"