"""
COMPLETE SETUP GUIDE: Elliott Wave Analyzer for Binance Futures Trading
======================================================================

This guide shows you EXACTLY how to use the Elliott Wave Analyzer
for automated Binance Futures trading.
"""

# Step 1: Install Required Packages
print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                          STEP 1: INSTALLATION                                   ║
╚══════════════════════════════════════════════════════════════════════════════════╝

Run these commands to install required packages:

    pip install python-binance ccxt pandas numpy plotly

""")

# Step 2: Get Binance API Credentials
print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                      STEP 2: BINANCE API SETUP                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

1. Go to Binance.com → Account → API Management
2. Create New API Key
3. Enable "Futures Trading" permission
4. Copy API Key and Secret Key
5. For testing: Use Binance Testnet (testnet.binancefuture.com)

IMPORTANT: 
• Start with TESTNET for practice
• Never share your API keys
• Use IP restrictions for security
""")

# Step 3: Basic Trading Example
basic_example = '''
# Example: Basic Elliott Wave Trading Setup

from binance_data_fetcher import BinanceDataFetcher
from elliott_wave_trading_system import ElliottWaveTradingSystem

# Initialize with your API credentials (TESTNET first!)
api_key = "your_api_key_here"
api_secret = "your_api_secret_here"

# Create trading system (paper trading mode)
trading_system = ElliottWaveTradingSystem(
    api_key=api_key,
    api_secret=api_secret,
    testnet=True  # ALWAYS start with testnet!
)

# Analyze a symbol for Elliott Wave patterns
analysis = trading_system.analyze_symbol('BTCUSDT', '4h', 200)

if analysis and analysis['signals']:
    for signal in analysis['signals']:
        print(f"📈 {signal['type']} Signal for {signal['symbol']}")
        print(f"   Entry: ${signal['entry_price']:.2f}")
        print(f"   Stop Loss: ${signal['stop_loss']:.2f}")
        print(f"   Take Profit: ${signal['take_profit_1']:.2f}")
        print(f"   Confidence: {signal['confidence']:.1%}")
'''

print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                        STEP 3: BASIC USAGE                                      ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")
print(basic_example)

# Step 4: Advanced Trading Bot
advanced_example = '''
# Example: Advanced Automated Trading Bot

import time
from datetime import datetime

class LiveTradingBot:
    def __init__(self, api_key, api_secret):
        self.trading_system = ElliottWaveTradingSystem(
            api_key=api_key,
            api_secret=api_secret,
            testnet=False  # LIVE TRADING - Be careful!
        )
        self.positions = {}
        self.balance = 10000  # Your account balance
        
    def run_continuous_trading(self):
        """Run continuous market scanning and trading"""
        symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']
        
        while True:
            try:
                print(f"🔍 Scanning markets at {datetime.now()}")
                
                for symbol in symbols:
                    # Skip if already have position
                    if symbol in self.positions:
                        continue
                        
                    # Analyze for Elliott Wave patterns
                    analysis = self.trading_system.analyze_symbol(symbol, '4h')
                    
                    if analysis and analysis['signals']:
                        best_signal = max(analysis['signals'], 
                                        key=lambda x: x['confidence'])
                        
                        # Execute trade if confidence > 70%
                        if best_signal['confidence'] > 0.7:
                            self.execute_live_trade(best_signal)
                    
                    time.sleep(5)  # Rate limiting
                
                # Check existing positions
                self.manage_positions()
                
                # Wait 5 minutes before next scan
                time.sleep(300)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(60)
    
    def execute_live_trade(self, signal):
        """Execute actual trade on Binance"""
        try:
            symbol = signal['symbol']
            
            # Calculate position size (1% account risk)
            risk_amount = self.balance * 0.01
            price_distance = abs(signal['entry_price'] - signal['stop_loss'])
            position_size = risk_amount / price_distance
            
            # Place market order
            order = self.trading_system.data_fetcher.client.futures_create_order(
                symbol=symbol,
                side='BUY' if signal['type'] == 'BUY' else 'SELL',
                type='MARKET',
                quantity=round(position_size, 6)
            )
            
            # Place stop loss
            stop_order = self.trading_system.data_fetcher.client.futures_create_order(
                symbol=symbol,
                side='SELL' if signal['type'] == 'BUY' else 'BUY',
                type='STOP_MARKET',
                quantity=round(position_size, 6),
                stopPrice=signal['stop_loss']
            )
            
            # Track position
            self.positions[symbol] = {
                'entry_price': signal['entry_price'],
                'position_size': position_size,
                'stop_loss': signal['stop_loss'],
                'take_profit': signal['take_profit_1'],
                'order_id': order['orderId']
            }
            
            print(f"✅ Trade executed: {symbol} {signal['type']}")
            
        except Exception as e:
            print(f"❌ Trade execution error: {e}")
    
    def manage_positions(self):
        """Monitor and manage active positions"""
        for symbol, position in list(self.positions.items()):
            try:
                # Get current price
                current_price = self.trading_system.data_fetcher.get_current_price(symbol)
                
                # Check if take profit hit
                if ((position['type'] == 'BUY' and current_price >= position['take_profit']) or
                    (position['type'] == 'SELL' and current_price <= position['take_profit'])):
                    
                    # Close position at take profit
                    self.close_position(symbol, current_price, 'TAKE_PROFIT')
                    
            except Exception as e:
                print(f"❌ Position management error for {symbol}: {e}")
    
    def close_position(self, symbol, price, reason):
        """Close a position and calculate P&L"""
        position = self.positions[symbol]
        
        # Calculate P&L
        if position['type'] == 'BUY':
            pnl = (price - position['entry_price']) * position['position_size']
        else:
            pnl = (position['entry_price'] - price) * position['position_size']
        
        print(f"🔒 Position closed: {symbol} - P&L: ${pnl:.2f}")
        
        # Update balance
        self.balance += pnl
        
        # Remove from active positions
        del self.positions[symbol]

# Usage (CAREFUL - This is live trading!)
# bot = LiveTradingBot(api_key="your_key", api_secret="your_secret")
# bot.run_continuous_trading()
'''

