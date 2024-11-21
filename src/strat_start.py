#-----------------------------------------------------------------------
#This is used as the starting class, which is used to call other classes
#-----------------------------------------------------------------------

import requests
import json
from dataclasses import dataclass

TAurl = "https://api.taapi.io/bulk"
priceurl = "https://api.taapi.io/price"

# Define the dataclass to store indicator values
@dataclass
class IndicatorData:
    rsi: float = None
    ema: float = None
    macd_value: float = None
    macd_signal: float = None
    macd_hist: float = None
    sma_5: float = None
    sma_20: float = None
    price: float = None


# Manager class to handle indicator data and updates
class IndicatorManager:
    def __init__(self, price_key, ti_key):
        self.indicator_data = IndicatorData()
        self.price_key = price_key
        self.ti_key = ti_key


    def update_price(self, price_data):
        self.indicator_data.price = price_data["value"]

    def update_indicators(self, data_dict):
        for item in data_dict['data']:
            indicator = item['indicator'].upper()
            id = item['id']

            if indicator == "RSI":
                self.indicator_data.rsi = item['result']['value']

            elif indicator == "EMA":
                self.indicator_data.ema = item['result']['value']

            elif indicator == "MACD":
                self.indicator_data.macd_value = item['result']['valueMACD']
                self.indicator_data.macd_signal = item['result']['valueMACDSignal']
                self.indicator_data.macd_hist = item['result']['valueMACDHist']


            #make sure to change the keys as well when the interval is changed in the payload
            elif id == "binance_BTC/USDT_1m_sma_5_0":
                self.indicator_data.sma_5 = item['result']['value']

            elif id == "binance_BTC/USDT_1m_sma_20_0":
                self.indicator_data.sma_20 = item['result']['value']

    #optional            
    def display_data(self):
        print(f"--- Indicator Data ---")
        print(f"Price: {self.indicator_data.price}")
        print(f"RSI: {self.indicator_data.rsi}")
        print(f"EMA(20): {self.indicator_data.ema}")
        print(f"MACD: Value={self.indicator_data.macd_value}, Signal={self.indicator_data.macd_signal}, Hist={self.indicator_data.macd_hist}")
        print(f"SMA(5): {self.indicator_data.sma_5}")
        print(f"SMA(20): {self.indicator_data.sma_20}")
        print("-----------------------")

    def update_data(self):
        # Payload for getting live indicator data
        payload = {
            "secret": self.ti_key,
            "construct": {
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "interval": "1m",
                "indicators": [
                    {"indicator": "rsi"},
                    {"indicator": "ema", "period": 20},
                    {"indicator": "macd"},
                    {"indicator": "sma", "period": 5},
                    {"indicator": "sma", "period": 20}
                ]
            }
        }

        # Params for getting live price data
        params = {
            "secret": self.price_key,      
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "1h"
        }

        headers = {"Content-Type": "application/json"}

        # Create an instance of the IndicatorManager
        indicator_manager = IndicatorManager(self.price_key, self.ti_key)

        
        # Get indicator data
        response_ta = requests.post(TAurl, json=payload, headers=headers)
        data_dict = json.loads(response_ta.content.decode("utf-8"))

        # Get price data
        response_price = requests.get(priceurl, params=params)
        if response_price.status_code == 200:
                price_data = response_price.json()
                indicator_manager.update_price(price_data)
        else:
            print(f"Failed to retrieve price data: {response_price.status_code}")

        # Update indicators
        indicator_manager.update_indicators(data_dict)

        return indicator_manager 