"""
Docker-Compatible Elliott Wave Trading Bot
Reads configuration from environment variables and files
"""

import os
import sys
from enhanced_elliott_wave_bot import EnhancedElliottWaveTradingBot
from enhanced_bot_config import BotConfig

def main():
    """Main function for Docker deployment"""
    
    print("🐳 ELLIOTT WAVE TRADING BOT - DOCKER VERSION")
    print("=" * 60)
    
    # Get API credentials from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'
    
    if not api_key or not api_secret:
        print("❌ ERROR: BINANCE_API_KEY and BINANCE_API_SECRET must be set!")
        print("   Please check your .env file or environment variables.")
        sys.exit(1)
    
    print(f"✅ API Credentials loaded from environment")
    print(f"🔧 Using Testnet: {use_testnet}")
    
    # Load configuration
    config_file = os.getenv('BOT_CONFIG_FILE', 'bot_config.json')
    
    try:
        # Create and start the bot
        print(f"📊 Loading configuration from: {config_file}")
        
        bot = EnhancedElliottWaveTradingBot(
            api_key=api_key,
            api_secret=api_secret,
            testnet=use_testnet,
            config_file=config_file
        )
        
        print("🚀 Starting Elliott Wave Trading Bot in Docker container...")
        print("💡 Bot will run continuously until stopped")
        print("📊 View logs: docker logs elliott_wave_trading_bot")
        print("⏹️ Stop bot: docker stop elliott_wave_trading_bot")
        
        # Start trading (runs indefinitely)
        bot.start_trading()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()