"""
Test Order Placement Script
===========================
This script tests placing a small order on Binance Futures Testnet
to verify the order placement logic works before deploying to production.
"""

import os
import sys
from dotenv import load_dotenv
from binance.client import Client

# Load environment variables
load_dotenv()

# Get API credentials
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'

print("=" * 80)
print("🧪 BINANCE FUTURES TESTNET - ORDER PLACEMENT TEST")
print("=" * 80)
print(f"API Key: {api_key[:10]}..." if api_key else "No API key found!")
print(f"Testnet Mode: {use_testnet}")
print("=" * 80)

if not api_key or not api_secret:
    print("❌ ERROR: API credentials not found in .env file!")
    sys.exit(1)

# Initialize Binance client
print("\n📡 Initializing Binance client...")
client = Client(api_key, api_secret, testnet=use_testnet)
print("✅ Client initialized successfully!")

# Check account balance
print("\n💰 Checking account balance...")
try:
    account = client.futures_account()
    total_balance = float(account['totalWalletBalance'])
    available_balance = float(account['availableBalance'])
    
    print(f"   Total Balance: ${total_balance:.2f} USDT")
    print(f"   Available Balance: ${available_balance:.2f} USDT")
    
    if available_balance < 10:
        print(f"⚠️  WARNING: Low balance! You need at least $10 USDT for testing.")
        print(f"   Get testnet funds at: https://testnet.binancefuture.com/")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ ERROR checking balance: {str(e)}")
    sys.exit(1)

# Test configuration
TEST_SYMBOL = 'DOTUSDT'  # Using DOT since bot is trading it
TEST_SIDE = 'BUY'  # BUY or SELL
TEST_POSITION_SIZE_USDT = 15  # $15 worth (smaller amount for testing)

print(f"\n🎯 Test Order Configuration:")
print(f"   Symbol: {TEST_SYMBOL}")
print(f"   Side: {TEST_SIDE}")
print(f"   Position Size: ${TEST_POSITION_SIZE_USDT} USDT")
print(f"   Stop Loss: 5% from entry")
print(f"   Take Profit: 10% from entry (2:1 R/R)")

# Get current price
print(f"\n📊 Getting current price for {TEST_SYMBOL}...")
try:
    ticker = client.futures_symbol_ticker(symbol=TEST_SYMBOL)
    current_price = float(ticker['price'])
    print(f"   Current Price: ${current_price:.2f}")
except Exception as e:
    print(f"❌ ERROR getting price: {str(e)}")
    sys.exit(1)

# Calculate quantity
quantity = TEST_POSITION_SIZE_USDT / current_price
print(f"\n🔢 Calculating quantity...")
print(f"   Raw quantity: {quantity}")

