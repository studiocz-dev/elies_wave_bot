"""
Test script to verify Unicode logging fixes
"""

from elliott_wave_trading_bot import ElliottWaveTradingBot
import json

def test_logging():
    """Test the Unicode logging functionality"""
    
    # Load API config
    try:
        with open('api_config.json', 'r') as f:
            api_config = json.load(f)
    except FileNotFoundError:
        print("API config not found, using default testnet settings")
        api_config = {
            'api_key': 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO',
            'api_secret': 'YZjsNhQpjsxGZVq5q2VKbvzEdOCGzCCH9gFbP9n2m3hkNP6LqNlWNvuBN1JN9Qf3'
        }
    
    print("Testing Elliott Wave Trading Bot Unicode logging...")
    
    # Initialize bot (this will test the logging setup)
    bot = ElliottWaveTradingBot(
        api_key=api_config['api_key'],
        api_secret=api_config['api_secret'],
        testnet=True
    )
    
    # Test various logging messages with emojis
    print("\nTesting safe logging with emojis:")
    bot.safe_log("info", "Testing Unicode emoji support", "🧪")
    bot.safe_log("info", "Testing financial emojis", "💰")
    bot.safe_log("info", "Testing chart emojis", "📊")
    bot.safe_log("info", "Testing trading emojis", "📈")
    bot.safe_log("warning", "Testing warning with emoji", "⚠️")
    bot.safe_log("info", "Testing search emoji", "🔍")
    
    print("\nLogging test completed successfully!")
    print("Check elliott_wave_bot.log file for UTF-8 encoded output")

if __name__ == "__main__":
    test_logging()