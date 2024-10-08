import requests
import json
import time

url = "https://api.taapi.io/bulk"

payload = {
    "secret": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjcwNTQ3YTEwOTlhYTMwMjViODBlOTdjIiwiaWF0IjoxNzI4Mzk5MjY1LCJleHAiOjMzMjMyODYzMjY1fQ.lU3WjVMVs5LS1ap8QN2IgxmqqxOlw87p3P0LtiME1j0",
    "construct": {
        "exchange": "binance",
        "symbol": "BTC/USDT",
        "interval": "1h",
        "indicators": [
            {
                "indicator": "rsi"
            }, {
                "indicator": "ema",
                "period": 20
            },
            {
                "indicator": "macd"
            }, 
            {
                "indicator": "kdj"
            }
        ]
    }
}
headers = {"Content-Type": "application/json"}


while(1):
    response = requests.request("POST", url, json=payload, headers=headers)

    json_str = response.content.decode("utf-8")

    # Parse the string as JSON
    data_dict = json.loads(json_str)

    print("Binance BTC/USDT Indicators (1 Hour)\n")
    for item in data_dict['data']:

        indicator = item['indicator']
        result = item['result']
        errors = item['errors']
        indicator = item["indicator"].upper()
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
        
        elif indicator == "KDJ":
            print(f"  - K Value: {item['result']['valueK']:.2f}")
            print(f"  - D Value: {item['result']['valueD']:.2f}")
            print(f"  - J Value: {item['result']['valueJ']:.2f}")
            time.sleep(15)
        print()
       
    