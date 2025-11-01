"""
Close Current Position
======================
"""

import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret, testnet=True)

SYMBOL = 'DOTUSDT'

print("=" * 80)
print(f"🔴 CLOSING {SYMBOL} POSITION")
print("=" * 80)

# Check current position
print(f"\n📊 Checking current position...")
try:
    positions = client.futures_position_information(symbol=SYMBOL)
    position_amt = 0
    
    for pos in positions:
        if pos['symbol'] == SYMBOL:
            position_amt = float(pos['positionAmt'])
            if abs(position_amt) > 0:
                print(f"   Position Size: {position_amt} DOT")
                print(f"   Entry Price: ${float(pos['entryPrice']):.4f}")
                print(f"   Mark Price: ${float(pos['markPrice']):.4f}")
                print(f"   Unrealized PnL: ${float(pos['unRealizedProfit']):.4f}")
            else:
                print(f"   ✅ No open position to close")
                exit(0)
            break
    
    if position_amt == 0:
        print("   ✅ No open position")
        exit(0)
        
    # Close position
    print(f"\n🔴 Closing position...")
    close_side = 'SELL' if position_amt > 0 else 'BUY'
    quantity = abs(position_amt)
    
    close_order = client.futures_create_order(
        symbol=SYMBOL,
        side=close_side,
        type='MARKET',
        quantity=quantity
    )
    
    print(f"✅ Position closed!")
    print(f"   Order ID: {close_order['orderId']}")
    print(f"   Side: {close_side}")
    print(f"   Quantity: {quantity}")
    
    # Check final position
    print(f"\n✅ Verifying position is closed...")
    import time
    time.sleep(1)
    
    positions = client.futures_position_information(symbol=SYMBOL)
    for pos in positions:
        if pos['symbol'] == SYMBOL:
            final_amt = float(pos['positionAmt'])
            if abs(final_amt) < 0.01:
                print(f"   ✅ Position successfully closed!")
            else:
                print(f"   ⚠️  Remaining position: {final_amt}")
            break
            
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    print(traceback.format_exc())

print("=" * 80)
