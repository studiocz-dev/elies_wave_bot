"""
🔑 BINANCE API SETUP GUIDE - Multiple Methods
===========================================

This file shows you EXACTLY where and how to set your Binance API credentials
for the Elliott Wave Trading Bot.
"""

# ================================================================================
# METHOD 1: ENVIRONMENT VARIABLES (RECOMMENDED FOR SECURITY)
# ================================================================================

import os
from elliott_wave_trading_bot import ElliottWaveTradingBot

def setup_with_environment_variables():
    """
    Most secure method - stores API keys as environment variables
    
    Steps:
    1. Set environment variables in Windows:
       - Press Win+R, type 'sysdm.cpl', press Enter
       - Go to Advanced tab → Environment Variables
       - Add new User variables:
         * Variable name: BINANCE_API_KEY
         * Variable value: your_actual_api_key
         * Variable name: BINANCE_API_SECRET  
         * Variable value: your_actual_api_secret
    
    2. Or set them in PowerShell for current session:
       $env:BINANCE_API_KEY="your_api_key_here"
       $env:BINANCE_API_SECRET="your_api_secret_here"
    """
    
    # Get API credentials from environment variables
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ ERROR: Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        return None
    
    # Trading configuration
    config = {
        'symbols': ['BTCUSDT', 'ETHUSDT'],
        'intervals': ['4h'],
        'risk_per_trade': 0.01,  # 1% risk per trade
        'min_confidence': 0.7,   # 70% minimum confidence
    }
    
    # Initialize bot
    bot = ElliottWaveTradingBot(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,  # Set to False for live trading
        config=config
    )
    
    print("✅ Bot initialized with environment variables")
    return bot


# ================================================================================
# METHOD 2: CONFIG FILE (GOOD FOR DEVELOPMENT)
# ================================================================================

import json

def setup_with_config_file():
    """
    Use a separate config file to store API credentials
    
    Create a file called 'api_config.json' with:
    {
        "binance_api_key": "your_actual_api_key",
        "binance_api_secret": "your_actual_api_secret",
        "testnet": true
    }
    
    IMPORTANT: Add 'api_config.json' to your .gitignore file!
    """
    
    try:
        # Load API credentials from config file
        with open('api_config.json', 'r') as f:
            api_config = json.load(f)
        
        api_key = api_config['binance_api_key']
        api_secret = api_config['binance_api_secret']
        testnet = api_config.get('testnet', True)
        
        # Trading configuration
        config = {
            'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT'],
            'intervals': ['1h', '4h'],
            'risk_per_trade': 0.02,  # 2% risk per trade
        }
        
        # Initialize bot
        bot = ElliottWaveTradingBot(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
            config=config
        )
        
        print("✅ Bot initialized from config file")
        return bot
        
    except FileNotFoundError:
        print("❌ ERROR: api_config.json file not found")
        print("Create api_config.json with your API credentials")
        return None
    except Exception as e:
        print(f"❌ ERROR loading config: {e}")
        return None


# ================================================================================
# METHOD 3: DIRECT IN CODE (SIMPLE BUT LESS SECURE)
# ================================================================================

def setup_with_direct_credentials():
    """
    Directly set API credentials in code
    
    ⚠️ WARNING: Don't commit this to version control!
    ⚠️ Replace the placeholder values with your actual API credentials
    """
    
    # 🔑 SET YOUR API CREDENTIALS HERE:
    api_key = "your_binance_api_key_here"        # Replace with actual key
    api_secret = "your_binance_api_secret_here"  # Replace with actual secret
    
    # Validate credentials are set
    if api_key == "your_binance_api_key_here" or api_secret == "your_binance_api_secret_here":
        print("❌ ERROR: Please replace placeholder API credentials with your actual keys")
        return None
    
    # Trading configuration
    config = {
        'symbols': ['BTCUSDT', 'ETHUSDT'],
        'intervals': ['4h'],
        'scan_frequency': 300,   # 5 minutes
        'max_positions': 3,
        'risk_per_trade': 0.01,  # 1% risk per trade
        'min_confidence': 0.6,   # 60% minimum confidence
        'min_risk_reward': 1.5,  # 1.5:1 minimum risk/reward
        'account_balance': 10000,
    }
    
    # Initialize bot
    bot = ElliottWaveTradingBot(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,  # ⚠️ Set to False for LIVE TRADING
        config=config
    )
    
    print("✅ Bot initialized with direct credentials")
    return bot


# ================================================================================
# TESTING YOUR SETUP
# ================================================================================

def test_api_connection(bot):
    """Test if your API credentials work"""
    if bot is None:
        return False
    
    try:
        # Test basic API connection
        current_price = bot.data_fetcher.get_current_price('BTCUSDT')
        
        if current_price:
            print(f"✅ API connection successful!")
            print(f"📊 Current BTC price: ${current_price:,.2f}")
            return True
        else:
            print("❌ API connection failed - unable to get price data")
            return False
            
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False


# ================================================================================
# MAIN DEMO
# ================================================================================

if __name__ == "__main__":
    print("🔑 BINANCE API SETUP GUIDE")
    print("=" * 50)
    
    # Try different setup methods
    print("\n1️⃣ Trying environment variables method...")
    bot = setup_with_environment_variables()
    
    if bot is None:
        print("\n2️⃣ Trying config file method...")
        bot = setup_with_config_file()
    
    if bot is None:
        print("\n3️⃣ Using direct credentials method...")
        bot = setup_with_direct_credentials()
    
    # Test the connection
    if bot:
        print("\n🧪 Testing API connection...")
        if test_api_connection(bot):
            print("\n🚀 Ready to start trading!")
            print("\nNext steps:")
            print("1. Run market scan: bot.scan_and_trade()")
            print("2. Start continuous trading: bot.start_trading()")
        else:
            print("\n❌ API setup needs attention")
    else:
        print("\n❌ Bot initialization failed")
        print("\nPlease set up your API credentials using one of the methods above")


# ================================================================================
# QUICK SETUP TEMPLATE
# ================================================================================

"""
📋 QUICK SETUP CHECKLIST:

□ 1. Get Binance API credentials:
     - Go to binance.com → Account → API Management
     - Create new API key with "Futures Trading" permission
     - Copy API Key and Secret Key

□ 2. Choose setup method:
     
     METHOD 1 (Recommended): Environment Variables
     - Set BINANCE_API_KEY and BINANCE_API_SECRET in Windows
     
     METHOD 2: Config File  
     - Create api_config.json with your credentials
     
     METHOD 3: Direct in Code
     - Replace placeholders in elliott_wave_trading_bot.py

□ 3. Test with testnet=True first

□ 4. For live trading, set testnet=False

□ 5. Start with small position sizes

⚠️ SECURITY REMINDERS:
- Never share your API keys
- Use IP restrictions on Binance
- Start with testnet for practice
- Don't commit API keys to version control
"""