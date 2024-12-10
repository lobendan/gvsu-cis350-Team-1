# Overview
This Software Requirements Specification (SRS) document describes the functionality and constraints of the AutoTrader desktop application. The program allows users to automate or manually execute trades, monitor performance through visualizations, and manage trading parameters such as take profit, stop loss, and leverage. The application uses live data from APIs and supports multiple trading strategies. This document serves as a guide for development, testing, and validation.

# Software Requirements
This section provides the functional and non-functional requirements of the AutoTrader program. Requirements are grouped into categories for structure and clarity.

## Functional Requirements
### Data Management
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR1 | The program shall request live price data using API key | UT1, IT1 |
| FR2 | The program shall request live indicator data using API key | IT1 |
| FR3 | The program shall store live data within CSV file  | N/A |
| FR4 | The program shall load saved trading session data on startup. | N/A |
| FR5 | The program shall display real-time updates to the graphs during trading. | IT3 |
### Trade Management
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR6 | The program shall allow users to manually open a long or short trade. | IT2 |
| FR7| The system shall allow users to close an open trade manually. | IT2 |
| FR8 | The system shall support the addition of a stop loss for trades. | UT2 |
| FR9 | The system shall support the addition of a take profit level for trades. | UT3 |
| FR10 | The program shall execute trades automatically based on SMA strategy signals. | IT3, ST1 |
### User Interface
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR11 | The program shall use a desktop application interface. | N/A |
| FR12 | The UI shall allow users to pause automated trading. | N/A |
| FR13 | The UI shall display information within graphs. | ST1 |
| FR14 | Users shall be able to deposit and withdraw funds via the interface. | N/A |
| FR15 | The UI shall allow users to set leverage for trades. | N/A |
| FR16 | The user shall be able to edit and manipulate strategies | N/A |

## Non-Functional Requirements
### Data Management
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR1 | The data displayed shall be accurate to within 1 second of live updates. | UT4, ST2 |
| NFR2 | The data shall update in a matter of a few seconds | ST2 |
| NFR3 | The system shall log all trading activities | N/A |
| NFR4 | The trading data history shall be stored permanently | N/A |
| NFR5 | All data shall be timestamped for accurate record keeping | N/A |
### Performance and Efficiency
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR6 | The program shall execute a manual trade within a second of user confirmation | N/A |
| NFR7 | Automated trades shall trigger within 1 second of a buy or sell signal | N/A |
| NFR8 | System startup shall take no longer than 5 seconds | ST3 |
| NFR9 | Live graphs shall refresh without visible lag | N/A |
| NFR10 | The program shall process API data responses in under a second, per request. | N/A |
### User Interface
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR11 | The UI shall use visually distinct graphs for price, SMA, net worth, and profit data. | N/A |
| NFR12 | The UI shall show active trades showing price change percentage, the amount of money in the position, current profit/loss of the position | N/A |
| NFR13 | The UI shall allow the user to decide how much of an asset they want to purchase or sell | N/A |
| NFR14 | All interactive elements shall provide immediate feedback on activation. | N/A |
| NFR15 | The UI shall provide clear visual indicators for successful or failed trade execution. | N/A |

# Test Specification
This section defines the testing strategy, methods, and criteria used to ensure the functionality, reliability, and performance of the auto trader application. It describes the planned test cases, their purpose, and how they validate the system against the specified requirements.

## Unit Tests
| ID | Description | Steps | Input Values | Expected Output | Actual Output | Pass/Fail | Requirement Link |
| :--:| :--------------------------------------:| :-----------------------------------------------:| :-------------------------:| :---------------------------------------------------:| :-----------: | :-------: | :---------------:|
| UT1 | Test live price data fetching | Trigger `update_data` and assert `price` update | Mock price: 50000 | `price` set to 50000 | TBD | TBD | FR1 |
| UT2 | Add stop-loss for trades | Assign `stop_loss = 50` and verify update | Stop-loss: 50 | `stop_loss` set to 50 | TBD | TBD | FR8  |
| UT3 | Add take-profit for trades | Assign `take_profit = 200` and verify update | Take-profit: 200 | `take_profit` set to 200 | TBD | TBD | FR9 |
| UT4 | Test data accuracy in updates | Trigger live data update and check attributes    | Mock data update | Accurate and timely data update | TBD | TBD | NFR1 |

## Integration Tests
| ID | Description | Steps | Input Values | Expected Output | Actual Output | Pass/Fail | Requirement Link |
| :--:| :-------------------------------------------:| :---------------------------------------------------:| :-------------------------:| :---------------------------------------------------:| :-----------: | :-------: | :---------------:|
| IT1 | Integration of `run_Trader` and `PriceDataProvider` | Trigger data update, validate data flow between modules | Mock price: 50000 | `PriceDataProvider.price` updated | TBD | TBD | FR1, FR2 |
| IT2 | Validate UI updates for manual trading | Open manual trade via UI, check updates in UI and CSV | Mock input: "open long" | UI reflects trade; CSV logs the trade action | TBD | TBD | FR6, FR7 |
| IT3 | Test trade execution and graph update | Trigger SMA signal, validate CSV and graph updates   | Mock SMA: short > long | Trade logged; graph updated correctly | TBD | TBD | FR5, FR10 |

## System Tests 
| ID | Description | Steps | Input Values | Expected Output | Actual Output | Pass/Fail | Requirement Link |
| :--:| :------------------------------------------:| :---------------------------------------------------:| :-------------------------:| :---------------------------------------------------:| :-----------: | :-------: | :---------------:|
| ST1 | End-to-end automated trading loop test | Launch app, verify automated trade execution | Mock SMA, price data | Trades executed and logged; graphs updated | TBD | TBD | FR10, FR13 |
| ST2 | Performance test for data updates | Monitor live data updates, validate timing | Mock API responses | Updates within 1 second | TBD | TBD | NFR1, NFR2 |
| ST3 | Verify system startup initialization | Launch app, validate UI/backend initialization | Valid API keys | Successful system startup | TBD | TBD | NFR8 |

# Software Artifacts
Key deliverables and components produced and used throughout the development of the project

* [Use Case Lucidchart](https://lucid.app/lucidchart/4526676c-834a-4f2b-8cfa-a9dc2e0721cd/edit?viewport_loc=-653%2C136%2C3354%2C1379%2C.Q4MUjXso07N&invitationId=inv_3f43ef50-38d6-4c75-a037-401fbb2b5d55)

* [Idea Doc](https://docs.google.com/document/d/1d3P0VOt5sV0tdv9Wqa1Ne2ZHNL_9CU0AVL8GTHbeNXE/edit?usp=sharing)

* [Trello Board](https://trello.com/b/0UfcR0VN/gvsu-cis350-team-1)

* [Prototype GUI](https://discoursemap.retool.com/apps/a8ea5b26-8745-11ef-9a25-5bbe01d66544/Team-1---Auto-Trader-Prorotype-GUI)

* [Gantt Chart](CIS350-Team-1-Gantt.pdf) 

* [Final Presentation](CIS350_Auto_Trader_Final_Team1.pdf)

* [Use Case Diagram](Usecase.pdf)

* [Class Diagram](UMLclassDiagram.pdf)

* [Object Diagram](ObjectDiagram.pdf)