"""
Enhanced Elliott Wave Trading Bot with Configurable Settings
Uses external configuration file for easy parameter adjustment
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json

from elliott_wave_trading_system import ElliottWaveTradingSystem
from enhanced_bot_config import BotConfig


class EnhancedElliottWaveTradingBot:
    """Enhanced Elliott Wave Trading Bot with configurable parameters"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, config_file: str = "bot_config.json"):
        """Initialize the enhanced trading bot"""
        
        # Load configuration
        self.config_manager = BotConfig(config_file)
        self.config = self.config_manager.config
        
        # Initialize trading system
        self.trading_system = ElliottWaveTradingSystem(api_key, api_secret, testnet)
        self.data_fetcher = self.trading_system.data_fetcher
        
        # Trading state
        self.active_positions = {}
        self.bot_running = False
        self.daily_pnl = 0.0
        self.trade_count = 0
        self.start_time = datetime.now()
        
        # Setup logging
        self.setup_logging()
        
        self.safe_log("info", "Enhanced Elliott Wave Trading Bot initialized", "🤖")
        self.safe_log("info", f"Loaded configuration from {config_file}", "📊")
        self.config_manager.print_config()
    
    def setup_logging(self):
        """Setup enhanced logging system"""
        try:
            # Setup file logging with UTF-8 encoding
            log_filename = f"enhanced_elliott_wave_bot_{datetime.now().strftime('%Y%m%d')}.log"
            
            logging.basicConfig(
                level=getattr(logging, self.config['log_level']),
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_filename, encoding='utf-8'),
                    logging.StreamHandler() if self.config['console_output'] else logging.NullHandler()
                ]
            )
            self.logger = logging.getLogger(__name__)
            self.safe_log("info", f"Logging setup complete: {log_filename}", "📝")
            
        except Exception as e:
            # Fallback logging setup
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)
            self.logger.warning(f"UTF-8 logging setup failed: {e}. Using fallback logging.")
    
    def safe_log(self, level: str, message: str, emoji: str = ""):
        """Safe logging method that handles Unicode encoding issues"""
        try:
            # Try logging with emoji
            full_message = f"{emoji} {message}" if emoji else message
            getattr(self.logger, level)(full_message)
        except UnicodeEncodeError:
            # Fall back to message without emoji
            getattr(self.logger, level)(message)
    
    def start_trading(self):
        """Start the enhanced automated trading loop"""
        self.bot_running = True
        self.safe_log("info", "Starting Enhanced Elliott Wave Trading Bot...", "🚀")
        self.safe_log("info", f"Monitoring {len(self.config['symbols'])} symbols across {len(self.config['intervals'])} timeframes", "📊")
        
        # Check account balance
        self.check_account_balance()
        
        try:
            while self.bot_running:
                # Check daily loss limit
                if self.check_daily_loss_limit():
                    self.safe_log("warning", "Daily loss limit reached. Stopping trading.", "🛑")
                    break
                
                # Scan markets for opportunities
                self.scan_and_trade()
                
                # Check and manage existing positions
                self.manage_positions()
                
                # Log enhanced status
                self.log_enhanced_status()
                
                # Wait for next scan
                time.sleep(self.config['scan_frequency'])
                
        except KeyboardInterrupt:
            self.safe_log("info", "Bot stopped by user", "⏹️")
        except Exception as e:
            self.safe_log("error", f"Bot error: {str(e)}", "❌")
        finally:
            self.shutdown()
    
    def check_account_balance(self):
        """Check and display Binance Futures account balance"""
        try:
            account = self.data_fetcher.client.futures_account()
            total_balance = float(account['totalWalletBalance'])
            available_balance = float(account['availableBalance'])
            
            self.safe_log("info", 
                f"💰 Account Balance: ${total_balance:.2f} USDT "
                f"(Available: ${available_balance:.2f})", "💰")
            
            if available_balance < 10:
                self.safe_log("warning", 
                    f"⚠️ Low balance! Available: ${available_balance:.2f} USDT. "
                    f"Minimum recommended: $10 USDT", "⚠️")
                
        except Exception as e:
            self.safe_log("error", f"Error checking account balance: {str(e)}", "❌")
    
    def check_daily_loss_limit(self) -> bool:
        """Check if daily loss limit has been reached"""
        max_daily_loss = self.config['account_balance'] * self.config['max_daily_loss']
        if abs(self.daily_pnl) >= max_daily_loss and self.daily_pnl < 0:
            return True
        return False
    
    def scan_and_trade(self):
        """Enhanced market scanning with better filtering"""
        self.safe_log("info", f"Scanning {len(self.config['symbols'])} symbols...", "🔍")
        
        for symbol in self.config['symbols']:
            for interval in self.config['intervals']:
                try:
                    # Skip if we already have max positions
                    if len(self.active_positions) >= self.config['max_positions']:
                        continue
                    
                    # Check if symbol exists and get market data with volume filtering
                    if not self.check_market_conditions(symbol):
                        continue
                    
                    # Analyze Elliott Wave patterns
                    analysis_results = self.trading_system.analyze_symbol(symbol, interval)
                    
                    if analysis_results and analysis_results.get('signals'):
                        signals = analysis_results['signals']
                        
                        # Apply enhanced signal filtering
                        valid_signals = [
                            s for s in signals 
                            if isinstance(s, dict) and 
                            s.get('confidence', 0) >= self.config['min_confidence'] and
                            s.get('risk_reward_ratio', 0) >= self.config['min_risk_reward']
                        ]
                        
                        if valid_signals:
                            self.safe_log("info", f"✅ Valid signals found for {symbol} {interval}: {len(valid_signals)}", "✅")
                            
                            for signal in valid_signals:
                                self.safe_log("info", f"🎯 Attempting to execute trade for {symbol} {interval}", "")
                                self.safe_log("info", f"   Signal details: {signal.get('direction')} @ {signal.get('entry_price')} (confidence: {signal.get('confidence'):.1%})", "")
                                self.execute_trade(signal, symbol, interval)
                    
                except Exception as e:
                    # Handle specific error types
                    if "Invalid symbol" in str(e) or "does not exist" in str(e):
                        self.safe_log("warning", f"Symbol {symbol} not available on futures, skipping", "⚠️")
                        continue
                    else:
                        self.safe_log("error", f"Error analyzing {symbol} {interval}: {str(e)}", "❌")
    
    def check_market_conditions(self, symbol: str) -> bool:
        """Check if market conditions are suitable for trading"""
        try:
            # Get 24h ticker data using correct futures API method
            ticker = self.data_fetcher.client.futures_ticker(symbol=symbol)
            
            # Check volume requirement
            volume_24h = float(ticker['quoteVolume'])
            if volume_24h < self.config['min_volume_24h']:
                return False
            
            # Check spread (if data available)
            bid_price = float(ticker.get('bidPrice', 0))
            ask_price = float(ticker.get('askPrice', 0))
            
            if bid_price > 0 and ask_price > 0:
                spread = (ask_price - bid_price) / bid_price
                if spread > self.config['max_spread_percentage']:
                    return False
            
            return True
            
        except Exception as e:
            self.safe_log("warning", f"Could not check market conditions for {symbol}: {str(e)}", "⚠️")
            return True  # Default to allow trading if check fails
    
    def execute_trade(self, signal: Dict, symbol: str, interval: str):
        """Execute trade with enhanced risk management and REAL order placement"""
        self.safe_log("info", f"🔵 EXECUTE_TRADE called for {symbol} {interval}", "")
        
        try:
            self.safe_log("info", f"   Step 1: Calculating position size...", "")
            # Calculate position size based on risk
            position_size = self.calculate_position_size(signal)
            self.safe_log("info", f"   Position size calculated: ${position_size:.2f} USDT", "")
            
            if position_size <= 0:
                self.safe_log("warning", f"⚠️ Invalid position size for {symbol}: ${position_size}", "⚠️")
                return
            
            self.safe_log("info", f"   Step 2: Getting current price from Binance...", "")
            # Get current price
            current_price = float(self.data_fetcher.client.futures_symbol_ticker(symbol=symbol)['price'])
            self.safe_log("info", f"   Current price: ${current_price:.4f}", "")
            
            self.safe_log("info", f"   Step 3: Calculating quantity...", "")
            # Calculate quantity based on position size in USDT
            quantity = position_size / current_price
            self.safe_log("info", f"   Raw quantity: {quantity}", "")
            
            self.safe_log("info", f"   Step 4: Getting symbol precision from Binance...", "")
            # Get symbol info to round quantity properly
            symbol_info = self.data_fetcher.client.futures_exchange_info()
            quantity_precision = 0
            for s in symbol_info['symbols']:
                if s['symbol'] == symbol:
                    for f in s['filters']:
                        if f['filterType'] == 'LOT_SIZE':
                            step_size = float(f['stepSize'])
                            quantity_precision = len(str(step_size).rstrip('0').split('.')[-1])
                            self.safe_log("info", f"   Found precision: {quantity_precision} decimals (step_size: {step_size})", "")
                            break
                    break
            
            # Round quantity to proper precision
            quantity = round(quantity, quantity_precision)
            self.safe_log("info", f"   Rounded quantity: {quantity}", "")
            
            if quantity <= 0:
                self.safe_log("warning", f"⚠️ Quantity too small for {symbol}: {quantity}", "⚠️")
                return
            
            # Determine order side
            side = 'BUY' if signal['direction'] == 'LONG' else 'SELL'
            
            # Place MARKET order on Binance Futures
            self.safe_log("info", f"📤 Step 5: Placing {side} MARKET order on Binance Futures...", "🔵")
            self.safe_log("info", f"   Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Price: ${current_price:.4f}", "")
            
            order = self.data_fetcher.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            self.safe_log("info", f"✅ MARKET order placed successfully!", "")
            self.safe_log("info", f"   Order ID: {order.get('orderId')}", "")
            
            # Get actual fill price by querying the order
            self.safe_log("info", f"   Fetching actual fill price...", "")
            import time
            time.sleep(0.5)  # Brief delay to ensure order is filled
            
            filled_order = self.data_fetcher.client.futures_get_order(
                symbol=symbol, 
                orderId=order['orderId']
            )
            
            # Calculate entry price from filled order
            if float(filled_order['executedQty']) > 0:
                entry_price = float(filled_order['cumQuote']) / float(filled_order['executedQty'])
            else:
                entry_price = current_price
                
            self.safe_log("info", f"   ✅ Actual fill price: ${entry_price:.4f}", "")
            
            # Get price precision for stop orders
            self.safe_log("info", f"   Getting price precision for {symbol}...", "")
            price_precision = 2  # Default
            for s in symbol_info['symbols']:
                if s['symbol'] == symbol:
                    for f in s['filters']:
                        if f['filterType'] == 'PRICE_FILTER':
                            tick_size = float(f['tickSize'])
                            price_precision = len(str(tick_size).rstrip('0').split('.')[-1])
                            self.safe_log("info", f"   Price precision: {price_precision} decimals", "")
                            break
                    break
            
            stop_loss_pct = signal.get('stop_loss_distance', self.config['stop_loss_percentage'])
            take_profit_pct = stop_loss_pct * signal['risk_reward_ratio']
            
            if side == 'BUY':
                stop_loss_price = round(entry_price * (1 - stop_loss_pct), price_precision)
                take_profit_price = round(entry_price * (1 + take_profit_pct), price_precision)
            else:
                stop_loss_price = round(entry_price * (1 + stop_loss_pct), price_precision)
                take_profit_price = round(entry_price * (1 - take_profit_pct), price_precision)
            
            self.safe_log("info", f"   Step 6: Placing STOP LOSS order...", "")
            self.safe_log("info", f"   SL Price: ${stop_loss_price:.4f} ({stop_loss_pct*100:.1f}% from entry)", "")
            
            # Place STOP LOSS order
            sl_side = 'SELL' if side == 'BUY' else 'BUY'
            sl_order = self.data_fetcher.client.futures_create_order(
                symbol=symbol,
                side=sl_side,
                type='STOP_MARKET',
                stopPrice=stop_loss_price,
                quantity=quantity,
                closePosition=True
            )
            
            self.safe_log("info", f"✅ STOP LOSS order placed! Order ID: {sl_order.get('orderId')}", "")
            
            self.safe_log("info", f"   Step 7: Placing TAKE PROFIT order...", "")
            self.safe_log("info", f"   TP Price: ${take_profit_price:.4f} ({take_profit_pct*100:.1f}% from entry)", "")
            
            # Place TAKE PROFIT order
            tp_order = self.data_fetcher.client.futures_create_order(
                symbol=symbol,
                side=sl_side,
                type='TAKE_PROFIT_MARKET',
                stopPrice=take_profit_price,
                quantity=quantity,
                closePosition=True
            )
            
            self.safe_log("info", f"✅ TAKE PROFIT order placed! Order ID: {tp_order.get('orderId')}", "")
            
            # Store position data
            trade_data = {
                'symbol': symbol,
                'interval': interval,
                'signal': signal,
                'size': position_size,
                'quantity': quantity,
                'entry_price': entry_price,
                'stop_loss': stop_loss_price,
                'take_profit': take_profit_price,
                'entry_time': datetime.now(),
                'status': 'active',
                'order_id': order['orderId'],
                'sl_order_id': sl_order['orderId'],
                'tp_order_id': tp_order['orderId']
            }
            
            self.active_positions[f"{symbol}_{interval}"] = trade_data
            self.trade_count += 1
            
            self.safe_log("info", "=" * 80, "")
            self.safe_log("info", 
                f"🎉 TRADE SUCCESSFULLY EXECUTED! 🎉", "💰")
            self.safe_log("info", 
                f"   {side} {symbol} {interval}", "")
            self.safe_log("info", 
                f"   Quantity: {quantity} @ ${entry_price:.4f}", "")
            self.safe_log("info", 
                f"   Stop Loss: ${stop_loss_price:.4f} | Take Profit: ${take_profit_price:.4f}", "")
            self.safe_log("info", 
                f"   Confidence: {signal['confidence']:.1%} | R/R: {signal['risk_reward_ratio']:.2f}", "")
            self.safe_log("info", 
                f"   Market Order ID: {order.get('orderId')}", "")
            self.safe_log("info", 
                f"   SL Order ID: {sl_order.get('orderId')}", "")
            self.safe_log("info", 
                f"   TP Order ID: {tp_order.get('orderId')}", "")
            self.safe_log("info", "=" * 80, "")
            
        except Exception as e:
            self.safe_log("error", "=" * 80, "")
            self.safe_log("error", f"❌ ERROR EXECUTING TRADE for {symbol}!", "❌")
            self.safe_log("error", f"   Error type: {type(e).__name__}", "")
            self.safe_log("error", f"   Error message: {str(e)}", "")
            import traceback
            self.safe_log("error", f"   Traceback: {traceback.format_exc()}", "")
            self.safe_log("error", "=" * 80, "")
    
    def calculate_position_size(self, signal: Dict) -> float:
        """Calculate position size based on risk management"""
        try:
            risk_amount = self.config['account_balance'] * self.config['risk_per_trade']
            
            # Get stop loss distance from signal
            stop_loss_distance = signal.get('stop_loss_distance', self.config['stop_loss_percentage'])
            
            # Prevent division by zero
            if stop_loss_distance <= 0:
                self.safe_log("warning", f"⚠️ Invalid stop loss distance: {stop_loss_distance}, using default 5%", "⚠️")
                stop_loss_distance = 0.05  # Default 5%
            
            # Calculate position size
            position_size = risk_amount / stop_loss_distance
            
            # Cap position size to reasonable limits
            max_position_size = self.config['account_balance'] * 0.1  # Max 10% of balance
            position_size = min(position_size, max_position_size)
            
            return position_size
            
        except Exception as e:
            self.safe_log("error", f"❌ Error calculating position size: {str(e)}", "❌")
            return 0
    
    def manage_positions(self):
        """Enhanced position management - check if positions are still open"""
        for position_id, position in list(self.active_positions.items()):
            try:
                symbol = position['symbol']
                
                # Check if position is still open on Binance
                positions = self.data_fetcher.client.futures_position_information(symbol=symbol)
                
                position_open = False
                for pos in positions:
                    if pos['symbol'] == symbol:
                        position_amt = float(pos['positionAmt'])
                        if abs(position_amt) > 0:
                            position_open = True
                            # Update unrealized PnL
                            unrealized_pnl = float(pos['unRealizedProfit'])
                            position['unrealized_pnl'] = unrealized_pnl
                        break
                
                # If position is closed, remove from tracking
                if not position_open:
                    self.safe_log("info", 
                        f"✅ Position closed by SL/TP: {symbol} "
                        f"P&L: ${position.get('unrealized_pnl', 0):.2f}", "💹")
                    del self.active_positions[position_id]
                    
            except Exception as e:
                self.safe_log("error", f"Error managing position {position_id}: {str(e)}", "❌")
    
    def close_position(self, position_id: str, reason: str):
        """Close a trading position"""
        try:
            position = self.active_positions.get(position_id)
            if not position:
                return
            
            # Simulate P&L calculation (demo)
            simulated_pnl = position['size'] * 0.01  # 1% gain (demo)
            self.daily_pnl += simulated_pnl
            
            # Remove from active positions
            del self.active_positions[position_id]
            
            self.safe_log("info", 
                f"POSITION CLOSED: {position['symbol']} {position['interval']} "
                f"P&L: ${simulated_pnl:.2f} "
                f"Reason: {reason}", "💹")
            
        except Exception as e:
            self.safe_log("error", f"Error closing position: {str(e)}", "❌")
    
    def log_enhanced_status(self):
        """Log enhanced bot status"""
        runtime = datetime.now() - self.start_time
        
        self.safe_log("info", 
            f"STATUS: {len(self.active_positions)} positions, "
            f"{self.trade_count} trades, "
            f"${self.daily_pnl:.2f} P&L, "
            f"Runtime: {str(runtime).split('.')[0]}", "📊")
    
    def shutdown(self):
        """Shutdown bot gracefully"""
        self.safe_log("info", "Shutting down Enhanced Elliott Wave Trading Bot...", "👋")
        
        # Close all positions (in live trading)
        for position_id in list(self.active_positions.keys()):
            self.close_position(position_id, "Bot shutdown")
        
        # Log final statistics
        runtime = datetime.now() - self.start_time
        self.safe_log("info", 
            f"FINAL STATS: {self.trade_count} trades, "
            f"${self.daily_pnl:.2f} total P&L, "
            f"Runtime: {str(runtime).split('.')[0]}", "📈")


def main():
    """Main function to run the enhanced bot"""
    # Load API credentials from environment variables
    API_KEY = os.getenv('BINANCE_API_KEY', '').strip().strip('"').strip("'")
    API_SECRET = os.getenv('BINANCE_API_SECRET', '').strip().strip('"').strip("'")
    USE_TESTNET = os.getenv('USE_TESTNET', 'true').lower() == 'true'
    
    # Validate API credentials
    if not API_KEY or not API_SECRET or API_KEY == "your_api_key_here":
        print("❌ ERROR: BINANCE_API_KEY and BINANCE_API_SECRET environment variables must be set!")
        print("Please set them in Railway or your .env file")
        return
    
    print("🚀 Enhanced Elliott Wave Trading Bot")
    print("=" * 50)
    print(f"✅ API Key loaded: {API_KEY[:10]}...{API_KEY[-10:]}")
    print(f"✅ Using Testnet: {USE_TESTNET}")
    print("=" * 50)
    
    # Create and start the enhanced bot
    bot = EnhancedElliottWaveTradingBot(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=USE_TESTNET,
        config_file="bot_config.json"
    )
    
    # Start trading
    bot.start_trading()


if __name__ == "__main__":
    main()