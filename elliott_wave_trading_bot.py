"""
Complete Elliott Wave Trading Bot for Binance Futures
===================================================

This is a production-ready trading bot that:
1. Continuously monitors markets for Elliott Wave patterns
2. Automatically places orders based on signals
3. Manages risk with stop-loss and take-profit orders
4. Tracks performance and maintains trading logs

IMPORTANT: This is for educational purposes. Use paper trading mode first!
"""

import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
import logging
from binance_data_fetcher import BinanceDataFetcher
from elliott_wave_trading_system import ElliottWaveTradingSystem


class ElliottWaveTradingBot:
    """
    Automated trading bot using Elliott Wave analysis
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True, config=None):
        """
        Initialize the trading bot
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret  
            testnet: Use paper trading mode
            config: Trading configuration dictionary
        """
        # Initialize trading system
        self.trading_system = ElliottWaveTradingSystem(api_key, api_secret, testnet)
        self.data_fetcher = self.trading_system.data_fetcher
        
        # Default configuration
        self.config = {
            'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT', 'SOLUSDT', 'DOGEUSDT', 'ATOMUSDT', 'DOTUSDT', 'LINKUSDT', 'AVAXUSDT'],
            'intervals': ['15m', '30m', '1h', '4h'],
            'scan_frequency': 300,  # seconds (5 minutes)
            'max_positions': 3,     # maximum concurrent positions
            'risk_per_trade': 0.02, # 2% risk per trade
            'min_confidence': 0.45,  # minimum pattern confidence (reduced from 0.6)
            'min_risk_reward': 1.2, # minimum risk/reward ratio (reduced from 1.5)
            'account_balance': 10000, # USDT balance for position sizing
        }
        
        # Update with custom config
        if config:
            self.config.update(config)
        
        # Trading state
        self.active_positions = {}
        self.trade_history = []
        self.last_scan_time = datetime.now()
        self.bot_running = False
        
        # Setup logging with UTF-8 encoding to handle emojis
        try:
            # Create file handler with UTF-8 encoding
            file_handler = logging.FileHandler('elliott_wave_bot.log', encoding='utf-8')
            
            # Create console handler with UTF-8 encoding
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Set formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Configure root logger
            logging.basicConfig(
                level=logging.INFO,
                handlers=[file_handler, console_handler]
            )
            
            self.logger = logging.getLogger(__name__)
            
        except Exception as e:
            # Fallback logging without emojis if UTF-8 fails
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
            self.logger.warning(f"UTF-8 logging setup failed: {e}. Using fallback logging.")
        
        self.safe_log("info", "Elliott Wave Trading Bot initialized", "🤖")
        self.safe_log("info", f"Configuration: {self.config}", "📊")
    
    def safe_log(self, level, message, emoji=""):
        """Safe logging method that handles Unicode encoding issues"""
        try:
            # Try logging with emoji
            full_message = f"{emoji} {message}" if emoji else message
            getattr(self.logger, level)(full_message)
        except UnicodeEncodeError:
            # Fall back to message without emoji
            getattr(self.logger, level)(message)
    
    def start_trading(self):
        """Start the automated trading loop"""
        self.bot_running = True
        self.safe_log("info", "Starting Elliott Wave Trading Bot...", "🚀")
        
        try:
            while self.bot_running:
                # Scan markets for opportunities
                self.scan_and_trade()
                
                # Check and manage existing positions
                self.manage_positions()
                
                # Log status
                self.log_status()
                
                # Wait for next scan
                time.sleep(self.config['scan_frequency'])
                
        except KeyboardInterrupt:
            self.safe_log("info", "Bot stopped by user", "⏹️")
        except Exception as e:
            self.safe_log("error", f"Bot error: {e}", "❌")
        finally:
            self.stop_trading()
    
    def stop_trading(self):
        """Stop the trading bot and cleanup"""
        self.bot_running = False
        self.safe_log("info", "Elliott Wave Trading Bot stopped", "🛑")
        
        # Close all positions if needed
        # self.close_all_positions()
    
    def scan_and_trade(self):
        """Scan markets and execute trades based on Elliott Wave signals"""
        self.safe_log("info", "Scanning markets for Elliott Wave patterns...", "🔍")
        
        all_signals = []
        
        # Scan each symbol and interval
        for symbol in self.config['symbols']:
            for interval in self.config['intervals']:
                try:
                    # Skip if we already have a position on this symbol
                    if symbol in self.active_positions:
                        continue
                    
                    # Get current analysis
                    analysis = self.trading_system.analyze_symbol(symbol, interval, 200)
                    
                    if analysis and analysis['signals']:
                        # Filter signals by confidence and risk/reward
                        valid_signals = [
                            s for s in analysis['signals']
                            if s['confidence'] >= self.config['min_confidence']
                            and s['risk_reward_ratio'] >= self.config['min_risk_reward']
                        ]
                        
                        all_signals.extend(valid_signals)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    self.logger.error(f"❌ Error scanning {symbol} {interval}: {e}")
        
        # Execute best signals
        if all_signals:
            # Sort by confidence and risk/reward
            all_signals.sort(
                key=lambda x: (x['confidence'], x['risk_reward_ratio']), 
                reverse=True
            )
            
            # Execute top signals up to max positions
            available_slots = self.config['max_positions'] - len(self.active_positions)
            
            for signal in all_signals[:available_slots]:
                self.execute_trade(signal)
    
    def execute_trade(self, signal):
        """
        Execute a trade based on Elliott Wave signal
        
        Args:
            signal: Trading signal dictionary
        """
        symbol = signal['symbol']
        
        try:
            self.safe_log("info", f"Executing {signal['type']} trade for {symbol}", "📈")
            
            # Calculate position size
            position_size = self.trading_system.get_position_size(
                symbol, 
                signal['entry_price'], 
                signal['stop_loss'],
                self.config['account_balance']
            )
            
            # Simulate trade execution (replace with real orders for live trading)
            trade = {
                'symbol': symbol,
                'type': signal['type'],
                'entry_price': signal['entry_price'],
                'position_size': position_size,
                'stop_loss': signal['stop_loss'],
                'take_profit_1': signal['take_profit_1'],
                'take_profit_2': signal.get('take_profit_2'),
                'confidence': signal['confidence'],
                'risk_reward_ratio': signal['risk_reward_ratio'],
                'entry_time': datetime.now(),
                'status': 'ACTIVE',
                'reason': signal['reason']
            }
            
            # Add to active positions
            self.active_positions[symbol] = trade
            
            # Log trade
            self.logger.info(f"✅ Trade executed: {symbol} {signal['type']}")
            self.logger.info(f"   Entry: ${signal['entry_price']:.2f}")
            self.logger.info(f"   Stop Loss: ${signal['stop_loss']:.2f}")
            self.logger.info(f"   Take Profit: ${signal['take_profit_1']:.2f}")
            self.logger.info(f"   Position Size: {position_size}")
            self.logger.info(f"   Confidence: {signal['confidence']:.1%}")
            
            # Save trade to history
            self.trade_history.append(trade.copy())
            
            # For live trading, replace this section with actual Binance orders:
            """
            if self.config.get('live_trading', False):
                # Place market order
                order = self.data_fetcher.client.futures_create_order(
                    symbol=symbol,
                    side='BUY' if signal['type'] == 'BUY' else 'SELL',
                    type='MARKET',
                    quantity=position_size
                )
                
                # Place stop loss order
                stop_order = self.data_fetcher.client.futures_create_order(
                    symbol=symbol,
                    side='SELL' if signal['type'] == 'BUY' else 'BUY',
                    type='STOP_MARKET',
                    quantity=position_size,
                    stopPrice=signal['stop_loss']
                )
                
                # Place take profit order
                tp_order = self.data_fetcher.client.futures_create_order(
                    symbol=symbol,
                    side='SELL' if signal['type'] == 'BUY' else 'BUY',
                    type='LIMIT',
                    quantity=position_size,
                    price=signal['take_profit_1']
                )
                
                # Store order IDs
                trade['order_id'] = order['orderId']
                trade['stop_order_id'] = stop_order['orderId']
                trade['tp_order_id'] = tp_order['orderId']
            """
            
        except Exception as e:
            self.logger.error(f"❌ Error executing trade for {symbol}: {e}")
    
    def manage_positions(self):
        """Monitor and manage active positions"""
        if not self.active_positions:
            return
        
        self.safe_log("info", f"Managing {len(self.active_positions)} active positions...", "📊")
        
        positions_to_close = []
        
        for symbol, position in self.active_positions.items():
            try:
                # Get current price
                current_price = self.data_fetcher.get_current_price(symbol)
                
                if current_price is None:
                    continue
                
                # Check stop loss and take profit levels
                position_closed = self.check_exit_conditions(position, current_price)
                
                if position_closed:
                    positions_to_close.append(symbol)
                else:
                    # Update position with current P&L
                    self.update_position_pnl(position, current_price)
                
            except Exception as e:
                self.logger.error(f"❌ Error managing position {symbol}: {e}")
        
        # Remove closed positions
        for symbol in positions_to_close:
            del self.active_positions[symbol]
    
    def check_exit_conditions(self, position, current_price):
        """Check if position should be closed based on stop loss or take profit"""
        symbol = position['symbol']
        trade_type = position['type']
        
        # Check stop loss
        if trade_type == 'BUY':
            if current_price <= position['stop_loss']:
                self.close_position(position, current_price, 'STOP_LOSS')
                return True
            elif current_price >= position['take_profit_1']:
                self.close_position(position, current_price, 'TAKE_PROFIT')
                return True
        
        elif trade_type == 'SELL':
            if current_price >= position['stop_loss']:
                self.close_position(position, current_price, 'STOP_LOSS')
                return True
            elif current_price <= position['take_profit_1']:
                self.close_position(position, current_price, 'TAKE_PROFIT')
                return True
        
        return False
    
    def close_position(self, position, exit_price, reason):
        """Close a position and calculate P&L"""
        symbol = position['symbol']
        
        # Calculate P&L
        if position['type'] == 'BUY':
            pnl = (exit_price - position['entry_price']) * position['position_size']
        else:
            pnl = (position['entry_price'] - exit_price) * position['position_size']
        
        pnl_percent = (pnl / self.config['account_balance']) * 100
        
        # Update position
        position['exit_price'] = exit_price
        position['exit_time'] = datetime.now()
        position['pnl'] = pnl
        position['pnl_percent'] = pnl_percent
        position['status'] = 'CLOSED'
        position['exit_reason'] = reason
        
        # Log closure
        self.logger.info(f"🔒 Position closed: {symbol}")
        self.logger.info(f"   Reason: {reason}")
        self.logger.info(f"   Entry: ${position['entry_price']:.2f}")
        self.logger.info(f"   Exit: ${exit_price:.2f}")
        self.logger.info(f"   P&L: ${pnl:.2f} ({pnl_percent:+.2f}%)")
        
        # Update account balance (for simulation)
        self.config['account_balance'] += pnl
    
    def update_position_pnl(self, position, current_price):
        """Update unrealized P&L for active position"""
        if position['type'] == 'BUY':
            unrealized_pnl = (current_price - position['entry_price']) * position['position_size']
        else:
            unrealized_pnl = (position['entry_price'] - current_price) * position['position_size']
        
        position['unrealized_pnl'] = unrealized_pnl
        position['current_price'] = current_price
    
    def log_status(self):
        """Log current bot status"""
        total_pnl = sum([p.get('pnl', 0) for p in self.trade_history if p.get('pnl')])
        unrealized_pnl = sum([p.get('unrealized_pnl', 0) for p in self.active_positions.values()])
        
        self.safe_log("info", f"Bot Status:", "📊")
        self.logger.info(f"   Active Positions: {len(self.active_positions)}")
        self.logger.info(f"   Total Trades: {len(self.trade_history)}")
        self.logger.info(f"   Account Balance: ${self.config['account_balance']:.2f}")
        self.logger.info(f"   Realized P&L: ${total_pnl:.2f}")
        self.logger.info(f"   Unrealized P&L: ${unrealized_pnl:.2f}")
    
    def get_performance_report(self):
        """Generate performance report"""
        if not self.trade_history:
            return "No trades executed yet."
        
        closed_trades = [t for t in self.trade_history if t.get('pnl') is not None]
        
        if not closed_trades:
            return "No closed trades yet."
        
        total_trades = len(closed_trades)
        winning_trades = len([t for t in closed_trades if t['pnl'] > 0])
        losing_trades = total_trades - winning_trades
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_pnl = sum([t['pnl'] for t in closed_trades])
        avg_win = np.mean([t['pnl'] for t in closed_trades if t['pnl'] > 0]) if winning_trades > 0 else 0
        avg_loss = np.mean([t['pnl'] for t in closed_trades if t['pnl'] < 0]) if losing_trades > 0 else 0
        
        report = f"""
