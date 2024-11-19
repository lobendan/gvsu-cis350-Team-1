import csv
import threading
import time
from strat_start import IndicatorManager
from winotify import Notification, audio
from datetime import datetime
from pathlib import Path
import os

# Function to log data into a CSV file
def log_trade(action, price, short_sma, long_sma, current_profit, total_profit):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("src/trade_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        if(isinstance(current_profit, float)):
            current_profit = round(current_profit,2)
            total_profit = round(total_profit,2)
            short_sma = round(short_sma, 2)
            long_sma = round(long_sma, 2)

        writer.writerow([timestamp, action, price, short_sma, long_sma, current_profit, total_profit])

# Simulated function for receiving SMA values from an external class
class PriceDataProvider:
    def __init__(self):
        self.price = None
        self.short_sma = None
        self.long_sma = None
        self.live_data = IndicatorManager()
        
    def get_price_and_sma(self):
        data = self.live_data.update_data()
        self.price = data.indicator_data.price
        self.short_sma = data.indicator_data.sma_5
        self.long_sma = data.indicator_data.sma_20
        return self.price, self.short_sma, self.long_sma

class strategy:
    def __init__(self):    
        self.opened_trade_price = 0
        self.opened_trade_type = ""
        self.total_profit = 0
        
        self.desktop_notification = True
        self.icon_path = Path(__file__).parent / 'logo.ico'

        self.stop_loss = 50  # in $
        self.take_profit = 100  # in $

        self.price_data_provider = PriceDataProvider()

        self.current_bar_index = 0
        self.last_higher = ""
        self.current_higher = ""
        self.manual_trade = ""

        self.parallel_trades_amnt = 1
        self.active_trades_amnt = 0

    def process_data(self):
        price, short_sma, long_sma = self.price_data_provider.get_price_and_sma()

        if short_sma > long_sma: 
            self.last_higher = self.current_higher
            self.current_higher = "short"
        elif short_sma < long_sma: 
            self.last_higher = self.current_higher
            self.current_higher = "long"


        #Manual Trade Logic
        if self.manual_trade == "open long":
            self.open_trade("long", price, short_sma, long_sma)
            self.manual_trade = ""

        elif self.manual_trade == "open short":
            self.open_trade("short", price, short_sma, long_sma)
            self.manual_trade = ""
            
        elif self.manual_trade == "close trade":
            self.close_trade("manual", "", price, short_sma, long_sma) #leave reason empty as the reason is manual (which is already known)
            self.manual_trade = ""

        # Automated Trade Logic
        elif self.current_higher == "short" and self.last_higher == "long" and self.active_trades_amnt < self.parallel_trades_amnt:
            self.open_trade("long", price, short_sma, long_sma)
            
        elif self.current_higher == "long" and self.last_higher == "short" and self.active_trades_amnt < self.parallel_trades_amnt:
            self.open_trade("short", price, short_sma, long_sma)

        elif self.active_trades_amnt > 0 and self.opened_trade_type == "long" and price >= self.opened_trade_price + self.take_profit:
            self.close_trade("long", "TP", price, short_sma, long_sma)
            
        elif self.active_trades_amnt > 0 and self.opened_trade_type == "long" and price <= self.opened_trade_price - self.stop_loss:
            self.close_trade("long", "SL", price, short_sma, long_sma)

        elif self.active_trades_amnt > 0 and self.opened_trade_type == "short" and price <= self.opened_trade_price - self.take_profit:
            self.close_trade("short", "TP", price, short_sma, long_sma)

        elif self.active_trades_amnt > 0 and self.opened_trade_type == "short" and price >= self.opened_trade_price + self.stop_loss:
            self.close_trade("short", "SL", price, short_sma, long_sma)
        
        else: 
            self.log_active_status(price, short_sma, long_sma)

    # Helper methods to handle trade actions automatically
    def open_trade(self, trade_type, price, short_sma, long_sma):
        log_trade(f"Open {trade_type.capitalize()} Trade", price, short_sma, long_sma, 0, self.total_profit)
        self.active_trades_amnt += 1
        self.opened_trade_type = trade_type
        self.opened_trade_price = price
        self.notify(trade_type, "opened", 0)

    def close_trade(self, trade_type, close_reason, price, short_sma, long_sma):
        profit = (price - self.opened_trade_price) if trade_type == "long" else (self.opened_trade_price - price)
        self.total_profit += profit
        log_trade(f"Close {trade_type.capitalize()} Trade ({close_reason})", price, short_sma, long_sma, profit, self.total_profit)
        self.active_trades_amnt -= 1
        self.notify(trade_type, "closed", profit)

    # Manual Trade Control Methods
    def open_manual_trade(self, trade_type):
        if self.active_trades_amnt < self.parallel_trades_amnt:
            price, short_sma, long_sma = self.price_data_provider.get_price_and_sma()
            self.open_trade(trade_type, price, short_sma, long_sma)
        else:
            print("Max parallel trades reached. Cannot open another trade.")

    def close_manual_trade(self):
        if self.active_trades_amnt > 0:
            price, short_sma, long_sma = self.price_data_provider.get_price_and_sma()
            profit = (price - self.opened_trade_price) if self.opened_trade_type == "long" else (self.opened_trade_price - price)
            self.total_profit += profit
            log_trade(f"Close {self.opened_trade_type.capitalize()} Trade (Manual)", price, short_sma, long_sma, profit, self.total_profit)
            self.active_trades_amnt -= 1
            self.notify(self.opened_trade_type, "closed", profit)
        else:
            print("No active trades to close.")

    def log_active_status(self, price, short_sma, long_sma):
        if self.active_trades_amnt > 0 and self.opened_trade_type == "long":
            log_trade("active", price, short_sma, long_sma, price - self.opened_trade_price, self.total_profit)
        elif self.active_trades_amnt > 0 and self.opened_trade_type == "short":
            log_trade("active", price, short_sma, long_sma, self.opened_trade_price - price, self.total_profit)
        else:
            log_trade("idle", price, short_sma, long_sma, "-", self.total_profit)

    def notify(self, longshort, openclose, profit):
        profit = round(profit, 2)
        message = f"A profit of {profit} dollars has been generated" if profit > 0 else f"A loss of {-profit} dollars has been generated" if profit < 0 else "You will be notified once the position is closed"
        
        if self.desktop_notification:
            toast = Notification(
                app_id="AutoTrader App",
                title=f'A {longshort} position has been {openclose}!',
                msg=message,
                icon=self.icon_path
            )
            toast.set_audio(audio.LoopingAlarm3, loop=False)
            toast.show()
# Trading loop in a separate thread
def trading_loop(strat):
    while True:
        strat.process_data()
        time.sleep(15)

# Manual input loop in a separate thread
def manual_input_listener(strat):
    while True:
        user_input = input("Enter command (e.g., 'open long', 'open short', 'close trade'): ").strip().lower()
        if user_input == "open long":
            strat.manual_trade = "open long"
        elif user_input == "open short":
            strat.manual_trade = "open short"
        elif user_input == "close trade":
            if strat.active_trades_amnt>0:
                strat.manual_trade = "close trade"
            else:
                print("No active trades, that can be closed.")
        else:
            print("Unknown command. Try again.")


class run_Trader: 
    def __init__(self):
        #csv vars
        csv_file = 'src/trade_log.csv'
        csv_mode = 'a'
        empty = True


        # Main strategy instance
        self.strat = strategy()

        #if the file already exists make sure the header doesn't get added again and get total profit
        if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
            empty = False
            # Open the file and read the contents
            with open(csv_file, mode="r", newline="") as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                    
                    # If there is at least one row, get the last row and the 8th column
                    if len(rows) > 1:  # Skip the header row
                        last_row = rows[-1]
                        last_value = last_row[6]  # Column 7 (index 6)
            
            self.strat.total_profit = float(last_value)

        # Create or append to the log file
        with open(csv_file, mode=csv_mode, newline="") as file:
            writer = csv.writer(file)
            if(empty):
                writer.writerow(["timestamp", "status", "price", "short sma", "long sma", "profit since opening trade", "total profit"])

        # Start threads
        # trading_thread = threading.Thread(target=trading_loop(strat))
        # input_thread = threading.Thread(target=manual_input_listener(strat))

        # trading_thread.start()
        # input_thread.start()
                                                                                                        
        # trading_thread.join()
        # input_thread.join()

    def run(self):
        self.strat.process_data()
