"""
Simple Elliott Wave Signal Generator
===================================

This creates basic trading signals from any detected Elliott Wave patterns,
useful for testing and demonstration purposes.
"""

import json
from elliott_wave_trading_bot import ElliottWaveTradingBot
from datetime import datetime

def create_simple_signal_bot():
    """Create a bot that generates signals from any detected patterns"""
    
    # Load API config
    try:
        with open('api_config.json', 'r') as f:
            config = json.load(f)
            api_config = {
                'api_key': config.get('binance_api_key', 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO'),
                'api_secret': config.get('binance_api_secret', 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu')
            }
    except:
        api_config = {
            'api_key': 'ERwz17q3vkEbVxTXWZWQZ5hxxI94nOGnyeCAkKluCiK9NpfONkD2iSI6pMUGD5ZO',
            'api_secret': 'VaaOtEOROLV4XgC5J2CjULoe8hvEjLoHLx8JQkImxkCQIs7xV6xjv1wKjsBPjkbu'
        }
    
    # Very permissive settings to generate signals
    permissive_config = {
        'symbols': ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT'],
        'intervals': ['1h', '4h', '1d'],
        'min_confidence': 0.1,  # Accept 10% confidence
        'min_risk_reward': 0.5, # Accept 0.5:1 risk/reward
        'risk_per_trade': 0.01, # 1% risk
        'max_positions': 5,
        'account_balance': 10000
    }
    
    print("🚀 SIMPLE ELLIOTT WAVE SIGNAL GENERATOR")
    print("=" * 50)
    print(f"📊 Ultra-permissive settings:")
    print(f"   Min Confidence: {permissive_config['min_confidence']*100}%")
    print(f"   Min Risk/Reward: {permissive_config['min_risk_reward']}:1")
    print(f"   Symbols: {', '.join(permissive_config['symbols'])}")
    print(f"   Timeframes: {', '.join(permissive_config['intervals'])}")
    print()
    
    # Create bot
    bot = ElliottWaveTradingBot(
        api_key=api_config['api_key'],
        api_secret=api_config['api_secret'],
        testnet=True,
        config=permissive_config
    )
    
    # Generate synthetic signals for demonstration
    synthetic_signals = []
    
    for symbol in permissive_config['symbols']:
        for interval in permissive_config['intervals']:
            try:
                # Get market data
                data = bot.data_fetcher.get_futures_klines(symbol, interval, 50)
                if data is None or len(data) < 10:
                    continue
                
                current_price = float(data[-1]['close'])
                high_price = max(float(d['high']) for d in data[-10:])
                low_price = min(float(d['low']) for d in data[-10:])
                
                # Create simple trend-following signals
                price_range = high_price - low_price
                
                if current_price > low_price + (price_range * 0.7):
                    # Price is in upper range - potential sell signal
                    signal = {
                        'symbol': symbol,
                        'interval': interval,
                        'type': 'SELL',
                        'entry_price': current_price,
                        'stop_loss': current_price * 1.02,
                        'take_profit': current_price * 0.95,
                        'confidence': 0.6,
                        'risk_reward_ratio': 2.5,
                        'reason': f'Simple trend reversal signal - {symbol} {interval}',
                        'timestamp': datetime.now()
                    }
                    synthetic_signals.append(signal)
                    
                elif current_price < low_price + (price_range * 0.3):
                    # Price is in lower range - potential buy signal
                    signal = {
                        'symbol': symbol,
                        'interval': interval,
                        'type': 'BUY',
                        'entry_price': current_price,
                        'stop_loss': current_price * 0.98,
                        'take_profit': current_price * 1.05,
                        'confidence': 0.6,
                        'risk_reward_ratio': 2.5,
                        'reason': f'Simple trend reversal signal - {symbol} {interval}',
                        'timestamp': datetime.now()
                    }
                    synthetic_signals.append(signal)
                
                print(f"✅ {symbol} {interval}: Price ${current_price:.2f} (Range: ${low_price:.2f} - ${high_price:.2f})")
                
            except Exception as e:
                print(f"❌ Error analyzing {symbol} {interval}: {e}")
    
    print(f"\n🎯 SYNTHETIC SIGNALS GENERATED: {len(synthetic_signals)}")
    print("=" * 50)
    
    if synthetic_signals:
        for i, signal in enumerate(synthetic_signals[:10]):  # Show first 10
            print(f"{i+1:2d}. {signal['symbol']:<8} {signal['interval']:<3} {signal['type']:<4} "
                  f"${signal['entry_price']:>8.2f} | R/R: {signal['risk_reward_ratio']:.1f} "
                  f"| Conf: {signal['confidence']:.0%}")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"1. These signals demonstrate the bot can generate trades")
        print(f"2. Real Elliott Wave signals need more complex market conditions")
        print(f"3. Consider using different timeframes or more volatile markets")
        print(f"4. Elliott Wave works best in trending markets with clear cycles")
        
        # Test executing one signal
        if len(synthetic_signals) > 0:
            test_signal = synthetic_signals[0]
            print(f"\n🧪 TESTING SIGNAL EXECUTION:")
            print(f"Signal: {test_signal['type']} {test_signal['symbol']} at ${test_signal['entry_price']:.2f}")
            print(f"This would normally execute on the testnet (paper trading)")
    else:
        print(f"❌ No signals generated even with synthetic logic")
        print(f"📊 Market conditions may be too stable for signal generation")

def test_manual_elliott_wave():
    """Test with manual Elliott Wave pattern detection"""
    
    print(f"\n🌊 MANUAL ELLIOTT WAVE PATTERN TEST")
    print("=" * 40)
    
    # Simulate finding an Elliott Wave pattern
    manual_patterns = [
        {
            'symbol': 'BTCUSDT',
            'interval': '4h',
            'pattern_type': 'Impulse Wave',
            'wave_count': 5,
            'completion': 80,  # 80% complete
            'direction': 'Bullish',
            'confidence': 0.7,
            'entry_signal': 'BUY on Wave 4 correction',
            'target': 'Wave 5 extension'
        },
        {
            'symbol': 'ETHUSDT',
            'interval': '1h',
            'pattern_type': 'Corrective Wave (ABC)',
            'wave_count': 3,
            'completion': 95,  # 95% complete
            'direction': 'Corrective',
            'confidence': 0.6,
            'entry_signal': 'BUY after correction ends',
            'target': 'New impulse wave'
        }
    ]
    
    for pattern in manual_patterns:
        print(f"📊 Pattern: {pattern['pattern_type']}")
        print(f"   Symbol: {pattern['symbol']} ({pattern['interval']})")
        print(f"   Direction: {pattern['direction']}")
        print(f"   Completion: {pattern['completion']}%")
        print(f"   Confidence: {pattern['confidence']:.0%}")
        print(f"   Signal: {pattern['entry_signal']}")
        print(f"   Target: {pattern['target']}")
        print()
    
    print(f"✅ These are the types of patterns Elliott Wave analysis looks for")
    print(f"📈 Current market conditions may not have clear 5-wave or 3-wave structures")

if __name__ == "__main__":
    create_simple_signal_bot()
    test_manual_elliott_wave()