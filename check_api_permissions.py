"""
Check API Key Permissions
=========================
This script checks if your Binance Testnet API keys are valid and have the correct permissions.
"""

import os
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables
load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'

print("=" * 80)
print("🔐 API KEY PERMISSIONS CHECK")
print("=" * 80)
print(f"API Key: {api_key[:20]}..." if api_key else "❌ No API key found!")
print(f"Testnet Mode: {use_testnet}")
print("=" * 80)

if not api_key or not api_secret:
    print("\n❌ ERROR: API credentials not found in .env file!")
    print("\nTo fix this:")
    print("1. Go to: https://testnet.binancefuture.com/")
    print("2. Click 'API Key' in the top menu")
    print("3. Generate new API keys")
    print("4. Update the .env file with new keys")
    exit(1)

print("\n📡 Testing API connection...")

try:
    client = Client(api_key, api_secret, testnet=use_testnet)
    print("✅ Client initialized")
    
    # Test 1: Check server time
    print("\n🕐 Test 1: Checking server connection...")
    server_time = client.get_server_time()
    print(f"✅ Server time: {server_time}")
    
    # Test 2: Check API key permissions
    print("\n🔑 Test 2: Checking API key permissions...")
    api_permissions = client.get_account_api_permissions()
    print(f"✅ API Permissions: {api_permissions}")
    
    # Test 3: Get account information
    print("\n💰 Test 3: Getting account information...")
    account = client.futures_account()
    print(f"✅ Total Balance: ${float(account['totalWalletBalance']):.2f} USDT")
    print(f"✅ Available Balance: ${float(account['availableBalance']):.2f} USDT")
    
    # Test 4: Check if we can query positions
    print("\n📊 Test 4: Querying positions...")
    positions = client.futures_position_information()
    print(f"✅ Can query positions ({len(positions)} symbols)")
    
    # Test 5: Check order permissions
    print("\n📋 Test 5: Getting open orders...")
    orders = client.futures_get_open_orders()
    print(f"✅ Can query orders ({len(orders)} open orders)")
    
    print("\n" + "=" * 80)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 80)
    print("\n✅ Your API keys are valid and have the correct permissions.")
    print("✅ You can now place orders on Binance Futures Testnet.")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    
    print("\n" + "=" * 80)
    print("🔧 HOW TO FIX THIS:")
    print("=" * 80)
    
    if "Invalid API-key" in str(e) or "code=-2015" in str(e):
        print("\n❌ Your API keys are INVALID or EXPIRED!")
        print("\nTo fix this:")
        print("1. Go to: https://testnet.binancefuture.com/")
        print("2. Log in (or create an account)")
        print("3. Click 'API Key' in the top menu")
        print("4. Delete old API keys")
        print("5. Generate NEW API keys")
        print("6. Copy the API Key and Secret Key")
        print("7. Update your .env file:")
        print("   BINANCE_API_KEY=<your_new_key>")
        print("   BINANCE_API_SECRET=<your_new_secret>")
        print("   USE_TESTNET=true")
        print("\n⚠️  IMPORTANT: Make sure to enable these permissions:")
        print("   ✅ Enable Reading")
        print("   ✅ Enable Futures")
        print("   ✅ Enable Trading")
        
    elif "Timestamp" in str(e):
        print("\n⏰ Time synchronization error!")
        print("Your computer's clock may be out of sync.")
        print("Try synchronizing your system time.")
        
    elif "permissions" in str(e).lower():
        print("\n🔐 Your API key doesn't have the required permissions!")
        print("When generating API keys on Binance Testnet, make sure to enable:")
        print("   ✅ Enable Reading")
        print("   ✅ Enable Futures")
        print("   ✅ Enable Trading")
    
    print("=" * 80)
    exit(1)
