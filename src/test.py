from strat import run_Trader
import time

trader = run_Trader()

while True:
    trader.run()
    time.sleep(15)