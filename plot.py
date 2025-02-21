import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Set USD to JPY conversion rate
USD_TO_JPY = 151  # Example rate, adjust as needed

# XRP
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=52&range=1D&convertId=2797
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=52&range=ALL&convertId=2797

# curl -H "Referer: https://coinmarketcap.com/" -H "platform: web" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15" -o chart-xrp.json https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=52&range=1D&convertId=2797

# TRON
# https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=1958&range=1D&convertId=2797

import requests
import json

# URL for CoinMarketCap XRP data
url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=52&range=1D&convertId=2797"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://coinmarketcap.com/currencies/xrp/"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Save JSON to file
    with open("xrp_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ XRP data saved to xrp_data.json")
else:
    print(f"❌ Failed to fetch data. Status code: {response.status_code}")
    print("Response:", response.text)

# Load JSON data
file_path = 'xrp_data.json'

with open(file_path, 'r') as f:
    data = json.load(f)

# Extract time-series data
timestamps = []
prices = []

for timestamp, values in data['data']['points'].items():
    dt = datetime.utcfromtimestamp(int(timestamp))
    price = values['v'][0]  # Assuming first value in 'v' is price
    timestamps.append(dt)
    prices.append(price)

# Convert USD prices to JPY
prices_jpy = [price * USD_TO_JPY for price in prices]

# Convert to numpy arrays for easier manipulation
timestamps = np.array(timestamps)
prices = np.array(prices_jpy)

# Calculate baseline (starting price)
baseline = prices[0]

# Plot the data
plt.figure(figsize=(12, 6))

# Green area (price above baseline)
plt.fill_between(timestamps, prices, baseline, where=(prices >= baseline), interpolate=True, color='green', alpha=0.3)

# Red area (price below baseline)
plt.fill_between(timestamps, prices, baseline, where=(prices < baseline), interpolate=True, color='red', alpha=0.3)

# Plot price line
plt.plot(timestamps, prices, color='black', linewidth=1.5, label='Price')

# Highlight the latest price
plt.scatter(timestamps[-1], prices[-1], color='green' if prices[-1] >= baseline else 'red', zorder=5)
plt.text(timestamps[-1], prices[-1], f"{prices[-1]:.2f}", fontsize=10, ha='left', va='bottom')

# Plot baseline
plt.axhline(baseline, color='gray', linestyle='--', linewidth=1)
plt.text(timestamps[0], baseline, f"{baseline:.4f}", color='gray', va='bottom')

# Chart details
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Price Chart with Green/Red Shading')
plt.grid(True)
plt.tight_layout()
plt.show()
