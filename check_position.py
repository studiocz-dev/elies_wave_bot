"""
Check Order Status and Position
================================
"""

import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret, testnet=True)

print("=" * 80)
print("📊 CHECKING ORDER STATUS AND POSITIONS")
print("=" * 80)

# Check the order we just placed
ORDER_ID = 91471997
SYMBOL = 'DOTUSDT'

print(f"\n🔍 Checking order {ORDER_ID}...")
try:
    order = client.futures_get_order(symbol=SYMBOL, orderId=ORDER_ID)
    print(f"   Status: {order['status']}")
    print(f"   Side: {order['side']}")
    print(f"   Type: {order['type']}")
    print(f"   Original Qty: {order['origQty']}")
    print(f"   Executed Qty: {order['executedQty']}")
    print(f"   Avg Price: {order['avgPrice']}")
    print(f"   Cumulative Quote Qty: {order['cumQuote']}")
    
    if float(order['executedQty']) > 0:
        actual_price = float(order['cumQuote']) / float(order['executedQty'])
        print(f"   ✅ Actual Fill Price: ${actual_price:.4f}")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print(f"\n📊 Checking {SYMBOL} position...")
try:
    positions = client.futures_position_information(symbol=SYMBOL)
    for pos in positions:
        if pos['symbol'] == SYMBOL:
            position_amt = float(pos['positionAmt'])
            if abs(position_amt) > 0:
                print(f"   ✅ Position Size: {position_amt} DOT")
                print(f"   Entry Price: ${float(pos['entryPrice']):.4f}")
                print(f"   Mark Price: ${float(pos['markPrice']):.4f}")
                print(f"   Unrealized PnL: ${float(pos['unRealizedProfit']):.4f}")
                print(f"   Leverage: {pos['leverage']}x")
            else:
                print(f"   No open position")
            break
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print(f"\n📋 Checking all open orders for {SYMBOL}...")
try:
    open_orders = client.futures_get_open_orders(symbol=SYMBOL)
    if open_orders:
        for order in open_orders:
            print(f"   Order ID: {order['orderId']}")
            print(f"   Type: {order['type']}")
            print(f"   Side: {order['side']}")
            print(f"   Quantity: {order['origQty']}")
            print(f"   Stop Price: {order.get('stopPrice', 'N/A')}")
            print("-" * 40)
    else:
        print("   No open orders")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n💰 Account Summary:")
try:
    account = client.futures_account()
    print(f"   Total Balance: ${float(account['totalWalletBalance']):.2f} USDT")
    print(f"   Available Balance: ${float(account['availableBalance']):.2f} USDT")
    print(f"   Total Unrealized Profit: ${float(account['totalUnrealizedProfit']):.2f} USDT")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("=" * 80)
