"""
Elliott Wave Trading Bot - Manual Control Script
==============================================

This script allows you to manually control the Elliott Wave trading bot:
1. Run single market scans
2. Start continuous trading
3. Monitor performance
"""

from elliott_wave_trading_bot import ElliottWaveTradingBot
import time

def main():
    print("🤖 ELLIOTT WAVE TRADING BOT - CONTROL PANEL")
    print("=" * 60)
    
    # Initialize bot with testnet API credentials
    api_key = "ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO"
    api_secret = "VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu"
    
    # Enhanced trading configuration
    config = {
        'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT'],  # More symbols
        'intervals': ['1h', '4h'],                                # Multiple timeframes
        'scan_frequency': 60,                                     # Scan every 60 seconds
        'max_positions': 3,                                       # Max 3 concurrent positions
        'risk_per_trade': 0.01,                                  # 1% risk per trade
        'min_confidence': 0.6,                                   # 60% minimum confidence
        'min_risk_reward': 1.5,                                  # 1.5:1 minimum risk/reward
        'account_balance': 100000,                               # $100,000 testnet balance
    }
    
    # Initialize bot
    print("🔧 Initializing Elliott Wave Trading Bot...")
    bot = ElliottWaveTradingBot(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,  # Testnet mode
        config=config
    )
    
    print(f"\n✅ Bot initialized successfully!")
    print(f"📊 Account Balance: ${config['account_balance']:,}")
    print(f"🎯 Symbols: {', '.join(config['symbols'])}")
    print(f"⏰ Timeframes: {', '.join(config['intervals'])}")
    print(f"🛡️ Risk per trade: {config['risk_per_trade']*100}%")
    
    while True:
        print("\n" + "="*60)
        print("🎮 TRADING BOT CONTROL MENU")
        print("="*60)
        print("1. 🔍 Run Single Market Scan")
        print("2. 🚀 Start Continuous Trading Bot")
        print("3. 📊 Show Current Status")
        print("4. 📈 Show Performance Report")
        print("5. ⚙️ Modify Settings")
        print("6. ❌ Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            run_market_scan(bot)
        elif choice == "2":
            start_continuous_trading(bot)
        elif choice == "3":
            show_status(bot)
        elif choice == "4":
            show_performance_report(bot)
        elif choice == "5":
            modify_settings(bot)
        elif choice == "6":
            print("👋 Exiting Elliott Wave Trading Bot...")
            break
        else:
            print("❌ Invalid option. Please select 1-6.")

def run_market_scan(bot):
    """Run a single comprehensive market scan"""
    print("\n🔍 RUNNING COMPREHENSIVE MARKET SCAN")
    print("-" * 50)
    
    try:
        # Run enhanced market scan
        all_signals = []
        
        for symbol in bot.config['symbols']:
            for interval in bot.config['intervals']:
                print(f"\n📊 Analyzing {symbol} on {interval} timeframe...")
                
                # Get analysis
                analysis = bot.trading_system.analyze_symbol(symbol, interval, 200)
                
                if analysis and analysis['signals']:
                    # Filter signals by bot's criteria
                    valid_signals = [
                        s for s in analysis['signals']
                        if s['confidence'] >= bot.config['min_confidence']
                        and s['risk_reward_ratio'] >= bot.config['min_risk_reward']
                    ]
                    
                    for signal in valid_signals:
                        signal['timeframe'] = interval
                        all_signals.append(signal)
                        
                        print(f"   🎯 {signal['type']} Signal Found!")
                        print(f"      Entry: ${signal['entry_price']:.2f}")
                        print(f"      Stop Loss: ${signal['stop_loss']:.2f}")
                        print(f"      Take Profit: ${signal['take_profit_1']:.2f}")
                        print(f"      Risk/Reward: {signal['risk_reward_ratio']:.2f}")
                        print(f"      Confidence: {signal['confidence']:.1%}")
                else:
                    print(f"   ❌ No valid signals found for {symbol} {interval}")
                
                time.sleep(1)  # Rate limiting
        
        # Summary
        print(f"\n📋 SCAN SUMMARY")
        print("-" * 30)
        print(f"Total signals found: {len(all_signals)}")
        
        if all_signals:
            # Sort by confidence
            all_signals.sort(key=lambda x: x['confidence'], reverse=True)
            
            print(f"\n🏆 TOP TRADING OPPORTUNITIES:")
            print(f"{'Rank':<5} {'Symbol':<10} {'Type':<5} {'Timeframe':<10} {'Confidence':<12} {'R/R':<6}")
            print("-" * 60)
            
            for i, signal in enumerate(all_signals[:5], 1):
                print(f"{i:<5} {signal['symbol']:<10} {signal['type']:<5} {signal['timeframe']:<10} "
                      f"{signal['confidence']:<12.1%} {signal['risk_reward_ratio']:<6.2f}")
        else:
            print("No trading opportunities found at this time.")
            print("💡 Try adjusting confidence or risk/reward thresholds.")
        
        input("\nPress Enter to continue...")
        
    except Exception as e:
        print(f"❌ Error during market scan: {e}")

def start_continuous_trading(bot):
    """Start continuous trading with user confirmation"""
    print("\n🚀 STARTING CONTINUOUS TRADING BOT")
    print("-" * 40)
    
    print("⚠️  IMPORTANT WARNINGS:")
    print("• This will start automated trading")
    print("• Bot will scan markets every 60 seconds")
    print("• Positions will be opened automatically")
    print("• This is TESTNET - no real money at risk")
    print("• Press Ctrl+C to stop the bot anytime")
    
    confirm = input("\n❓ Are you sure you want to start continuous trading? (yes/no): ").lower().strip()
    
    if confirm in ['yes', 'y']:
        print("\n🎯 Starting continuous trading bot...")
        print("🛑 Press Ctrl+C to stop at any time")
        print("-" * 50)
        
        try:
            # Start the trading bot
            bot.start_trading()
        except KeyboardInterrupt:
            print("\n⏹️ Trading bot stopped by user")
        except Exception as e:
            print(f"\n❌ Trading bot error: {e}")
    else:
        print("❌ Continuous trading cancelled")

def show_status(bot):
    """Show current bot status"""
    print("\n📊 CURRENT BOT STATUS")
    print("-" * 30)
    
    # Active positions
    print(f"Active Positions: {len(bot.active_positions)}")
    
    if bot.active_positions:
        print("\n🔄 ACTIVE POSITIONS:")
        print(f"{'Symbol':<10} {'Type':<5} {'Entry':<10} {'Current':<10} {'P&L':<10}")
        print("-" * 50)
        
        for symbol, position in bot.active_positions.items():
            current_price = bot.data_fetcher.get_current_price(symbol)
            if current_price:
                if position['type'] == 'BUY':
                    pnl = (current_price - position['entry_price']) * position['position_size']
                else:
                    pnl = (position['entry_price'] - current_price) * position['position_size']
                
                print(f"{symbol:<10} {position['type']:<5} ${position['entry_price']:<9.2f} "
                      f"${current_price:<9.2f} ${pnl:<9.2f}")
    
    # Account summary
    total_pnl = sum([p.get('pnl', 0) for p in bot.trade_history if p.get('pnl')])
    unrealized_pnl = sum([p.get('unrealized_pnl', 0) for p in bot.active_positions.values()])
    
    print(f"\n💰 ACCOUNT SUMMARY:")
    print(f"Account Balance: ${bot.config['account_balance']:,.2f}")
    print(f"Total Trades: {len(bot.trade_history)}")
    print(f"Realized P&L: ${total_pnl:.2f}")
    print(f"Unrealized P&L: ${unrealized_pnl:.2f}")
    
    input("\nPress Enter to continue...")

def show_performance_report(bot):
    """Show detailed performance report"""
    print("\n📈 PERFORMANCE REPORT")
    print("-" * 30)
    
    report = bot.get_performance_report()
    print(report)
    
    input("\nPress Enter to continue...")

def modify_settings(bot):
    """Modify bot settings"""
    print("\n⚙️ MODIFY BOT SETTINGS")
    print("-" * 25)
    
    print("Current settings:")
    for key, value in bot.config.items():
        print(f"  {key}: {value}")
    
    print("\nWhich setting would you like to modify?")
    print("1. Risk per trade")
    print("2. Minimum confidence")
    print("3. Minimum risk/reward ratio")
    print("4. Scan frequency")
    print("5. Back to main menu")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    try:
        if choice == "1":
            new_risk = float(input("Enter new risk per trade (0.01 = 1%): "))
            bot.config['risk_per_trade'] = new_risk
            print(f"✅ Risk per trade updated to {new_risk*100}%")
        elif choice == "2":
            new_confidence = float(input("Enter new minimum confidence (0.6 = 60%): "))
            bot.config['min_confidence'] = new_confidence
            print(f"✅ Minimum confidence updated to {new_confidence*100}%")
        elif choice == "3":
            new_rr = float(input("Enter new minimum risk/reward ratio: "))
            bot.config['min_risk_reward'] = new_rr
            print(f"✅ Minimum risk/reward ratio updated to {new_rr}")
        elif choice == "4":
            new_freq = int(input("Enter new scan frequency (seconds): "))
            bot.config['scan_frequency'] = new_freq
            print(f"✅ Scan frequency updated to {new_freq} seconds")
    except ValueError:
        print("❌ Invalid input. Settings not changed.")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()