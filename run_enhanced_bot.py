"""
Run Enhanced Elliott Wave Trading Bot with Real API Credentials
"""

from enhanced_elliott_wave_bot import EnhancedElliottWaveTradingBot
from enhanced_bot_config import BotConfig

def main():
    """Run the enhanced bot with real API credentials"""
    
    print("🚀 ENHANCED ELLIOTT WAVE TRADING BOT")
    print("=" * 50)
    
    # Your actual Binance testnet API credentials
    API_KEY = "jrXGWzslblLrKOa7WUHMCvZFM1gCFWGowJvC8DLLPKcT7mLxbDzuvDqT0KP8KcHY"
    API_SECRET = "PQh6Q6eGjNOhJUeBtUzPq7LEX8Y6kI6N8WKfVWP6Q87UKelgpDr4Wr7aLjBOKWcJ"
    USE_TESTNET = True
    
    print("📊 CONFIGURATION SETUP")
    print("-" * 30)
    
    # First, create and display the configuration
    config = BotConfig("enhanced_bot_config.json")
    
    print("\n💡 ENHANCEMENT SUMMARY:")
    print(f"   • Symbols: {len(config.get('symbols'))} (was 4, now 10)")
    print(f"   • Timeframes: {len(config.get('intervals'))} (was 2, now 4)")
    print(f"   • Min Confidence: {config.get('min_confidence')*100}% (was 60%, now 45%)")
    print(f"   • Min Risk/Reward: {config.get('min_risk_reward')}:1 (was 1.5:1, now 1.2:1)")
    print(f"   • Scan Frequency: {config.get('scan_frequency')} seconds")
    
    print(f"\n📈 EXPECTED IMPROVEMENTS:")
    print(f"   • Market coverage: {10*4} combinations (was {4*2})")
    print(f"   • Signal sensitivity: ~50% more signals expected")
    print(f"   • Faster timeframes: 15m/30m for quicker entries")
    
    input("\n▶️ Press Enter to start the enhanced bot...")
    
    # Create and start the enhanced bot
    bot = EnhancedElliottWaveTradingBot(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=USE_TESTNET,
        config_file="enhanced_bot_config.json"
    )
    
    # Start trading
    try:
        bot.start_trading()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")


if __name__ == "__main__":
    main()