# Get symbol precision
print(f"\n🔍 Getting symbol precision...")
try:
    exchange_info = client.futures_exchange_info()
    quantity_precision = 1  # Default
    min_qty = 0.1
    
    for s in exchange_info['symbols']:
        if s['symbol'] == TEST_SYMBOL:
            for f in s['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    step_size = float(f['stepSize'])
                    min_qty = float(f['minQty'])
                    quantity_precision = len(str(step_size).rstrip('0').split('.')[-1])
                    print(f"   Min Quantity: {min_qty}")
                    print(f"   Step Size: {step_size}")
                    print(f"   Precision: {quantity_precision} decimals")
                    break
            break
    
    # Round quantity
    quantity = round(quantity, quantity_precision)
    print(f"   Rounded quantity: {quantity}")
    
    if quantity < min_qty:
        print(f"⚠️  WARNING: Quantity {quantity} is less than minimum {min_qty}")
        quantity = min_qty
        print(f"   Adjusted to minimum: {quantity}")
        
except Exception as e:
    print(f"❌ ERROR getting precision: {str(e)}")
    sys.exit(1)

# Ask for confirmation
print("\n" + "=" * 80)
print("⚠️  READY TO PLACE TEST ORDER")
print("=" * 80)
print(f"Order Summary:")
print(f"  {TEST_SIDE} {quantity} {TEST_SYMBOL} @ ${current_price:.2f}")
print(f"  Total Value: ${quantity * current_price:.2f} USDT")
print(f"  Stop Loss: ${current_price * 0.95:.2f} (-5%)")
print(f"  Take Profit: ${current_price * 1.10:.2f} (+10%)")
print("=" * 80)

response = input("\n🤔 Place this test order? (yes/no): ").strip().lower()

if response != 'yes':
    print("❌ Order cancelled by user.")
    sys.exit(0)

# Place MARKET order
print("\n" + "=" * 80)
print("📤 STEP 1: Placing MARKET order...")
print("=" * 80)

try:
    market_order = client.futures_create_order(
        symbol=TEST_SYMBOL,
        side=TEST_SIDE,
        type='MARKET',
        quantity=quantity
    )
    
    print("✅ MARKET ORDER PLACED SUCCESSFULLY!")
    print(f"   Order ID: {market_order['orderId']}")
    print(f"   Status: {market_order['status']}")
    print(f"   Executed Qty: {market_order.get('executedQty', 'N/A')}")
    
    # Get entry price
    entry_price = float(market_order.get('avgPrice', current_price))
    print(f"   Entry Price: ${entry_price:.2f}")
    
except Exception as e:
    print(f"❌ ERROR placing MARKET order: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")
    sys.exit(1)

# Calculate SL and TP prices
if TEST_SIDE == 'BUY':
    stop_loss_price = entry_price * 0.95  # 5% below
    take_profit_price = entry_price * 1.10  # 10% above
    sl_side = 'SELL'
else:
    stop_loss_price = entry_price * 1.05  # 5% above
    take_profit_price = entry_price * 0.90  # 10% below
    sl_side = 'BUY'

# Place STOP LOSS order
print("\n" + "=" * 80)
print("📤 STEP 2: Placing STOP LOSS order...")
print("=" * 80)
print(f"   Stop Price: ${stop_loss_price:.2f}")

try:
    sl_order = client.futures_create_order(
        symbol=TEST_SYMBOL,
        side=sl_side,
        type='STOP_MARKET',
        stopPrice=round(stop_loss_price, 2),
        quantity=quantity,
        closePosition=True
    )
    
    print("✅ STOP LOSS ORDER PLACED SUCCESSFULLY!")
    print(f"   Order ID: {sl_order['orderId']}")
    print(f"   Stop Price: ${sl_order.get('stopPrice', 'N/A')}")
    
except Exception as e:
    print(f"❌ ERROR placing STOP LOSS order: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")

# Place TAKE PROFIT order
print("\n" + "=" * 80)
print("📤 STEP 3: Placing TAKE PROFIT order...")
print("=" * 80)
print(f"   Stop Price: ${take_profit_price:.2f}")

try:
    tp_order = client.futures_create_order(
        symbol=TEST_SYMBOL,
        side=sl_side,
        type='TAKE_PROFIT_MARKET',
        stopPrice=round(take_profit_price, 2),
        quantity=quantity,
        closePosition=True
    )
    
    print("✅ TAKE PROFIT ORDER PLACED SUCCESSFULLY!")
    print(f"   Order ID: {tp_order['orderId']}")
    print(f"   Stop Price: ${tp_order.get('stopPrice', 'N/A')}")
    
except Exception as e:
    print(f"❌ ERROR placing TAKE PROFIT order: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")

# Final summary
print("\n" + "=" * 80)
print("🎉 TEST ORDER PLACEMENT COMPLETE!")
print("=" * 80)
print(f"✅ Market Order: {market_order['orderId']}")
print(f"✅ Stop Loss Order: {sl_order['orderId']}")
print(f"✅ Take Profit Order: {tp_order['orderId']}")
print("=" * 80)
print("\n🔍 Verify your orders at:")
print("   https://testnet.binancefuture.com/")
print("   Go to: Positions → Open Orders")
print("=" * 80)

print("\n⚠️  Remember to CLOSE the position manually if you don't want to wait for SL/TP!")
print("=" * 80)
