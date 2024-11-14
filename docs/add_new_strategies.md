# Instructions on how to add and implement new strategies

## 1. Get access to technical indicator and price data

- search for indicators available at [taapi.io/indicators](https://taapi.io/indicators/)
- each indicator has instruction on how to implemnt the api into a python program
- the main goal is to bundle all indicator data into one single payload to request its data 
- an example indicator payload can be found in [strat_start.py](..\src\strat_start.py)
- add the indicators which are need into the "indicators" field of the payload
- in order to make the indicator data available, a variable has to be created in the IndicatorData dataclass at the top of the document
- this variable has to be filled with the returned indicator data from the api in the update_indicators function which might require some debugging: let the class run and set a breakpoint insdide of the update_indicators function, where the 'data_dict' object can be analyzed. In there, find out the path on how to get to each indicator data. The loop will go through the object, create if statements that when the loop gets to the indicator name or id, the respective variable of the IndicatorData dataclass gets set to the live data from api-object. This has to be done for every indicator. By doing this, it allows you to access the data easily in the strategy itself.
 - to get access to __price data__ update the params dictionary to your desired exchange, coin, etc. More information on that can be found [here](https://taapi.io/indicators/price/)

## 2. implementing the strategy
 - All strategy logic is located at [strat.py](..\src\strat.py)
 - To add the logic to automatically open and close trades, look for "#Automated Trade Logic", the first two if statements are an example of when a long or a short trade will be opened. These if statements would need to be adjusted for the respective strategy. Make sure to calculate and process most of your data in the same function before the if statement.
- To adjust the stop loss and take profit margins. Adjust the stop_loss- take_profit attributes of the strategy class. You can either implement them static, like in the example strategy or adjust them over time with logic

  
  

