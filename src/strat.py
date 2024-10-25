import csv
from strat_start import IndicatorManager
import time
from winotify import Notification, audio
from datetime import datetime
from pathlib import Path

# Function to log data into a CSV file
def log_trade(action, price, short_sma, long_sma, current_profit, total_profit):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open("src/trade_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, action, price, short_sma, long_sma, current_profit, total_profit])

# Simulated function for receiving SMA values from an external class
# You would replace this class with the actual class or data source you're using
class PriceDataProvider:
    def __init__(self):
        self.price = None
        self.short_sma = None
        self.long_sma = None
        self.live_data = IndicatorManager()
        
    
    def get_price_and_sma(self):
        # self.live_data.display_data
        data = self.live_data.update_data()
        self.price = data.indicator_data.price
        self.short_sma = data.indicator_data.sma_5
        self.long_sma = data.indicator_data.sma_20
        return self.price, self.short_sma, self.long_sma


class strategy:
    def __init__(self):    
        # Initialize variables
        self.opened_trade_price=0
        self.opened_trade_type=""
        self.total_profit = 0
        
        #used to toggle desktop notifications
        self.desktop_notification=True
        self.icon_path = Path(__file__).parent  / 'logo.ico'  #make sure that the logo file is in the same directory as this file

        # Stop loss and take profit levels (configurable)
        self.stop_loss = 50  # in $
        self.take_profit = 100  # in $

        # Initialize the price data provider
        self.price_data_provider = PriceDataProvider()

        self.current_bar_index = 0

        self.last_higher = ""
        self.current_higher = ""

        self.parallel_trades_amnt = 1
        self.active_trades_amnt = 0

        self.open_trade = False

    # Function to process incoming data and apply trading logic
    def process_data(self):
        price, short_sma, long_sma = self.price_data_provider.get_price_and_sma()

        if short_sma > long_sma: 
            self.last_higher=self.current_higher
            self.current_higher = "short"

        elif short_sma < long_sma: 
            self.last_higher=self.current_higher
            self.current_higher = "long"
        
        

        #open long trade
        if self.current_higher == "short" and self.last_higher == "long" and self.active_trades_amnt < self.parallel_trades_amnt:
            log_trade("Open Long Trade", price, short_sma, long_sma, 0, self.total_profit)
            self.active_trades_amnt=+1
            self.opened_trade_type="long"
            self.opened_trade_price = price
            self.notify("long", "opened")
            
        
        #open short trade
        elif self.current_higher == "long" and self.last_higher == "short" and self.active_trades_amnt < self.parallel_trades_amnt:
            log_trade("Open Short Trade", price, short_sma, long_sma, 0, self.total_profit)
            self.active_trades_amnt=+1
            self.opened_trade_type="short"
            self.opened_trade_price = price
            self.notify("short", "opened")

        #close long (TP)
        elif self.active_trades_amnt > 0 and self.opened_trade_type=="long" and price>=self.opened_trade_price+self.take_profit:
            self.total_profit = self.total_profit - self.opened_trade_price + price
            log_trade("Close Long Trade (TP)", price, short_sma, long_sma, price - self.opened_trade_price, self.total_profit)
            self.active_trades_amnt=-1
            self.notify("long", "closed", price - self.opened_trade_price)
            

        #close long (SL)
        elif self.active_trades_amnt > 0 and self.opened_trade_type=="long" and price<=self.opened_trade_price-self.stop_loss:
            self.total_profit = self.total_profit - self.opened_trade_price + price
            log_trade("Close Long Trade (SL)", price, short_sma, long_sma, price - self.opened_trade_price, self.total_profit)
            self.active_trades_amnt=-1
            self.notify("long", "closed", price - self.opened_trade_price)

        #close short (TP)
        elif self.active_trades_amnt > 0 and self.opened_trade_type=="short" and price<=self.opened_trade_price-self.take_profit:
            self.total_profit = self.total_profit + self.opened_trade_price - price
            log_trade("Close Short Trade (TP)", price, short_sma, long_sma, self.opened_trade_price - price, self.total_profit)
            self.active_trades_amnt=-1
            self.notify("short", "closed", self.opened_trade_price - price)

        #close short (SL)
        elif self.active_trades_amnt > 0 and self.opened_trade_type=="short" and price>=self.opened_trade_price+self.stop_loss:
            self.total_profit = self.total_profit + self.opened_trade_price - price
            log_trade("Close Short Trade (SL)", price, short_sma, long_sma, self.opened_trade_price - price, self.total_profit)
            self.active_trades_amnt=-1
            self.notify("short", "closed", self.opened_trade_price - price)

        #current status if no trade is opened or closed in that iteration
        else: 
            if self.active_trades_amnt > 0 and self.opened_trade_type=="long":
                log_trade("active", price, short_sma, long_sma, price - self.opened_trade_price, self.total_profit)
            
            elif self.active_trades_amnt > 0 and self.opened_trade_type=="short":
                log_trade("active", price, short_sma, long_sma, self.opened_trade_price - price, self.total_profit)
            
            else:
                log_trade("idle", price, short_sma, long_sma, "-", self.total_profit)



    def notify(self, longshort, openclose, profit):
        if(profit > 0):
            message = f"A profit of {profit} dollars has been generated"


        else:
            message = f"A loss of {profit} dollars has been generated"
        
        if self.desktop_notification:
            toast = Notification(
                app_id="AutoTrader App",
                title=f'A {longshort} position has been {openclose}!',
                msg=message,
                icon=self.icon_path  # Absolute path to icon
            )
            toast.set_audio(audio.LoopingAlarm3, loop=False)
            toast.show()
#Main
strat = strategy()

#create new log file or show that 
with open("src/trade_log.csv", mode="a", newline="") as file:   #use "w" to delete previous log file, use "a" to append into existing file 
        writer = csv.writer(file)
        writer.writerow(["timestamp", "status", "price", "short sma", "long sma", "profit since opening trade", "total profit"])
while True:
    strat.process_data()
    time.sleep(15)
    # Depending on your setup, you can add sleep intervals or event-based triggers here
