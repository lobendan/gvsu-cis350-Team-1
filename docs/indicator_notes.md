# Notes on Indicators

### Higher Priority: RSI, MACD

### Lowerer Priority: ADX, ATR, VIX, SAR

## RSI
RSI is the Relative Strength Index; Its purpose is to measure the speed and cange of different price movements. It can be used to figure out if something is being undersold or overbought.

The range of RSI is 0-100. Looking at typical values, if greater than 70 then the price is likely to be overvalued. If below 30 then its likely for it to be undervalued.

We hope to use RSI to notify for possible entry or exit points. We can also integrate an automated strategy that will initiate trades when RSI hits certain values.

## MACD
MACD stands for Moving Average Convergence Divergence. The purpose is to see changes in the strength, direction, and momentum of a trend in a price. 

It concists of a MACD line which is the difference between the 12-day and 26-day EMA (Exponetial Moving Average). The EMA is the graph of how ever many days it is, so 12-day EMA would be the graph of the last 12 days. There is also a signal line which is a 9-day EMA of the MACD line used previously. Finally, the histogram is the difference between the MACD and signal lines. This is used to visualize the strength of changes in trends.

Its overall use is to spot trend reversals and determine potential trading direction in the program. A bullish signal is when the MACD line crosses above the signal line, indicating an upward momentum. A bearish signal is when the MACD line crosses below the signal line.

## ADX
ADX is the Average Directional Index. It measures the stength of a trend, but does not measure the direction. It has a range of 0-100 and a value of above 25 indicates a strong trend while falling below 20 means a weak or non-existent trand (whether up or down). We can use ADX in combination with other indicators to confirm our predictios with other methods.

## ATR
ATR is the Average True Range and it measures the market volatility by using the range of a price of a certain time period. A higher ATR value indicates more volatility while lower values suggest less volitility. Its useful for adjusting the size of positions in an asset based on the volatility and risk.

## VIX
VIX, or Volatility Index, is also known as the fear guage and measures the markets expectation of futere volatility based on options of the S&P 500. A higher VIX often signals market uncertainty, while a lower VIX suggests confidence. Its not directly tied to asset prices but can provide insight into the risk levels.

## SAR
SAR is Parabolic Stop and Reverse, it identifies points where the direction of the market might change. Dots are plotted on a chart that trail the price and when the price touches a dot it is likely for a reversal in trend. We could use this to set trailing stop-loss levels for auto-selling or notifying the user.
