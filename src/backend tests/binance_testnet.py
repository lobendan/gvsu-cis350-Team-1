import requests
import hmac
import hashlib
import time

# Replace with your API key and secret
API_KEY = '1add414e04f307ee931e2e40a3a4adaa25db71723c92bead016114315b276852'
API_SECRET = 'c5d9c194c3ec2856427824be79b8d0f8f1d98deb5e67810a8e00108b46fda05e'
BASE_URL = 'https://testnet.binancefuture.com'


def create_signature(query_string):
    """Create HMAC SHA256 signature."""
    return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def get_account_info():
    """Retrieve account information."""
    endpoint = '/fapi/v2/account'
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = create_signature(query_string)
    url = f'{BASE_URL}{endpoint}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json()


def set_leverage(symbol, leverage):
    """Set leverage for a specific trading pair."""
    endpoint = '/fapi/v1/leverage'
    timestamp = int(time.time() * 1000)

    query_string = f'symbol={symbol}&leverage={leverage}&timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f'{BASE_URL}{endpoint}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers)
    return response.json()


def place_market_order(symbol, side, quantity):
    """Place a market order to open a trade."""
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)

    query_string = f'symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f'{BASE_URL}{endpoint}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers)
    return response.json()


def close_market_order(symbol, side, quantity):
    """Close a trade by placing a market order in the opposite direction."""
    return place_market_order(symbol, side, quantity)


def open_short_position(symbol, quantity):
    """Open a short position by placing a market sell order."""
    return place_market_order(symbol, 'SELL', quantity)


def get_order_status(symbol, order_id):
    """Check the status of a specific order."""
    endpoint = '/fapi/v1/order'
    timestamp = int(time.time() * 1000)

    query_string = f'symbol={symbol}&orderId={order_id}&timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f'{BASE_URL}{endpoint}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json()


# Example usage
if __name__ == '__main__':
    # Retrieve account information
    account_info = get_account_info()
    print("Account Info:", account_info)

    # Set leverage for the trading pair
    symbol = 'BTCUSDT'
    leverage = 20  # Adjust leverage as needed
    leverage_response = set_leverage(symbol, leverage)
    print("Set Leverage Response:", leverage_response)

    # Open a short position
    quantity = .01  # Adjust quantity as needed
    open_short_trade = open_short_position(symbol, quantity)
    print("Open Short Trade Response:", open_short_trade)

    # Close the short position (buy back)
    close_short_trade = close_market_order(symbol, 'BUY', quantity)
    print("Close Short Trade Response:", close_short_trade)

    # Check the status of the order
    if 'orderId' in open_short_trade:
        order_status = get_order_status(symbol, open_short_trade['orderId'])
        print("Order Status:", order_status)
