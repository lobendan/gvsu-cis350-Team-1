import time
from binance.client import Client

# Get API credentials from the user
API_KEY = input("Enter your Binance API Key: ")
API_SECRET = input("Enter your Binance API Secret: ")

# Initialize the Binance client
client = Client(API_KEY, API_SECRET, tld='us')

# Get the cryptocurrency pair to track
symbol = 'BTCUSDC'
try:
    # Continuously fetch the price every second
    while True:
        # Fetch the latest price
        ticker = client.get_symbol_ticker(symbol=symbol)
        print(f"The latest price for {symbol} is {ticker['price']}")

        # Wait for 1 second before fetching again
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by the user.")
except Exception as e:
    print(f"Error: {e}")

