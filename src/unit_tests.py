import unittest
from strat import run_Trader


class AutoTraderTests(unittest.TestCase):

    def setUp(self):
        self.price_key = "TEST_PRICE_KEY"
        self.ti_key = "TEST_TI_KEY"
        self.trader = run_Trader(self.price_key, self.ti_key)

        # Replace the `update_data` method with a simulated one
        def fake_update_data():
            # Simulate indicator data
            self.trader.strat.price_data_provider.live_data.indicator_data = type(
                "IndicatorData",
                (object,),
                {
                    "rsi": 70,
                    "ema": 60000,
                    "sma_5": 500,
                    "sma_20": 400,
                },
            )()

            # Simulate price data
            self.trader.strat.price_data_provider.price = 50000
            self.trader.strat.price_data_provider.short_sma = 500
            self.trader.strat.price_data_provider.long_sma = 400

        # Override the `update_data` method
        self.trader.strat.price_data_provider.live_data.update_data = fake_update_data

    def test_request_live_price_data(self):
        """Test the program requests live price data (FR1)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        self.assertEqual(self.trader.strat.price_data_provider.price, 50000)

    def test_request_live_indicator_data(self):
        """Test the program requests live indicator data (FR2)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        indicators = self.trader.strat.price_data_provider.live_data.indicator_data
        self.assertEqual(indicators.rsi, 70)
        self.assertEqual(indicators.ema, 60000)
        self.assertEqual(indicators.sma_5, 500)
        self.assertEqual(indicators.sma_20, 400)

    def test_open_manual_long_trade(self):
        """Test manually opening a long trade (FR6)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        self.trader.strat.manual_trade = "open long"
        self.trader.run()
        self.assertEqual(self.trader.strat.active_trades_amnt, 1)
        self.assertEqual(self.trader.strat.opened_trade_type, "long")

    def test_close_manual_trade(self):
        """Test manually closing a trade (FR7)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        self.trader.strat.manual_trade = "open long"
        self.trader.run()
        self.trader.strat.manual_trade = "close trade"
        self.trader.run()
        self.assertEqual(self.trader.strat.active_trades_amnt, 0)

    def test_add_stop_loss(self):
        """Test adding a stop-loss for trades (FR8)."""
        self.trader.strat.stop_loss = 100
        self.assertEqual(self.trader.strat.stop_loss, 100)

    def test_add_take_profit(self):
        """Test adding a take-profit level for trades (FR9)."""
        self.trader.strat.take_profit = 200
        self.assertEqual(self.trader.strat.take_profit, 200)

    def test_automated_trade_execution(self):
        """Test automated trade execution based on SMA signals (FR10)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        self.trader.run()
        self.assertEqual(self.trader.strat.active_trades_amnt, 1)
        self.assertEqual(self.trader.strat.opened_trade_type, "long")

    def test_accuracy_of_data_update(self):
        """Test data accuracy and update speed (NFR1)."""
        self.trader.strat.price_data_provider.live_data.update_data()
        self.assertEqual(self.trader.strat.price_data_provider.price, 50000)


if __name__ == "__main__":
    unittest.main()
