"""
Test Binance Testnet Connection with Manual Configuration
=========================================================
"""

import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

print("=" * 80)
print("🧪 TESTING BINANCE TESTNET CONNECTION")
print("=" * 80)
print(f"API Key: {api_key[:20]}..." if api_key else "❌ No API key")
print("=" * 80)

# Try different testnet configurations
configs = [
    {
        'name': 'Standard Testnet',
        'testnet': True,
        'tld': 'com'
    },
    {
        'name': 'Testnet with custom URL',
        'testnet': False,
        'tld': 'com',
        'base_endpoint': 'https://testnet.binancefuture.com'
    }
]

for config in configs:
    print(f"\n📡 Testing: {config['name']}")
    print("-" * 80)
    
    try:
        # Initialize client with config
        if 'base_endpoint' in config:
            client = Client(
                api_key, 
                api_secret,
                testnet=config.get('testnet', False),
                tld=config.get('tld', 'com')
            )
            # Manually set futures base endpoint
            client.FUTURES_URL = config['base_endpoint']
        else:
            client = Client(
                api_key, 
                api_secret,
                testnet=config.get('testnet', False),
                tld=config.get('tld', 'com')
            )
        
        # Test connection
        print("   Testing server connection...")
        server_time = client.futures_time()
        print(f"   ✅ Server time: {server_time}")
        
        # Test account
        print("   Testing account access...")
        account = client.futures_account()
        balance = float(account['totalWalletBalance'])
        print(f"   ✅ Balance: ${balance:.2f} USDT")
        
        print(f"\n🎉 SUCCESS with: {config['name']}")
        print("=" * 80)
        break
        
    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        continue

else:
    print("\n" + "=" * 80)
    print("❌ ALL CONFIGURATIONS FAILED")
    print("=" * 80)
    print("\nPlease verify:")
    print("1. Your API keys are from: https://testnet.binancefuture.com/")
    print("2. API key permissions include: Reading, Futures, Trading")
    print("3. The keys were just generated (not expired)")
    print("=" * 80)
