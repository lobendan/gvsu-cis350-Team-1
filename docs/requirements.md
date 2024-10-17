
# Software Requirement Specification

This document will be a collection of features, described in detail by functional- and non-functional requirements. This is an actively managed file, which will be updated while the project is being worked on. 

# Functional Requirements

**Get live data**
- the programshall request live data using APIs

**create analysis**
- the system shall save historical trading data permanently

**strategy creation**
- the system shall give the user the oportunity to add, edit, and delete strategies

**User Interface**
-the program shall be accessed using a desktop application

___

# Non-Functional Requirements

**Get live data**
- there shall be data about stocks, crypto, ETFs, and Forex
- the data shall be accurate to the live data shown on Trading View
- the data shall update in a matter of a few seconds


**Create analysis**
- to system shall display statistics like percentage of successfull trades, profit factor, maximum drawdown to the user

**strategy creation**
- the user shall be able to create python code as strategies having access to the indicators in python
- tutorials shall exists which teach users of how to create and edit strategies
- the user shall be able to add their API key to their broker for automating strategies
- the user shall be able to have the choice to either receive computer-, or mail notification or to automatically open trades
- automated trades shall trigger buy signals using APIs with a time difference of less than a second

**User Interface**
- the UI shall use line graphs to show price and net worth data
- the UI shall show active trades showing price change percentage, the amount of money in the position, current profit/loss of the position
  