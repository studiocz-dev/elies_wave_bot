"""
Enhanced Trading Control Panel with Unicode Support
==================================================

This version addresses Windows PowerShell Unicode encoding issues
and provides better error handling for console output.
"""

import os
import sys
import json
import time
from datetime import datetime
from elliott_wave_trading_bot import ElliottWaveTradingBot

# Set console encoding for Windows
if sys.platform == "win32":
    try:
        # Try to set console to UTF-8 mode
        os.system("chcp 65001 > nul 2>&1")
    except:
        pass

def safe_print(message, emoji=""):
    """Safe print function that handles Unicode encoding issues"""
    try:
        if emoji:
            print(f"{emoji} {message}")
        else:
            print(message)
    except UnicodeEncodeError:
        # Fallback without emoji
        print(message)

def load_api_config():
    """Load API configuration from file"""
    try:
        with open('api_config.json', 'r') as f:
            config = json.load(f)
            # Map the actual keys to expected keys
            return {
                'api_key': config.get('binance_api_key', 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO'),
                'api_secret': config.get('binance_api_secret', 'YZjsNhQpjsxGZVq5q2VKbvzEdOCGzCCH9gFbP9n2m3hkNP6LqNlWNvuBN1JN9Qf3')
            }
    except FileNotFoundError:
        safe_print("No API config found. Using default testnet credentials.", "⚠️")
        return {
            'api_key': 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO',
            'api_secret': 'YZjsNhQpjsxGZVq5q2VKbvzEdOCGzCCH9gFbP9n2m3hkNP6LqNlWNvuBN1JN9Qf3'
        }

def print_header():
    """Print the control panel header"""
    safe_print("=" * 60)
    safe_print("ENHANCED ELLIOTT WAVE TRADING CONTROL PANEL", "🎮")
    safe_print("=" * 60)

def print_menu():
    """Print the main menu options"""
    options = [
        ("1", "🔍", "Run Single Market Scan"),
        ("2", "🚀", "Start Continuous Trading Bot"),
        ("3", "📊", "Show Current Status"),
        ("4", "📈", "Show Performance Report"),
        ("5", "⚙️", "Modify Settings"),
        ("6", "❌", "Exit")
    ]
    
    for num, emoji, desc in options:
        safe_print(f"{num}. {desc}", emoji)

def run_market_scan(bot):
    """Execute a single market scan"""
    safe_print("Initiating market scan across all configured symbols...", "🔍")
    safe_print("-" * 50)
    
    try:
        # Get current configuration
        symbols = bot.config['symbols']
        intervals = bot.config['intervals']
        
        total_patterns = 0
        total_signals = 0
        scan_results = []
        
        for symbol in symbols:
            for interval in intervals:
                safe_print(f"Analyzing {symbol} on {interval} timeframe...", "🔍")
                
                try:
                    # Analyze the symbol
                    analysis = bot.trading_system.analyze_symbol(symbol, interval, 200)
                    
                    if analysis:
                        patterns_found = analysis.get('patterns_found', 0)
                        signals_found = len(analysis.get('signals', []))
                        total_patterns += patterns_found
                        total_signals += signals_found
                        
                        scan_results.append({
                            'symbol': symbol,
                            'interval': interval,
                            'patterns': patterns_found,
                            'signals': signals_found,
                            'analysis': analysis
                        })
                        
                        safe_print(f"Analysis complete: {patterns_found} patterns, {signals_found} signals", "✅")
                    else:
                        safe_print(f"No analysis data available for {symbol} {interval}", "⚠️")
                        
                except Exception as e:
                    safe_print(f"Error analyzing {symbol} {interval}: {str(e)}", "❌")
        
        # Print summary
        safe_print("\n" + "=" * 50)
        safe_print("MARKET SCAN SUMMARY", "📊")
        safe_print("=" * 50)
        safe_print(f"Total Patterns Found: {total_patterns}")
        safe_print(f"Total Trading Signals: {total_signals}")
        safe_print(f"Symbols Scanned: {len(symbols)}")
        safe_print(f"Timeframes: {', '.join(intervals)}")
        
        if total_signals > 0:
            safe_print(f"Ready to execute {total_signals} trading signals!", "🎯")
        else:
            safe_print("No trading signals found. Markets may be in consolidation.", "💤")
            
    except Exception as e:
        safe_print(f"Market scan failed: {str(e)}", "❌")

def start_continuous_trading(bot):
    """Start the continuous trading bot with safety checks"""
    safe_print("CONTINUOUS TRADING STARTUP", "🚀")
    safe_print("-" * 40)
    
    # Safety warnings
    safe_print("IMPORTANT SAFETY NOTICES:", "⚠️")
    safe_print("1. This is paper trading on Binance Testnet")
    safe_print("2. No real money will be used")
    safe_print("3. Press Ctrl+C to stop the bot at any time")
    safe_print("4. Monitor the bot's performance regularly")
    
    # Confirm start
    response = input("\nAre you sure you want to start continuous trading? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        safe_print("Starting continuous trading bot...", "🚀")
        safe_print("Bot is now scanning markets every 5 minutes")
        safe_print("Press Ctrl+C to stop")
        safe_print("-" * 50)
        
        try:
            bot.start_trading()
        except KeyboardInterrupt:
            safe_print("Trading stopped by user", "⏹️")
    else:
        safe_print("Continuous trading cancelled by user", "❌")

def show_status(bot):
    """Display current bot status"""
    safe_print("CURRENT BOT STATUS", "📊")
    safe_print("-" * 30)
    
    # Account info
    safe_print(f"Account Balance: $100,000.00 (Testnet)")
    safe_print(f"Active Positions: {len(bot.active_positions)}")
    safe_print(f"Total Trades: {len(bot.trade_history)}")
    
    # Calculate P&L
    total_pnl = sum(trade.get('pnl', 0) for trade in bot.trade_history)
    safe_print(f"Realized P&L: ${total_pnl:.2f}")
    
    # Bot state
    if bot.bot_running:
        safe_print("Bot Status: RUNNING", "🟢")
    else:
        safe_print("Bot Status: STOPPED", "🔴")
    
    safe_print(f"Last Scan: {bot.last_scan_time.strftime('%Y-%m-%d %H:%M:%S')}")

def show_performance_report(bot):
    """Display detailed performance report"""
    safe_print("PERFORMANCE REPORT", "📈")
    safe_print("-" * 40)
    
    if not bot.trade_history:
        safe_print("No trades executed yet", "💤")
        return
    
    # Trade statistics
    total_trades = len(bot.trade_history)
    winning_trades = sum(1 for trade in bot.trade_history if trade.get('pnl', 0) > 0)
    losing_trades = total_trades - winning_trades
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    safe_print(f"Total Trades: {total_trades}")
    safe_print(f"Winning Trades: {winning_trades}")
    safe_print(f"Losing Trades: {losing_trades}")
    safe_print(f"Win Rate: {win_rate:.1f}%")
    
    # P&L analysis
    total_pnl = sum(trade.get('pnl', 0) for trade in bot.trade_history)
    best_trade = max(bot.trade_history, key=lambda x: x.get('pnl', 0), default={})
    worst_trade = min(bot.trade_history, key=lambda x: x.get('pnl', 0), default={})
    
    safe_print(f"Total P&L: ${total_pnl:.2f}")
    if best_trade:
        safe_print(f"Best Trade: ${best_trade.get('pnl', 0):.2f}")
    if worst_trade:
        safe_print(f"Worst Trade: ${worst_trade.get('pnl', 0):.2f}")

def modify_settings(bot):
    """Allow user to modify bot settings"""
    safe_print("CURRENT SETTINGS", "⚙️")
    safe_print("-" * 30)
    
    for key, value in bot.config.items():
        safe_print(f"{key}: {value}")
    
    safe_print("\nSettings modification not implemented in this demo", "ℹ️")
    safe_print("You can modify settings in the bot configuration file")

def main():
    """Main control panel loop"""
    try:
        # Initialize bot
        api_config = load_api_config()
        bot = ElliottWaveTradingBot(
            api_key=api_config['api_key'],
            api_secret=api_config['api_secret'],
            testnet=True
        )
        
        safe_print("Elliott Wave Trading Bot initialized successfully!", "✅")
        
        while True:
            print("\n")
            print_header()
            print_menu()
            print()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                run_market_scan(bot)
            elif choice == '2':
                start_continuous_trading(bot)
            elif choice == '3':
                show_status(bot)
            elif choice == '4':
                show_performance_report(bot)
            elif choice == '5':
                modify_settings(bot)
            elif choice == '6':
                safe_print("Exiting Elliott Wave Trading Bot...", "👋")
                break
            else:
                safe_print("Invalid option. Please select 1-6.", "❌")
            
            input("\nPress Enter to continue...")
    
    except Exception as e:
        safe_print(f"Application error: {str(e)}", "❌")
        safe_print("Please check your configuration and try again")

if __name__ == "__main__":
    main()