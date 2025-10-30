"""
Binance Futures Data Fetcher for Elliott Wave Analysis
=====================================================

This module fetches real-time futures data from Binance and formats it
for use with the Elliott Wave Analyzer.
"""

import pandas as pd
import numpy as np
from binance.client import Client
import ccxt
from datetime import datetime, timedelta
import time


class BinanceDataFetcher:
    """
    Fetches real-time and historical data from Binance Futures
    """
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize Binance client
        
        Args:
            api_key: Binance API key (optional for public data)
            api_secret: Binance API secret (optional for public data)
            testnet: Use testnet for paper trading (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Initialize Binance client
        if api_key and api_secret:
            self.client = Client(api_key, api_secret, testnet=testnet)
        else:
            self.client = Client()  # Public client for market data
            
        # Initialize CCXT for additional functionality
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'sandbox': testnet,
            'enableRateLimit': True,
        })
        
        print(f"✅ Binance client initialized (Testnet: {testnet})")
    
    def get_futures_klines(self, symbol, interval='1h', limit=500):
        """
        Fetch futures kline/candlestick data
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Number of candles to fetch (max 1500)
            
        Returns:
            DataFrame with OHLCV data formatted for Elliott Wave Analyzer
        """
        try:
            print(f"📡 Fetching {symbol} {interval} data from Binance Futures...")
            
            # Fetch klines from Binance
            klines = self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Format for Elliott Wave Analyzer
            df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['Open'] = df['Open'].astype(float)
            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            df['Close'] = df['Close'].astype(float)
            df['Volume'] = df['Volume'].astype(float)
            
            # Select and reorder columns to match Elliott Wave Analyzer format
            result_df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            result_df['Date'] = result_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"✅ Successfully fetched {len(result_df)} candles")
            print(f"📊 Price range: ${result_df['Low'].min():.2f} - ${result_df['High'].max():.2f}")
            print(f"⏰ Time range: {result_df['Date'].iloc[0]} to {result_df['Date'].iloc[-1]}")
            
            return result_df
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Get current futures price for a symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            print(f"❌ Error getting current price: {e}")
            return None
    
    def get_popular_futures_pairs(self):
        """Get list of popular futures trading pairs"""
        try:
            exchange_info = self.client.futures_exchange_info()
            symbols = []
            
            for symbol_info in exchange_info['symbols']:
                if (symbol_info['status'] == 'TRADING' and 
                    symbol_info['contractType'] == 'PERPETUAL' and
                    symbol_info['quoteAsset'] == 'USDT'):
                    symbols.append(symbol_info['symbol'])
            
            # Return top liquid pairs
            popular_pairs = [
                'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT', 'XRPUSDT',
                'SOLUSDT', 'DOGEUSDT', 'DOTUSDT', 'AVAXUSDT', 'LINKUSDT'
            ]
            
            return [pair for pair in popular_pairs if pair in symbols]
            
        except Exception as e:
            print(f"❌ Error getting futures pairs: {e}")
            return ['BTCUSDT', 'ETHUSDT']  # Fallback
    
    def save_data_to_csv(self, df, symbol, interval):
        """Save fetched data to CSV file"""
        if df is not None:
            filename = f"data/{symbol}_{interval}_futures.csv"
            df.to_csv(filename, index=False)
            print(f"💾 Data saved to {filename}")
            return filename
        return None


# Demo usage
if __name__ == "__main__":
    print("=== BINANCE FUTURES DATA FETCHER DEMO ===\n")
    
    # Initialize data fetcher (no API keys needed for market data)
    fetcher = BinanceDataFetcher()
    
    # Get popular trading pairs
    pairs = fetcher.get_popular_futures_pairs()
    print(f"📈 Popular futures pairs: {pairs[:5]}...\n")
    
    # Fetch BTC futures data
    symbol = 'BTCUSDT'
    interval = '1h'
    
    df = fetcher.get_futures_klines(symbol, interval, limit=200)
    
    if df is not None:
        print(f"\n📊 Sample data for {symbol}:")
        print(df.head())
        
        # Save to CSV
        filename = fetcher.save_data_to_csv(df, symbol, interval)
        
        print(f"\n✅ Ready for Elliott Wave Analysis!")
        print(f"   Use this file: {filename}")