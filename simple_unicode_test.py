"""
Simple Unicode logging test
"""

import logging
import sys

def test_unicode_logging():
    """Test Unicode logging with different approaches"""
    
    print("Testing Unicode logging approaches...")
    print(f"System encoding: {sys.stdout.encoding}")
    
    # Test 1: Basic logging setup
    try:
        # Create file handler with UTF-8 encoding
        file_handler = logging.FileHandler('test_unicode.log', encoding='utf-8')
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Set formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Configure logger
        logger = logging.getLogger('test_logger')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        print("\n✅ Logging setup successful")
        
        # Test emoji logging
        test_messages = [
            ("🔍", "Scanning markets for Elliott Wave patterns..."),
            ("📊", "Bot Status: Active"),
            ("📈", "Executing LONG trade for BTCUSDT"),
            ("🚀", "Starting Elliott Wave Trading Bot..."),
            ("⏹️", "Bot stopped by user"),
            ("🛑", "Elliott Wave Trading Bot stopped")
        ]
        
        print("\nTesting emoji logging:")
        for emoji, message in test_messages:
            try:
                full_message = f"{emoji} {message}"
                logger.info(full_message)
                print(f"✅ {emoji} - Message logged successfully")
            except Exception as e:
                print(f"❌ {emoji} - Error: {e}")
                # Fallback without emoji
                logger.info(message)
                print(f"✅ Fallback logged: {message}")
        
        print(f"\n✅ Test completed! Check test_unicode.log for results")
        
    except Exception as e:
        print(f"❌ Logging setup failed: {e}")

if __name__ == "__main__":
    test_unicode_logging()