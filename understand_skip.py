import numpy as np
import pandas as pd
from models.MonoWave import MonoWaveUp

# Load the Bitcoin data
df = pd.read_csv(r'data\btc-usd_1d.csv')
lows = np.array(list(df['Low']))
highs = np.array(list(df['High']))
dates = np.array(list(df['Date']))

print("=== Understanding the SKIP Parameter ===\n")

# Start from a low point
start_idx = 3
print(f"Starting from index {start_idx}, date: {dates[start_idx]}")
print(f"Starting price (low): ${lows[start_idx]:,.2f}")

# Test different skip values
skip_values = [0, 2, 5, 10]

for skip in skip_values:
    print(f"\n--- Skip = {skip} ---")
    
    try:
        mw = MonoWaveUp(lows=lows, highs=highs, dates=dates, idx_start=start_idx, skip=skip)
        
        print(f"End index: {mw.idx_end}")
        print(f"End date: {mw.date_end}")
        print(f"End price (high): ${mw.high:,.2f}")
        print(f"Wave duration: {mw.duration} days")
        print(f"Price gain: ${mw.length:,.2f} ({(mw.length/mw.low)*100:.1f}%)")
        
    except Exception as e:
        print(f"No valid wave found with skip={skip}")

print(f"\n=== Key Insight ===")
print("Higher skip values find LONGER-TERM waves by ignoring smaller corrections.")
print("Lower skip values find SHORTER-TERM waves that end at the first correction.")
print("This allows the algorithm to analyze waves at multiple timeframes!")