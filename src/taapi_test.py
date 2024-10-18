import requests
import json
import time

TAurl = "https://api.taapi.io/bulk"

import requests

# Define the URL with your secret key
priceurl = "https://api.taapi.io/price"

# params for getting live price data
params = {
    "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjcxMTQzMmUwOTlhYTMwMjViNWRjMjgyIiwiaWF0IjoxNzI5MTg0NTU4LCJleHAiOjMzMjMzNjQ4NTU4fQ.RgqbtHeecIl1OhdWwfM-oKkW-xNnhAnCLvPN3cNMzIw",      
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "interval": "1h"
}



# payload for getting live indicator dat
payload = {
    "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjcwNTQ3YTEwOTlhYTMwMjViODBlOTdjIiwiaWF0IjoxNzI4Mzk5MjY1LCJleHAiOjMzMjMyODYzMjY1fQ.lU3WjVMVs5LS1ap8QN2IgxmqqxOlw87p3P0LtiME1j0",
    "construct": {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1h",
        "indicators": [
            {
                "indicator": "rsi"
            }, 
            {
                "indicator": "ema",
                "period": 20
            },
            {
                "indicator": "macd"
            }, 
            {
                "indicator": "sma",
                "period": 5
            },
            {
                "indicator": "sma",
                "period": 20
            }
        ]
    }
}
headers = {"Content-Type": "application/json"}




while(1):
    response_ta = requests.request("POST", TAurl, json=payload, headers=headers)

    # Make the GET request
    response_price = requests.get(priceurl, params=params)

    # Check the response status code
    if response_price.status_code == 200:
        # Parse the JSON data
        data = response_price.json()
        print("Current BTC/USDT Price:", data)
    else:
        print(f"Failed to retrieve data: {response_price.status_code}")

    json_str = response_ta.content.decode("utf-8")

    # Parse the string as JSON
    data_dict = json.loads(json_str)

    print("Binance BTC/USDT Indicators (1 min)\n")
    for item in data_dict['data']:

        indicator = item['indicator']
        result = item['result']
        errors = item['errors']
        indicator = item["indicator"].upper()
        id = item["id"]
        print(f"Indicator: {indicator}")
        
        if indicator == "RSI":
            print(f"  - Value: {item['result']['value']:.2f}")
        
        elif indicator == "EMA":
            print(f"  - Period: 20")
            print(f"  - Value: {item['result']['value']:.2f}")
        
        elif indicator == "MACD":
            print(f"  - MACD Value: {item['result']['valueMACD']:.2f}")
            print(f"  - MACD Signal: {item['result']['valueMACDSignal']:.2f}")
            print(f"  - MACD Histogram: {item['result']['valueMACDHist']:.2f}")
        
        elif id == "binance_BTC/USDT_1h_sma_5_0":
            print(f"  SMA(5) Value: {item['result']['value']:.2f}")

        elif id == "binance_BTC/USDT_1h_sma_20_0":
            print(f"  SMA(20) Value: {item['result']['value']:.2f}")
            time.sleep(15)
        print()
       
    