print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    STEP 4: ADVANCED LIVE TRADING BOT                            ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")
print(advanced_example)

# Step 5: Risk Management Guidelines
print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                      STEP 5: RISK MANAGEMENT                                    ║
╚══════════════════════════════════════════════════════════════════════════════════╝

🛡️ ESSENTIAL RISK MANAGEMENT RULES:

1. POSITION SIZING
   • Never risk more than 1-2% per trade
   • Calculate position size based on stop loss distance
   • Use: Position Size = (Account * Risk%) / (Entry - Stop Loss)

2. STOP LOSSES
   • ALWAYS use stop losses
   • Place stops 2-3% beyond Elliott Wave invalidation levels
   • Use trailing stops for profitable positions

3. TAKE PROFITS
   • Scale out at multiple targets
   • First target: 50% at nearby resistance
   • Second target: 50% at wave projection levels

4. PORTFOLIO LIMITS
   • Maximum 3-5 concurrent positions
   • Diversify across different symbols
   • Avoid over-leveraging

5. MARKET CONDITIONS
   • Elliott Wave works best in trending markets
   • Reduce position sizes in choppy conditions
   • Monitor broader market sentiment

6. DRAWDOWN MANAGEMENT
   • Stop trading after 10% account drawdown
   • Review and adjust strategy
   • Never chase losses with bigger positions

⚠️ WARNINGS:
• Elliott Wave analysis is subjective
• Patterns can fail or extend beyond expectations
• Always have an exit plan
• Markets can gap against you
• Use proper leverage (max 10x for crypto)
""")

# Step 6: Performance Monitoring
print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                   STEP 6: PERFORMANCE MONITORING                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝

📊 KEY METRICS TO TRACK:

• Win Rate: Target 60%+ winning trades
• Profit Factor: Gross Profit / Gross Loss (target >1.5)
• Risk/Reward Ratio: Average Win / Average Loss (target >2.0)
• Maximum Drawdown: Largest peak-to-trough decline
• Sharpe Ratio: Risk-adjusted returns
• Monthly Returns: Consistent profitability

📝 TRADING LOG TEMPLATE:

Date | Symbol | Type | Entry | Exit | Size | P&L | % | Reason | Notes
-----|--------|------|-------|------|------|-----|---|--------|-------
10/30| BTCUSDT| BUY  | 70000 | 72000| 0.1  | 200 |2% | Wave5  | Good

🔄 STRATEGY OPTIMIZATION:

1. Backtest on 1+ years of historical data
2. Forward test on paper trading for 1 month
3. Start live trading with minimal position sizes
4. Gradually increase size as confidence grows
5. Regularly review and adjust parameters
""")

# Final Implementation Checklist
print("""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    FINAL IMPLEMENTATION CHECKLIST                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝

□ 1. Install all required Python packages
□ 2. Set up Binance account and get API credentials
□ 3. Test with Binance Testnet first
□ 4. Understand Elliott Wave theory basics
□ 5. Run the provided examples and understand outputs
□ 6. Backtest strategy on historical data
□ 7. Paper trade for at least 1 month
□ 8. Define risk management rules
□ 9. Start with small position sizes
□ 10. Monitor performance and adjust

🚀 READY TO START TRADING!

Remember:
• Start small and scale up gradually
• Always use proper risk management
• Keep learning and improving your strategy
• Elliott Wave analysis takes practice to master
• Consider combining with other indicators

Good luck with your Elliott Wave trading journey! 📈
""")

if __name__ == "__main__":
    print("Elliott Wave Futures Trading Setup Guide Displayed!")
    print("\n📚 All files are ready in your workspace:")
    print("   • binance_data_fetcher.py - Data fetching from Binance")
    print("   • elliott_wave_trading_system.py - Signal generation")
    print("   • futures_trading_demo.py - Complete trading demo")
    print("\n🎯 Next: Set up your Binance API and start paper trading!")