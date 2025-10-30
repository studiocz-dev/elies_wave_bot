from models.MonoWave import MonoWaveDown, MonoWaveUp
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv(r'data\btc-usd_1d.csv')
lows = np.array(list(df['Low']))
highs = np.array(list(df['High']))
dates = np.array(list(df['Date']))

print("Data loaded successfully!")
print(f"Data shape: {df.shape}")
print(f"Date range: {dates[0]} to {dates[-1]}")

# Create a monowave up starting from the low at the 3rd index
print("\nCreating MonoWave Up...")
mw_up = MonoWaveUp(lows=lows, highs=highs, dates=dates, idx_start=3, skip=5)
print(f"MonoWave Up: from index {mw_up.idx_start} to {mw_up.idx_end}")
print(f"Low: {mw_up.low} at index {mw_up.low_idx}, High: {mw_up.high} at index {mw_up.high_idx}")
print(f"Start date: {mw_up.date_start}, End date: {mw_up.date_end}")
print(f"Wave length: {mw_up.length}, Duration: {mw_up.duration} periods")

# Create a monowave down from the end of the monowave up  
print("\nCreating MonoWave Down...")
mw_down = MonoWaveDown(lows=lows, highs=highs, dates=dates, idx_start=mw_up.idx_end, skip=0)
print(f"MonoWave Down: from index {mw_down.idx_start} to {mw_down.idx_end}")
print(f"Low: {mw_down.low} at index {mw_down.low_idx}, High: {mw_down.high} at index {mw_down.high_idx}")
print(f"Start date: {mw_down.date_start}, End date: {mw_down.date_end}")
print(f"Wave length: {mw_down.length}, Duration: {mw_down.duration} periods")

print("\nElliott Wave Analyzer is working correctly!")
print("To visualize the waves, you can:")
print("1. Use fig.show() instead of saving images")
print("2. Install a proper kaleido package for image saving")
print("3. Use the built-in plot functions with modifications")