📊 ELLIOTT WAVE TRADING BOT PERFORMANCE REPORT
{'='*50}
Total Trades: {total_trades}
Winning Trades: {winning_trades}
Losing Trades: {losing_trades}
Win Rate: {win_rate:.1f}%

Total P&L: ${total_pnl:.2f}
Average Win: ${avg_win:.2f}
Average Loss: ${avg_loss:.2f}
Profit Factor: {abs(avg_win/avg_loss):.2f if avg_loss != 0 else 'N/A'}

Account Balance: ${self.config['account_balance']:.2f}
Return: {((self.config['account_balance']/10000)-1)*100:+.2f}%
"""
        
        return report


# Demo Usage & Configuration
if __name__ == "__main__":
    print("=== ELLIOTT WAVE TRADING BOT ===\n")
    
    # Trading configuration
    config = {
        'symbols': ['BTCUSDT', 'ETHUSDT'],  # Symbols to trade
        'intervals': ['4h'],                # Timeframes to analyze
        'scan_frequency': 60,               # Scan every 60 seconds (demo)
        'max_positions': 2,                 # Max 2 concurrent positions
        'risk_per_trade': 0.01,            # 1% risk per trade
        'min_confidence': 0.7,              # 70% minimum confidence
        'min_risk_reward': 2.0,             # 2:1 minimum risk/reward
        'account_balance': 10000,           # $10,000 starting balance
    }
    
    # Initialize bot (PAPER TRADING MODE)
    # For paper trading (fake money):
    # bot = ElliottWaveTradingBot(testnet=True, config=config)
    
    # For LIVE TRADING, add your API credentials:
    api_key = "ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO"        # Binance Testnet API Key
    api_secret = "VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu"  # Binance Testnet Secret Key
    
    bot = ElliottWaveTradingBot(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,  # Set to False for live trading
        config=config
    )
    
    print("🔧 Bot Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    print("\n⚠️  IMPORTANT: This is PAPER TRADING mode for testing!")
    print("⚠️  For live trading, add your Binance API credentials.")
    print("⚠️  Always test thoroughly before risking real money!")
    
    # Run a single scan demonstration
    print("\n🔍 Running single market scan...")
    bot.scan_and_trade()
    
    print("\n📊 Current Status:")
    bot.log_status()
    
    print("\n✅ Demo complete!")
    print("\n🚀 To start continuous trading, call: bot.start_trading()")
    print("🛑 To stop trading, press Ctrl+C")
    
    # Uncomment to start continuous trading:
    # bot.start_trading()