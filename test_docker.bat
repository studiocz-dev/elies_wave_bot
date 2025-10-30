@echo off
REM Test Docker deployment locally on Windows

echo 🧪 Testing Elliott Wave Trading Bot Docker Setup
echo ===============================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is installed

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️ Please edit .env file with your API credentials before continuing
    echo    Then run this script again
    pause
    exit /b 1
)

echo ✅ Environment file found

REM Check if configuration exists
if not exist bot_config.json (
    echo 📊 Creating bot configuration...
    python enhanced_bot_config.py
)

echo ✅ Bot configuration ready

REM Build the Docker image
echo 🔨 Building Docker image...
docker-compose build

if %errorlevel% neq 0 (
    echo ❌ Failed to build Docker image
    pause
    exit /b 1
)

echo ✅ Docker image built successfully

REM Test the container
echo 🧪 Testing container startup...
docker-compose up -d

REM Wait a moment for startup
timeout /t 5 >nul

REM Check if container is running
docker ps --filter name=elliott_wave_trading_bot --quiet | findstr . >nul
if %errorlevel% equ 0 (
    echo ✅ Container is running successfully
    
    echo 📋 Showing recent logs...
    docker-compose logs --tail=20 elliott-wave-bot
    
    echo.
    echo 🎉 Docker setup test completed successfully!
    echo.
    echo 📊 Container Status:
    docker ps --filter name=elliott_wave_trading_bot --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo.
    echo 💡 Next steps:
    echo    1. View full logs: docker-compose logs -f elliott-wave-bot
    echo    2. Stop bot: docker-compose down
    echo    3. Deploy to cloud: Follow DOCKER_DEPLOYMENT.md
    
) else (
    echo ❌ Container failed to start
    echo 📋 Checking logs...
    docker-compose logs elliott-wave-bot
    docker-compose down
    pause
    exit /b 1
)

pause