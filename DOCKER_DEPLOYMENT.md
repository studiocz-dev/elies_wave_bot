# 🐳 Elliott Wave Trading Bot - Docker Deployment Guide

## Overview
Run your Elliott Wave trading bot 24/7 in the cloud using Docker, even when your computer is off!

## 🎯 Deployment Options (FREE TIERS AVAILABLE)

### 1. 🚂 Railway.app (RECOMMENDED)
**FREE: 500 hours/month + $5 credit**
- ✅ Easiest setup
- ✅ Auto-deploys from GitHub
- ✅ Built-in monitoring
- ✅ Perfect for trading bots

### 2. 🎨 Render.com  
**FREE: 750 hours/month**
- ✅ Good Docker support
- ✅ GitHub integration
- ✅ Auto-sleep (spins down when idle)

### 3. 🪰 Fly.io
**FREE: 3 shared-cpu VMs**
- ✅ Global edge deployment
- ✅ Good performance
- ✅ CLI-based deployment

### 4. 🟪 Heroku (Container Registry)
**PAID: Starts at $5/month**
- ✅ Most reliable
- ✅ Great for production
- ❌ No free tier anymore

---

## 🚀 Quick Start (Local Docker)

### Step 1: Setup Environment
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your API credentials
# BINANCE_API_KEY=your_key_here
# BINANCE_API_SECRET=your_secret_here
# USE_TESTNET=true
```

### Step 2: Build and Run
```bash
# Build the Docker image
docker-compose build

# Start the bot (runs in background)
docker-compose up -d

# View logs
docker-compose logs -f elliott-wave-bot

# Stop the bot
docker-compose down
```

---

## 🌍 Cloud Deployment (24/7 Operation)

### Option A: Railway.app (Easiest)

1. **Prepare your code:**
   ```bash
   # Push to GitHub
   git add .
   git commit -m "Add Docker deployment"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Visit [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Dockerfile!

3. **Set Environment Variables:**
   - Go to your project dashboard
   - Click "Variables" tab
   - Add:
     - `BINANCE_API_KEY` = your API key
     - `BINANCE_API_SECRET` = your API secret
     - `USE_TESTNET` = true

4. **Deploy:**
   - Railway automatically builds and deploys
   - Bot runs 24/7 until you stop it
   - Free tier: 500 hours/month

### Option B: Render.com

1. **Connect GitHub:**
   - Visit [render.com](https://render.com)
   - Connect your GitHub repository

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Select your repo
   - Choose "Docker" as runtime

3. **Configure:**
   - Set start command: `python docker_bot.py`
   - Add environment variables (same as Railway)

4. **Deploy:**
   - Click "Create Web Service"
   - Free tier: 750 hours/month

### Option C: Fly.io (Advanced)

1. **Install CLI:**
   ```bash
   # Install flyctl
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy:**
   ```bash
   # Login
   flyctl auth login
   
   # Launch app
   flyctl launch
   
   # Set secrets
   flyctl secrets set BINANCE_API_KEY=your_key
   flyctl secrets set BINANCE_API_SECRET=your_secret
   flyctl secrets set USE_TESTNET=true
   
   # Deploy
   flyctl deploy
   ```

---

## 📊 Monitoring Your Bot

### View Logs:
```bash
# Local Docker
docker-compose logs -f elliott-wave-bot

# Railway
# Use Railway dashboard logs tab

# Fly.io
flyctl logs

# Render
# Use Render dashboard logs tab
```

### Check Bot Status:
```bash
# Local Docker
docker-compose ps

# Check if container is healthy
docker inspect elliott_wave_trading_bot | grep -A5 Health
```

---

## 🔧 Configuration Management

### Update Trading Parameters:
1. Edit `bot_config.json`
2. Restart container:
   ```bash
   # Local
   docker-compose restart
   
   # Cloud platforms auto-restart on file changes
   ```

### Switch to Live Trading:
1. Change `.env`:
   ```bash
   USE_TESTNET=false
   ```
2. Use real API credentials (not testnet)
3. Restart container

---

## 💡 Pro Tips

### 1. **Resource Optimization:**
- Bot uses ~100MB RAM
- Minimal CPU usage
- Perfect for free tiers

### 2. **Monitoring:**
- Check logs daily for trading activity
- Set up alerts for errors
- Monitor account balance

### 3. **Security:**
- Never commit API keys to GitHub
- Use environment variables only
- Enable IP whitelist on Binance API

### 4. **Backup:**
- Export trading logs regularly
- Keep configuration files backed up
- Save successful trading parameters

---

## 🆘 Troubleshooting

### Bot Won't Start:
1. Check API credentials in environment variables
2. Verify internet connection
3. Check Binance API status

### No Trading Signals:
1. Market conditions might not meet criteria
2. Try lowering confidence threshold
3. Check if patterns are being detected

### Container Crashes:
1. Check logs for specific errors
2. Verify all dependencies in requirements.txt
3. Test locally first

---

## 📋 Deployment Checklist

- [ ] ✅ Code tested locally
- [ ] ✅ API credentials set in .env
- [ ] ✅ bot_config.json configured
- [ ] ✅ Docker container builds successfully
- [ ] ✅ Local testing completed
- [ ] ✅ GitHub repository updated
- [ ] ✅ Cloud platform chosen
- [ ] ✅ Environment variables set on cloud
- [ ] ✅ Bot deployed and running
- [ ] ✅ Logs monitoring setup
- [ ] ✅ Alert system configured

---

## 🏆 Recommended Setup

**For Maximum Uptime:**
1. **Primary**: Railway.app (500 hours free)
2. **Backup**: Render.com (750 hours free)
3. **Monitoring**: Both platforms have built-in monitoring

This gives you 1,250+ hours/month coverage (more than 24/7)!

---

## 💸 Cost Analysis

| Platform | Free Tier | Monthly Cost | Uptime |
|----------|-----------|--------------|--------|
| Railway | 500 hours | $0 | 69% |
| Render | 750 hours | $0 | 100%+ |
| Fly.io | 3 VMs | $0 | 100%+ |
| Heroku | None | $5+ | 100% |

**Best Strategy**: Use Render.com for 24/7 free operation!

Your Elliott Wave trading bot will now run continuously in the cloud! 🚀