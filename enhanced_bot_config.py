"""
Enhanced Elliott Wave Trading Bot Configuration System
Allows easy adjustment of trading parameters without code changes
"""

import json
import os
from typing import Dict, List, Any

class BotConfig:
    """Enhanced configuration management for Elliott Wave Trading Bot"""
    
    def __init__(self, config_file: str = "bot_config.json"):
        self.config_file = config_file
        self.default_config = {
            # Trading symbols - popular crypto pairs (all available on Binance Futures)
            'symbols': [
                'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT', 
                'SOLUSDT', 'DOGEUSDT', 'ATOMUSDT', 'DOTUSDT', 
                'LINKUSDT', 'AVAXUSDT'
            ],
            
            # Timeframes for analysis
            'intervals': ['15m', '30m', '1h', '4h'],
            
            # Scanning and timing
            'scan_frequency': 300,  # seconds (5 minutes)
            'max_positions': 3,     # maximum concurrent positions
            
            # Risk management
            'risk_per_trade': 0.02,     # 2% risk per trade
            'account_balance': 100000,  # USDT balance for position sizing
            'max_daily_loss': 0.05,     # 5% max daily loss
            
            # Signal quality filters (ADJUSTABLE for more/less signals)
            'min_confidence': 0.45,     # 45% minimum confidence (was 60%)
            'min_risk_reward': 1.2,     # 1.2:1 minimum risk/reward (was 1.5:1)
            
            # Advanced settings
            'stop_loss_percentage': 0.02,   # 2% stop loss
            'take_profit_multiplier': 2.0,  # 2x risk for take profit
            'trailing_stop': True,          # Enable trailing stops
            'trailing_stop_percentage': 0.01, # 1% trailing stop
            
            # Market conditions
            'min_volume_24h': 10000000,     # $10M minimum 24h volume
            'max_spread_percentage': 0.001,  # 0.1% max bid-ask spread
            
            # Logging and notifications
            'log_level': 'INFO',
            'log_to_file': True,
            'console_output': True,
            'enable_alerts': False,
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create with defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with defaults (in case new options were added)
                config = self.default_config.copy()
                config.update(loaded_config)
                
                print(f"✅ Configuration loaded from {self.config_file}")
                return config
            else:
                print(f"⚙️ Creating default configuration: {self.config_file}")
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"❌ Error loading config: {e}. Using defaults.")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """Save current configuration to file"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f, indent=4)
            print(f"💾 Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save"""
        self.config[key] = value
        self.save_config()
        print(f"🔧 Updated {key} = {value}")
    
    def print_config(self) -> None:
        """Print current configuration in a readable format"""
        print("\n🔧 CURRENT BOT CONFIGURATION")
        print("=" * 50)
        
        print("\n📊 TRADING SYMBOLS:")
        for symbol in self.config['symbols']:
            print(f"   • {symbol}")
        
        print(f"\n⏰ TIMEFRAMES: {', '.join(self.config['intervals'])}")
        print(f"🔄 SCAN FREQUENCY: {self.config['scan_frequency']} seconds")
        print(f"📈 MAX POSITIONS: {self.config['max_positions']}")
        
        print(f"\n💰 RISK MANAGEMENT:")
        print(f"   • Risk per trade: {self.config['risk_per_trade']*100}%")
        print(f"   • Account balance: ${self.config['account_balance']:,}")
        print(f"   • Max daily loss: {self.config['max_daily_loss']*100}%")
        print(f"   • Stop loss: {self.config['stop_loss_percentage']*100}%")
        
        print(f"\n🎯 SIGNAL FILTERS:")
        print(f"   • Min confidence: {self.config['min_confidence']*100}%")
        print(f"   • Min risk/reward: {self.config['min_risk_reward']}:1")
        
        print(f"\n📊 MARKET CONDITIONS:")
        print(f"   • Min 24h volume: ${self.config['min_volume_24h']:,}")
        print(f"   • Max spread: {self.config['max_spread_percentage']*100}%")
        
        print("=" * 50)
    
    def create_aggressive_config(self) -> None:
        """Create more aggressive trading configuration"""
        aggressive_settings = {
            'min_confidence': 0.35,      # Lower confidence threshold
            'min_risk_reward': 1.0,      # Lower risk/reward requirement
            'max_positions': 5,          # More concurrent positions
            'risk_per_trade': 0.025,     # Slightly higher risk per trade
            'scan_frequency': 180,       # Scan every 3 minutes
        }
        
        for key, value in aggressive_settings.items():
            self.config[key] = value
        
        self.save_config()
        print("🚀 AGGRESSIVE CONFIGURATION ACTIVATED!")
        print("   • Lower signal quality thresholds")
        print("   • More frequent scanning")
        print("   • Higher position limits")
    
    def create_conservative_config(self) -> None:
        """Create more conservative trading configuration"""
        conservative_settings = {
            'min_confidence': 0.65,      # Higher confidence threshold
            'min_risk_reward': 2.0,      # Higher risk/reward requirement
            'max_positions': 2,          # Fewer concurrent positions
            'risk_per_trade': 0.015,     # Lower risk per trade
            'scan_frequency': 600,       # Scan every 10 minutes
        }
        
        for key, value in conservative_settings.items():
            self.config[key] = value
        
        self.save_config()
        print("🛡️ CONSERVATIVE CONFIGURATION ACTIVATED!")
        print("   • Higher signal quality thresholds")
        print("   • Lower risk per trade")
        print("   • Fewer concurrent positions")
    
    def add_symbol(self, symbol: str) -> None:
        """Add a new trading symbol"""
        if symbol not in self.config['symbols']:
            self.config['symbols'].append(symbol)
            self.save_config()
            print(f"➕ Added symbol: {symbol}")
        else:
            print(f"⚠️ Symbol {symbol} already exists")
    
    def remove_symbol(self, symbol: str) -> None:
        """Remove a trading symbol"""
        if symbol in self.config['symbols']:
            self.config['symbols'].remove(symbol)
            self.save_config()
            print(f"➖ Removed symbol: {symbol}")
        else:
            print(f"⚠️ Symbol {symbol} not found")
    
    def add_timeframe(self, timeframe: str) -> None:
        """Add a new timeframe"""
        if timeframe not in self.config['intervals']:
            self.config['intervals'].append(timeframe)
            self.save_config()
            print(f"➕ Added timeframe: {timeframe}")
        else:
            print(f"⚠️ Timeframe {timeframe} already exists")


def main():
    """Demo of configuration system"""
    print("🔧 Elliott Wave Trading Bot - Enhanced Configuration System")
    print("=" * 60)
    
    # Create config manager
    config = BotConfig()
    
    # Display current configuration
    config.print_config()
    
    print("\n💡 QUICK CONFIGURATION OPTIONS:")
    print("   1. Current settings are BALANCED for more signals")
    print("   2. Use config.create_aggressive_config() for maximum signals")
    print("   3. Use config.create_conservative_config() for quality over quantity")
    
    print(f"\n📁 Configuration file: {config.config_file}")
    print("   Edit this file directly or use the methods above")
    
    return config


if __name__ == "__main__":
    config = main()