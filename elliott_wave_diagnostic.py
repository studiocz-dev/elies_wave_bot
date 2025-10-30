"""
Elliott Wave Signal Diagnostic Tool
==================================

This tool helps diagnose why no trading signals are generated
by showing detailed pattern detection information.
"""

import json
from elliott_wave_trading_bot import ElliottWaveTradingBot
from elliott_wave_trading_system import ElliottWaveTradingSystem

def load_api_config():
    """Load API configuration"""
    try:
        with open('api_config.json', 'r') as f:
            config = json.load(f)
            return {
                'api_key': config.get('binance_api_key', 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO'),
                'api_secret': config.get('binance_api_secret', 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu')
            }
    except:
        return {
            'api_key': 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO',
            'api_secret': 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu'
        }

def analyze_with_lower_thresholds():
    """Test Elliott Wave analysis with more sensitive settings"""
    
    print("🔍 ELLIOTT WAVE SIGNAL DIAGNOSTIC")
    print("=" * 50)
    
    # Load API config
    api_config = load_api_config()
    
    # Create bot with more sensitive settings
    sensitive_config = {
        'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT'],
        'intervals': ['1h', '4h'],
        'min_confidence': 0.3,  # Lower threshold (30% instead of 60%)
        'min_risk_reward': 1.0, # Lower threshold (1:1 instead of 1.5:1)
        'risk_per_trade': 0.02,
        'max_positions': 3,
        'account_balance': 10000
    }
    
    bot = ElliottWaveTradingBot(
        api_key=api_config['api_key'],
        api_secret=api_config['api_secret'],
        testnet=True,
        config=sensitive_config
    )
    
    print(f"📊 Using sensitive settings:")
    print(f"   Min Confidence: {sensitive_config['min_confidence']*100}%")
    print(f"   Min Risk/Reward: {sensitive_config['min_risk_reward']}:1")
    print()
    
    # Analyze each symbol/timeframe combination
    all_signals = []
    total_patterns = 0
    
    for symbol in sensitive_config['symbols']:
        for interval in sensitive_config['intervals']:
            print(f"🔍 Analyzing {symbol} {interval}...")
            
            try:
                # Get detailed analysis
                analysis = bot.trading_system.analyze_symbol(symbol, interval, 200)
                
                if analysis:
                    patterns = analysis.get('patterns_found', 0)
                    signals = analysis.get('signals', [])
                    raw_signals = analysis.get('raw_signals', [])
                    
                    total_patterns += patterns
                    
                    print(f"   ✅ Patterns found: {patterns}")
                    print(f"   📊 Raw signals: {len(raw_signals) if raw_signals else 0}")
                    print(f"   🎯 Filtered signals: {len(signals)}")
                    
                    # Show raw signals (before filtering)
                    if raw_signals:
                        print(f"   📋 Raw signal details:")
                        for i, sig in enumerate(raw_signals[:3]):  # Show first 3
                            conf = sig.get('confidence', 0)
                            rr = sig.get('risk_reward_ratio', 0)
                            print(f"      Signal {i+1}: {sig.get('type', 'N/A')} - Conf: {conf:.1%}, R/R: {rr:.2f}")
                    
                    # Add filtered signals to our collection
                    all_signals.extend(signals)
                    
                else:
                    print(f"   ❌ No analysis data")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()
    
    # Summary
    print("=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    print(f"Total patterns detected: {total_patterns}")
    print(f"Total signals generated: {len(all_signals)}")
    
    if all_signals:
        print(f"\n🎯 TRADING SIGNALS FOUND:")
        for i, signal in enumerate(all_signals[:5]):  # Show first 5
            print(f"  {i+1}. {signal['symbol']} {signal['type']} - "
                  f"Conf: {signal['confidence']:.1%}, R/R: {signal['risk_reward_ratio']:.2f}")
    else:
        print(f"\n💤 No signals found even with relaxed criteria")
        print(f"🔍 Possible reasons:")
        print(f"   - Markets are in strong trend (no clear 5-wave patterns)")
        print(f"   - Current timeframes don't show complete Elliott Wave cycles")
        print(f"   - Wave patterns are too complex/irregular for detection")
        print(f"   - More historical data might be needed")

def test_different_timeframes():
    """Test analysis with different timeframes"""
    
    print("\n🕐 TESTING DIFFERENT TIMEFRAMES")
    print("=" * 40)
    
    api_config = load_api_config()
    trading_system = ElliottWaveTradingSystem(
        api_key=api_config['api_key'],
        api_secret=api_config['api_secret'],
        testnet=True
    )
    
    # Test multiple timeframes
    timeframes = ['15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d']
    symbol = 'BTCUSDT'
    
    for tf in timeframes:
        try:
            print(f"🔍 Testing {symbol} {tf}...")
            analysis = trading_system.analyze_symbol(symbol, tf, 100)
            
            if analysis:
                patterns = analysis.get('patterns_found', 0)
                signals = len(analysis.get('signals', []))
                print(f"   Patterns: {patterns}, Signals: {signals}")
            else:
                print(f"   No data")
                
        except Exception as e:
            print(f"   Error: {str(e)}")

if __name__ == "__main__":
    analyze_with_lower_thresholds()
    test_different_timeframes()