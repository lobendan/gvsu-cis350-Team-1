import unittest
from strat_start import IndicatorManager, IndicatorData
from strat import strategy, run_Trader
from new_vis import TradingApp
import tkinter as tk

class TestBase(unittest.TestCase):
    def setUp(self):
        # Global mock API keys
        self.price_key = "mock_price_key"
        self.ti_key = "mock_ti_key"


class TestIndicatorManager(TestBase):
    def test_price_update(self):
        manager = IndicatorManager(self.price_key, self.ti_key)
        
        # Mock price data
        price_data = {"value": 45000.0}
        manager.update_price(price_data)
        
        # Assert that the price was updated
        self.assertEqual(manager.indicator_data.price, 45000.0)

    def test_indicators_update(self):
        manager = IndicatorManager(self.price_key, self.ti_key)
        
        # Mock indicator data
        mock_data = {
            "data": [
                {"indicator": "RSI", "result": {"value": 70}},
                {"indicator": "EMA", "result": {"value": 44000.0}},
                {"indicator": "MACD", "result": {"valueMACD": 10, "valueMACDSignal": 9, "valueMACDHist": 1}}
            ]
        }
        manager.update_indicators(mock_data)
        
        # Assert that indicators were updated correctly
        self.assertEqual(manager.indicator_data.rsi, 70)
        self.assertEqual(manager.indicator_data.ema, 44000.0)
        self.assertEqual(manager.indicator_data.macd_value, 10)
        self.assertEqual(manager.indicator_data.macd_signal, 9)
        self.assertEqual(manager.indicator_data.macd_hist, 1)


class TestStrategy(TestBase):
    def test_automated_trade_logic(self):
        strat = strategy(self.price_key, self.ti_key)
        
        # Mock SMA crossing data
        strat.price_data_provider.get_price_and_sma = lambda: (45000, 46000, 44000)  # Short > Long
        strat.process_data()
        
        # Assert that a long trade is opened
        self.assertEqual(strat.opened_trade_type, "long")
        self.assertEqual(strat.active_trades_amnt, 1)

    def test_manual_trade_logic(self):
        strat = strategy(self.price_key, self.ti_key)
        strat.manual_trade = "open long"
        
        # Mock SMA and price data
        strat.price_data_provider.get_price_and_sma = lambda: (45000, 46000, 44000)
        strat.process_data()
        
        # Assert that a long trade is opened manually
        self.assertEqual(strat.opened_trade_type, "long")
        self.assertEqual(strat.active_trades_amnt, 1)


class TestIntegration(TestBase):
    def test_trade_lifecycle(self):
        trader = run_Trader(self.price_key, self.ti_key)
        strat = trader.strat
        
        # Mock SMA crossing conditions
        strat.price_data_provider.get_price_and_sma = lambda: (45000, 46000, 44000)  # Open long
        strat.process_data()
        
        strat.price_data_provider.get_price_and_sma = lambda: (45500, 45000, 46000)  # Close long
        strat.process_data()
        
        # Assert trade lifecycle
        self.assertEqual(strat.opened_trade_type, "")
        self.assertEqual(strat.active_trades_amnt, 0)
        self.assertGreater(strat.total_profit, 0)

    def test_live_price_update(self):
        manager = IndicatorManager(self.price_key, self.ti_key)
        
        # Mock live API response
        mock_price_response = {"value": 45500.0}
        manager.update_price(mock_price_response)
        
        # Assert price update
        self.assertEqual(manager.indicator_data.price, 45500.0)

    def test_ui_updates(self):
        root = tk.Tk()
        app = TradingApp(root, "mock_file.csv", run_Trader(self.price_key, self.ti_key))
        app.trader.strat.open_trade("long", 45000, 46000, 44000)
        
        # Mock UI update
        app.update_data()
        
        # Assert that UI reflects new trade
        self.assertIn("Active Profit", app.info_box_label.cget("text"))
        root.destroy()


class TestSystem(TestBase):
    def test_end_to_end_trading_cycle(self):
        trader = run_Trader(self.price_key, self.ti_key)
        strat = trader.strat
        
        # Mock full trading cycle
        strat.price_data_provider.get_price_and_sma = lambda: (45000, 46000, 44000)  # Open long
        strat.process_data()
        
        strat.price_data_provider.get_price_and_sma = lambda: (45500, 45000, 46000)  # Close long
        strat.process_data()
        
        # Assert end-to-end lifecycle
        self.assertEqual(strat.active_trades_amnt, 0)
        self.assertGreater(strat.networth, 1000)  # Initial net worth = 1000

    def test_graph_responsiveness(self):
        root = tk.Tk()
        app = TradingApp(root, "mock_file.csv", run_Trader(self.price_key, self.ti_key))
        
        # Mock graph data
        app.df = app.df.append({
            'timestamp': '2023-12-09 12:00:00',
            'price': 45500,
            'short sma': 46000,
            'long sma': 44000
        }, ignore_index=True)
        
        app.plot_data()
        
        # Assert graphs are updated without lag
        self.assertTrue(app.canvas is not None)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
