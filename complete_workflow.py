"""
ELLIOTT WAVE ANALYZER - COMPLETE WORKFLOW
=========================================

This demonstrates the full algorithm from data input to pattern detection.
"""

import numpy as np
import pandas as pd
from models.WaveAnalyzer import WaveAnalyzer
from models.WaveOptions import WaveOptionsGenerator5
from models.WaveRules import Impulse
from models.WavePattern import WavePattern

print("=== ELLIOTT WAVE ANALYZER WORKFLOW ===\n")

# Step 1: Load Market Data
print("1. LOADING MARKET DATA")
df = pd.read_csv(r'data\btc-usd_1d.csv')
print(f"   - Loaded {len(df)} days of Bitcoin price data")
print(f"   - Date range: {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}")
print(f"   - Price range: ${df['Low'].min():,.0f} to ${df['High'].max():,.0f}")

# Step 2: Find Starting Point
idx_start = np.argmin(np.array(list(df['Low'])))
print(f"\n2. FINDING ANALYSIS STARTING POINT")
print(f"   - Starting from lowest price at index {idx_start}")
print(f"   - Date: {df['Date'].iloc[idx_start]}")
print(f"   - Price: ${df['Low'].iloc[idx_start]:,.2f}")

# Step 3: Generate Wave Options
print(f"\n3. GENERATING WAVE OPTION COMBINATIONS")
wave_options = WaveOptionsGenerator5(up_to=5)  # Smaller range for demo
print(f"   - Generating combinations up to [5,5,5,5,5]")
print(f"   - Total combinations: {wave_options.number:,}")
print(f"   - First few options: {[str(opt) for opt in list(wave_options.options_sorted)[:5]]}")

# Step 4: Set up Wave Analyzer and Rules
print(f"\n4. SETTING UP ANALYSIS ENGINE")
wa = WaveAnalyzer(df=df, verbose=False)
impulse_rule = Impulse('impulse')
print(f"   - Wave analyzer initialized")
print(f"   - Elliott Wave impulse rules loaded ({len(impulse_rule.conditions)} conditions)")

# Step 5: Search for Patterns
print(f"\n5. SEARCHING FOR ELLIOTT WAVE PATTERNS")
valid_patterns = []
tested_patterns = 0

for option in list(wave_options.options_sorted)[:10]:  # Test first 10 for demo
    tested_patterns += 1
    
    # Try to find 5-wave impulse with this option
    waves = wa.find_impulsive_wave(idx_start=idx_start, wave_config=option.values)
    
    if waves:
        # Create wave pattern
        pattern = WavePattern(waves, verbose=False)
        
        # Validate against Elliott Wave rules
        if pattern.check_rule(impulse_rule):
            valid_patterns.append((option.values, pattern))
            print(f"   ✓ VALID IMPULSE FOUND: {option.values}")

# Step 6: Results Summary
print(f"\n6. ANALYSIS RESULTS")
print(f"   - Tested {tested_patterns} wave option combinations")
print(f"   - Found {len(valid_patterns)} valid Elliott Wave impulse patterns")

if valid_patterns:
    print(f"\n   VALID PATTERNS DETECTED:")
    for i, (option, pattern) in enumerate(valid_patterns):
        print(f"   Pattern {i+1}: {option}")
        print(f"     - Wave 1: ${pattern.waves['wave1'].low:,.0f} → ${pattern.waves['wave1'].high:,.0f}")
        print(f"     - Wave 2: ${pattern.waves['wave2'].high:,.0f} → ${pattern.waves['wave2'].low:,.0f}")
        print(f"     - Wave 3: ${pattern.waves['wave3'].low:,.0f} → ${pattern.waves['wave3'].high:,.0f}")
        print(f"     - Wave 4: ${pattern.waves['wave4'].high:,.0f} → ${pattern.waves['wave4'].low:,.0f}")
        print(f"     - Wave 5: ${pattern.waves['wave5'].low:,.0f} → ${pattern.waves['wave5'].high:,.0f}")
        print(f"     - Total move: ${pattern.waves['wave1'].low:,.0f} → ${pattern.waves['wave5'].high:,.0f}")
        print(f"     - Duration: {pattern.waves['wave1'].idx_start} to {pattern.waves['wave5'].idx_end} ({pattern.waves['wave5'].idx_end - pattern.waves['wave1'].idx_start} days)")

print(f"\n=== ALGORITHM SUMMARY ===")
print("1. Load OHLC price data")
print("2. Generate all possible skip combinations [i,j,k,l,m]")  
print("3. For each combination:")
print("   a. Find 5 alternating MonoWaves (Up-Down-Up-Down-Up)")
print("   b. Create WavePattern from the 5 MonoWaves")
print("   c. Validate against Elliott Wave rules")
print("   d. If valid, save as detected pattern")
print("4. Return all valid Elliott Wave patterns found")
print("\nThis brute-force approach tests MILLIONS of combinations")
print("to find patterns that comply with Elliott Wave theory!")