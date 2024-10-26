Team name: Team 1

Team members: James McCarty, Brendan Gross, Daniel Lobenstein

# Introduction

The objective of our project is to build an "Autotrader" that is able to get live data and is a framework to automate different trading strategies.
Using that framework, users are able to automate their own strategies, without needing to sit on their screen to do it. 

In order to create the best and easiest user experience, it is essential to have as much information to as many products as possible. 
Meaning there shouldn't be indicators missing as options to as many different stocks, crypto currencies, forex currenices, ETFs, and so on. 

Another major objective is to do this in a cost efficient way, without having excessive costs of APIs to get the data and instead try to rely as much 
as possible on free APIs or even scrape the data off public websites to get the necessary data. This part of the program should also be flexible so that the user is also able 
to choose APIs which might not be free without having to change too much.

An optional feature would be to also test strategies by using old historical data to test the strategies without having to wait for longer periods of time.

The program is designed to be a accessed using a desktop app as a simple but useful GUI.

The results should be output in a generated Excel file. 


FEATURES:
    -Simple GUI (Desirable)
    -Collect trading data (Essential)
    -Analyze the data (Desirable)
    -Create trading strategies from data (Essential)
    -Suggest trades / auto trade based on strategies (Essential)
    -Automatically open and close real trades on exchanges (Optional)

# Anticipated Technologies

UPDATE

Use APIs and/or webscrapers to get the data.
Technologies to create the desktop APP (GUI). 
Use openpyxl or similar module to create the Excel files.


# Method/Approach
First we should find a way to get the price data in an cost- and overall efficient way.
See if there's a good way to get the indicator data as well, if not try to create some on our own. (there should be opensource for many) 
Start creating the framework for the strategies. 
Create the Excel output.


# Estimated Timeline

Timeline is documented using a Gantt chart. 
Go to [OnlineGantt](https://www.onlinegantt.com/#/gantt) and import the gantt document found at docs\Gantt_chart.gantt


(Figure out what your major milestones for this project will be, including how long you anticipate it *may* take to reach that point)

# Anticipated Problems

Find good ways to get the data - research different ways and compare them
Connect the logic with the GUI - have set parameters that are easily accessed to have output in the GUI
Actual algorithm to analyze the data - individual research and group meetings to find the best and most efficient way

