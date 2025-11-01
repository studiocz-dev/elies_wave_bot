"""
FINAL TEST: Complete Order with Stop Loss and Take Profit
=========================================================
This test uses the FIXED logic to place orders correctly
"""

import os
import time
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret, testnet=True)

# Test configuration
SYMBOL = 'DOTUSDT'
SIDE = 'BUY'
POSITION_SIZE_USDT = 15
STOP_LOSS_PCT = 0.05  # 5%
TAKE_PROFIT_PCT = 0.10  # 10% (2:1 R/R)

print("=" * 80)
print("🧪 FINAL TEST: COMPLETE ORDER PLACEMENT")
print("=" * 80)
print(f"Symbol: {SYMBOL}")
print(f"Side: {SIDE}")
print(f"Position Size: ${POSITION_SIZE_USDT} USDT")
print(f"Stop Loss: {STOP_LOSS_PCT*100}%")
print(f"Take Profit: {TAKE_PROFIT_PCT*100}%")
print("=" * 80)

# Get current price
print(f"\n📊 Getting current price...")
ticker = client.futures_symbol_ticker(symbol=SYMBOL)
current_price = float(ticker['price'])
print(f"   Current Price: ${current_price:.4f}")

# Calculate quantity
quantity = POSITION_SIZE_USDT / current_price

# Get precision
exchange_info = client.futures_exchange_info()
for s in exchange_info['symbols']:
    if s['symbol'] == SYMBOL:
        for f in s['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
                quantity_precision = len(str(step_size).rstrip('0').split('.')[-1])
                quantity = round(quantity, quantity_precision)
                print(f"   Quantity: {quantity} {SYMBOL.replace('USDT', '')}")
                break
        break

# Ask confirmation
print("\n" + "=" * 80)
response = input(f"🤔 Place test {SIDE} order for {quantity} {SYMBOL}? (yes/no): ").strip().lower()
if response != 'yes':
    print("❌ Cancelled")
    exit(0)

# STEP 1: Place MARKET order
print("\n" + "=" * 80)
print("📤 STEP 1: Placing MARKET order...")
print("=" * 80)

try:
    market_order = client.futures_create_order(
        symbol=SYMBOL,
        side=SIDE,
        type='MARKET',
        quantity=quantity
    )
    
    print(f"✅ MARKET order placed!")
    print(f"   Order ID: {market_order['orderId']}")
    
    # CRITICAL FIX: Query order to get actual fill price
    print(f"\n🔍 Fetching actual fill price...")
    time.sleep(0.5)  # Brief delay
    
    filled_order = client.futures_get_order(symbol=SYMBOL, orderId=market_order['orderId'])
    
    # Calculate entry price
    if float(filled_order['executedQty']) > 0:
        entry_price = float(filled_order['cumQuote']) / float(filled_order['executedQty'])
    else:
        entry_price = current_price
    
    print(f"   ✅ Actual fill price: ${entry_price:.4f}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    exit(1)

# Get price precision for stop orders
price_precision = 2  # Default
for s in exchange_info['symbols']:
    if s['symbol'] == SYMBOL:
        for f in s['filters']:
            if f['filterType'] == 'PRICE_FILTER':
                tick_size = float(f['tickSize'])
                price_precision = len(str(tick_size).rstrip('0').split('.')[-1])
                print(f"   Price precision: {price_precision} decimals (tick_size: {tick_size})")
                break
        break

# Calculate SL and TP prices
if SIDE == 'BUY':
    stop_loss_price = round(entry_price * (1 - STOP_LOSS_PCT), price_precision)
    take_profit_price = round(entry_price * (1 + TAKE_PROFIT_PCT), price_precision)
    sl_side = 'SELL'
else:
    stop_loss_price = round(entry_price * (1 + STOP_LOSS_PCT), price_precision)
    take_profit_price = round(entry_price * (1 - TAKE_PROFIT_PCT), price_precision)
    sl_side = 'BUY'

# STEP 2: Place STOP LOSS order
print("\n" + "=" * 80)
print("📤 STEP 2: Placing STOP LOSS order...")
print("=" * 80)
print(f"   Stop Price: ${stop_loss_price:.4f}")

try:
    sl_order = client.futures_create_order(
        symbol=SYMBOL,
        side=sl_side,
        type='STOP_MARKET',
        stopPrice=stop_loss_price,
        quantity=quantity,
        closePosition=True
    )
    
    print(f"✅ STOP LOSS order placed!")
    print(f"   Order ID: {sl_order['orderId']}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

# STEP 3: Place TAKE PROFIT order
print("\n" + "=" * 80)
print("📤 STEP 3: Placing TAKE PROFIT order...")
print("=" * 80)
print(f"   Stop Price: ${take_profit_price:.4f}")

try:
    tp_order = client.futures_create_order(
        symbol=SYMBOL,
        side=sl_side,
        type='TAKE_PROFIT_MARKET',
        stopPrice=take_profit_price,
        quantity=quantity,
        closePosition=True
    )
    
    print(f"✅ TAKE PROFIT order placed!")
    print(f"   Order ID: {tp_order['orderId']}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

# Final summary
print("\n" + "=" * 80)
print("🎉 TEST COMPLETE!")
print("=" * 80)
print(f"✅ Position opened: {quantity} {SYMBOL.replace('USDT', '')} @ ${entry_price:.4f}")
print(f"✅ Stop Loss: ${stop_loss_price:.4f} ({STOP_LOSS_PCT*100}% loss)")
print(f"✅ Take Profit: ${take_profit_price:.4f} ({TAKE_PROFIT_PCT*100}% profit)")
print("=" * 80)
print("\n🔍 Verify at: https://testnet.binancefuture.com/")
print("=" * 80)
