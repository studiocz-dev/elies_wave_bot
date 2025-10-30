"""
Direct Elliott Wave Bot Runner
=============================

Runs the Elliott Wave Trading Bot directly in continuous mode
"""

import json
from elliott_wave_trading_bot import ElliottWaveTradingBot

def load_api_config():
    """Load API configuration"""
    try:
        with open('api_config.json', 'r') as f:
            config = json.load(f)
            return {
                'api_key': config.get('binance_api_key', 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO'),
                'api_secret': config.get('binance_api_secret', 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu')
            }
    except:
        return {
            'api_key': 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO',
            'api_secret': 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu'
        }

def run_bot():
    """Run the Elliott Wave Trading Bot"""
    
    print("🚀 STARTING ELLIOTT WAVE TRADING BOT")
    print("=" * 50)
    
    # Load API configuration
    api_config = load_api_config()
    
    # Bot configuration
    bot_config = {
        'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT'],
        'intervals': ['1h', '4h'],
        'scan_frequency': 60,  # Scan every 1 minute for demo
        'max_positions': 3,
        'risk_per_trade': 0.02,  # 2% risk per trade
        'min_confidence': 0.6,   # 60% confidence threshold
        'min_risk_reward': 1.5,  # 1.5:1 risk/reward ratio
        'account_balance': 100000  # $100k testnet balance
    }
    
    print(f"📊 Configuration:")
    print(f"   Symbols: {', '.join(bot_config['symbols'])}")
    print(f"   Timeframes: {', '.join(bot_config['intervals'])}")
    print(f"   Scan frequency: {bot_config['scan_frequency']} seconds")
    print(f"   Risk per trade: {bot_config['risk_per_trade']*100}%")
    print(f"   Min confidence: {bot_config['min_confidence']*100}%")
    print(f"   Account balance: ${bot_config['account_balance']:,}")
    print()
    
    # Initialize bot
    bot = ElliottWaveTradingBot(
        api_key=api_config['api_key'],
        api_secret=api_config['api_secret'],
        testnet=True,
        config=bot_config
    )
    
    print("✅ Bot initialized and ready to trade!")
    print("📡 Connected to Binance Testnet (paper trading)")
    print("🔍 Starting continuous market scanning...")
    print("⚠️  Press Ctrl+C to stop the bot")
    print("=" * 50)
    
    try:
        # Start the trading bot
        bot.start_trading()
        
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
        print("📊 Final Status:")
        print(f"   Active Positions: {len(bot.active_positions)}")
        print(f"   Total Trades: {len(bot.trade_history)}")
        print("✅ Bot shut down safely")
        
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
        print("🔧 Check configuration and restart")

if __name__ == "__main__":
    run_bot()