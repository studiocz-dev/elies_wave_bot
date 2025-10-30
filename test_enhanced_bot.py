"""
Auto-Run Enhanced Elliott Wave Trading Bot
"""

from enhanced_elliott_wave_bot import EnhancedElliottWaveTradingBot
from enhanced_bot_config import BotConfig
import time

def main():
    """Auto-run the enhanced bot for testing"""
    
    print("🚀 AUTO-TESTING ENHANCED ELLIOTT WAVE TRADING BOT")
    print("=" * 60)
    
    # Your actual Binance testnet API credentials
    API_KEY = "jrXGWzslblLrKOa7WUHMCvZFM1gCFWGowJvC8DLLPKcT7mLxbDzuvDqT0KP8KcHY"
    API_SECRET = "PQh6Q6eGjNOhJUeBtUzPq7LEX8Y6kI6N8WKfVWP6Q87UKelgpDr4Wr7aLjBOKWcJ"
    USE_TESTNET = True
    
    print("📊 ENHANCED CONFIGURATION LOADED")
    print("-" * 40)
    
    # Create and display the configuration
    config = BotConfig("enhanced_bot_config.json")
    
    print(f"✅ Symbols: {len(config.get('symbols'))} (expanded from 4 to 10)")
    print(f"✅ Timeframes: {len(config.get('intervals'))} (expanded from 2 to 4)")
    print(f"✅ Min Confidence: {config.get('min_confidence')*100}% (reduced from 60%)")
    print(f"✅ Min Risk/Reward: {config.get('min_risk_reward')}:1 (reduced from 1.5:1)")
    print(f"✅ Market Coverage: {len(config.get('symbols')) * len(config.get('intervals'))} combinations")
    
    print("\n🚀 STARTING ENHANCED BOT (Test Run - 2 minutes)")
    print("-" * 50)
    
    try:
        # Create the enhanced bot
        bot = EnhancedElliottWaveTradingBot(
            api_key=API_KEY,
            api_secret=API_SECRET,
            testnet=USE_TESTNET,
            config_file="enhanced_bot_config.json"
        )
        
        # Run for 2 minutes for testing
        print("⏰ Running for 2 minutes to test enhanced configuration...")
        
        start_time = time.time()
        bot.bot_running = True
        
        while time.time() - start_time < 120:  # 2 minutes
            # Single scan cycle
            bot.scan_and_trade()
            bot.manage_positions()
            bot.log_enhanced_status()
            
            # Wait for next scan
            time.sleep(bot.config['scan_frequency'])
            
            if not bot.bot_running:
                break
        
        print("\n✅ TEST COMPLETED SUCCESSFULLY!")
        bot.shutdown()
        
        # Summary
        print(f"\n📊 ENHANCED BOT TEST SUMMARY")
        print(f"   • Total symbols scanned: {len(config.get('symbols'))}")
        print(f"   • Total timeframes: {len(config.get('intervals'))}")
        print(f"   • Market combinations: {len(config.get('symbols')) * len(config.get('intervals'))}")
        print(f"   • Expected signal increase: ~50% more opportunities")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()