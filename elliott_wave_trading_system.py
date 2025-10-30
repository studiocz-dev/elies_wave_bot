"""
Elliott Wave Trading System for Binance Futures
==============================================

This system combines Elliott Wave analysis with Binance Futures trading
to generate automated trading signals and manage positions.
"""

import pandas as pd
import numpy as np
from binance_data_fetcher import BinanceDataFetcher
from models.WaveAnalyzer import WaveAnalyzer
from models.WaveOptions import WaveOptionsGenerator5
from models.WaveRules import Impulse, LeadingDiagonal
from models.WavePattern import WavePattern
from datetime import datetime
import time


class ElliottWaveTradingSystem:
    """
    Complete trading system using Elliott Wave analysis for Binance Futures
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize the trading system
        
        Args:
            api_key: Binance API key (required for trading)
            api_secret: Binance API secret (required for trading)
            testnet: Use testnet for paper trading
        """
        self.data_fetcher = BinanceDataFetcher(api_key, api_secret, testnet)
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Trading parameters
        self.risk_per_trade = 0.02  # 2% risk per trade
        self.max_skip_value = 10    # Maximum skip value for wave detection
        self.min_wave_duration = 5  # Minimum wave duration in periods
        
        # Trading state
        self.active_signals = {}
        self.trade_history = []
        
        print("🤖 Elliott Wave Trading System initialized")
        print(f"📊 Risk per trade: {self.risk_per_trade*100}%")
        print(f"🌊 Max skip value: {self.max_skip_value}")
    
    def analyze_symbol(self, symbol, interval='1h', lookback=200):
        """
        Perform Elliott Wave analysis on a trading pair
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Timeframe for analysis
            lookback: Number of candles to analyze
            
        Returns:
            Dictionary with analysis results and trading signals
        """
        print(f"\n🔍 Analyzing {symbol} on {interval} timeframe...")
        
        # Fetch data
        df = self.data_fetcher.get_futures_klines(symbol, interval, lookback)
        if df is None:
            return None
        
        # Initialize wave analyzer
        wa = WaveAnalyzer(df=df, verbose=False)
        
        # Generate wave options
        wave_options = WaveOptionsGenerator5(up_to=self.max_skip_value)
        
        # Set up Elliott Wave rules
        impulse_rule = Impulse('impulse')
        diagonal_rule = LeadingDiagonal('leading_diagonal')
        rules = [impulse_rule, diagonal_rule]
        
        # Find analysis starting points (recent lows and highs)
        lows = np.array(df['Low'])
        highs = np.array(df['High'])
        
        # Look for patterns in the last 80% of data
        start_range = int(len(df) * 0.2)
        end_range = int(len(df) * 0.8)
        
        analysis_results = {
            'symbol': symbol,
            'interval': interval,
            'current_price': float(df['Close'].iloc[-1]),
            'timestamp': datetime.now(),
            'bullish_patterns': [],
            'bearish_patterns': [],
            'signals': []
        }
        
        print(f"🔍 Searching for Elliott Wave patterns...")
        patterns_found = 0
        
        # Search for patterns from multiple starting points
        for start_idx in range(start_range, end_range, 10):
            
            # Look for bullish impulse waves (starting from lows)
            for option in list(wave_options.options_sorted)[:50]:  # Limit search for performance
                
                waves = wa.find_impulsive_wave(idx_start=start_idx, wave_config=option.values)
                
                if waves and len(waves) == 5:
                    pattern = WavePattern(waves, verbose=False)
                    
                    # Check if pattern satisfies Elliott Wave rules
                    for rule in rules:
                        if pattern.check_rule(rule):
                            patterns_found += 1
                            
                            # Analyze pattern for trading signals
                            signal = self._analyze_pattern_for_signals(pattern, df, symbol, rule.name)
                            if signal:
                                analysis_results['bullish_patterns'].append({
                                    'start_idx': start_idx,
                                    'wave_config': option.values,
                                    'rule': rule.name,
                                    'pattern': pattern,
                                    'confidence': self._calculate_pattern_confidence(pattern)
                                })
                                analysis_results['signals'].append(signal)
            
            # Limit computation time
            if patterns_found > 10:
                break
        
        print(f"✅ Analysis complete: {patterns_found} patterns found")
        print(f"📈 Bullish patterns: {len(analysis_results['bullish_patterns'])}")
        print(f"🎯 Trading signals: {len(analysis_results['signals'])}")
        
        return analysis_results
    
    def _analyze_pattern_for_signals(self, pattern, df, symbol, rule_name):
        """
        Analyze an Elliott Wave pattern to generate trading signals
        """
        waves = pattern.waves
        current_price = float(df['Close'].iloc[-1])
        
        # Get the last wave (wave 5) details
        wave5 = waves['wave5']
        wave4 = waves['wave4']
        wave3 = waves['wave3']
        wave1 = waves['wave1']
        
        # Determine pattern completion status
        wave5_end_idx = wave5.idx_end
        total_candles = len(df)
        
        # Signal generation logic
        signal = None
        
        # Pattern recently completed (within last 5 candles)
        if total_candles - wave5_end_idx <= 5:
            
            # Check if Wave 5 extended beyond Wave 3 (bullish completion)
            if wave5.high > wave3.high:
                
                # Calculate key levels
                pattern_low = wave1.low
                pattern_high = wave5.high
                wave4_low = wave4.low
                
                # Generate SELL signal (pattern completion, expect correction)
                signal = {
                    'type': 'SELL',
                    'symbol': symbol,
                    'rule': rule_name,
                    'entry_price': current_price,
                    'stop_loss': pattern_high * 1.02,  # 2% above pattern high
                    'take_profit_1': wave4_low,       # First target: Wave 4 low
                    'take_profit_2': pattern_low,     # Second target: Pattern start
                    'confidence': self._calculate_pattern_confidence(pattern),
                    'reason': f"Elliott Wave {rule_name} completion - expect ABC correction",
                    'risk_reward_ratio': self._calculate_risk_reward(current_price, pattern_high * 1.02, wave4_low)
                }
        
        # Pattern in Wave 4 correction (potential Wave 5 entry)
        elif wave4.idx_end <= total_candles - 1 <= wave5.idx_start + 2:
            
            # Check if in Wave 4 correction zone
            if wave4_low <= current_price <= wave3.high * 0.8:
                
                # Generate BUY signal (Wave 5 potential)
                signal = {
                    'type': 'BUY',
                    'symbol': symbol,
                    'rule': rule_name,
                    'entry_price': current_price,
                    'stop_loss': wave4_low * 0.98,    # 2% below Wave 4 low
                    'take_profit_1': wave3.high,      # First target: Wave 3 high
                    'take_profit_2': wave3.high * 1.1, # Second target: 110% of Wave 3
                    'confidence': self._calculate_pattern_confidence(pattern),
                    'reason': f"Elliott Wave {rule_name} Wave 4 correction - expect Wave 5",
                    'risk_reward_ratio': self._calculate_risk_reward(current_price, wave4_low * 0.98, wave3.high)
                }
        
        return signal
    
    def _calculate_pattern_confidence(self, pattern):
        """
        Calculate confidence score for an Elliott Wave pattern (0-1)
        """
        waves = pattern.waves
        
        # Base confidence
        confidence = 0.5
        
        # Check Wave 3 extension (strongest wave)
        wave1_length = waves['wave1'].length
        wave3_length = waves['wave3'].length
        wave5_length = waves['wave5'].length
        
        # Wave 3 should be strongest or second strongest
        if wave3_length >= max(wave1_length, wave5_length):
            confidence += 0.2
        
        # Check Fibonacci relationships
        wave2_retrace = waves['wave2'].length / wave1_length
        if 0.38 <= wave2_retrace <= 0.618:  # Fibonacci retracement
            confidence += 0.15
        
        wave4_retrace = waves['wave4'].length / wave3_length
        if 0.25 <= wave4_retrace <= 0.5:    # Shallow Wave 4
            confidence += 0.15
        
        # Duration proportions
        total_duration = waves['wave5'].idx_end - waves['wave1'].idx_start
        if total_duration >= self.min_wave_duration:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_risk_reward(self, entry_price, stop_loss, take_profit):
        """Calculate risk-to-reward ratio"""
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        
        if risk > 0:
            return reward / risk
        return 0
    
    def get_position_size(self, symbol, entry_price, stop_loss, account_balance=10000):
        """
        Calculate position size based on risk management
        
        Args:
            symbol: Trading pair
            entry_price: Entry price
            stop_loss: Stop loss price
            account_balance: Available balance in USDT
            
        Returns:
            Position size in base currency
        """
        # Calculate risk per trade in USDT
        risk_amount = account_balance * self.risk_per_trade
        
        # Calculate distance to stop loss
        price_distance = abs(entry_price - stop_loss)
        
        # Calculate position size
        if price_distance > 0:
            position_size = risk_amount / price_distance
            return round(position_size, 6)
        
        return 0
    
    def scan_multiple_symbols(self, symbols=None, interval='1h'):
        """
        Scan multiple symbols for Elliott Wave trading opportunities
        """
        if symbols is None:
            symbols = self.data_fetcher.get_popular_futures_pairs()[:5]  # Top 5 pairs
        
        print(f"\n🔎 Scanning {len(symbols)} symbols for trading opportunities...")
        
        all_signals = []
        
        for symbol in symbols:
            try:
                print(f"\n--- {symbol} ---")
                analysis = self.analyze_symbol(symbol, interval)
                
                if analysis and analysis['signals']:
                    all_signals.extend(analysis['signals'])
                    
                    for signal in analysis['signals']:
                        print(f"🎯 {signal['type']} signal for {symbol}")
                        print(f"   Entry: ${signal['entry_price']:.2f}")
                        print(f"   Stop Loss: ${signal['stop_loss']:.2f}")
                        print(f"   Take Profit: ${signal['take_profit_1']:.2f}")
                        print(f"   Risk/Reward: {signal['risk_reward_ratio']:.2f}")
                        print(f"   Confidence: {signal['confidence']:.1%}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")
        
        # Sort signals by confidence
        all_signals.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"\n📋 TRADING OPPORTUNITIES SUMMARY")
        print(f"{'Symbol':<12} {'Type':<6} {'Entry':<10} {'R/R':<6} {'Confidence':<10}")
        print("-" * 60)
        
        for signal in all_signals[:10]:  # Top 10 signals
            print(f"{signal['symbol']:<12} {signal['type']:<6} ${signal['entry_price']:<9.2f} "
                  f"{signal['risk_reward_ratio']:<6.2f} {signal['confidence']:<10.1%}")
        
        return all_signals


# Demo Usage
if __name__ == "__main__":
    print("=== ELLIOTT WAVE TRADING SYSTEM DEMO ===\n")
    
    # Initialize trading system (paper trading mode)
    trading_system = ElliottWaveTradingSystem(testnet=True)
    
    # Analyze single symbol
    print("🔍 Single Symbol Analysis:")
    btc_analysis = trading_system.analyze_symbol('BTCUSDT', '1h', 150)
    
    print("\n" + "="*60)
    
    # Scan multiple symbols
    print("🔍 Multi-Symbol Scan:")
    signals = trading_system.scan_multiple_symbols(['BTCUSDT', 'ETHUSDT'], '1h')
    
    print(f"\n✅ Analysis complete!")
    print(f"💡 Found {len(signals)} trading opportunities")
    print(f"🚀 Ready for live trading implementation!")