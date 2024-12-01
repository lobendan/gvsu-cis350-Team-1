# Overview
This Software Requirements Specification (SRS) document describes the functionality and constraints of the AutoTrader desktop application. The program allows users to automate or manually execute trades, monitor performance through visualizations, and manage trading parameters such as take profit, stop loss, and leverage. The application uses live data from APIs and supports multiple trading strategies. This document serves as a guide for development, testing, and validation.

# Software Requirements
This section provides the functional and non-functional requirements of the AutoTrader program. Requirements are grouped into categories for structure and clarity.

## Functional Requirements
### <Data Management>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR1 | The program shall request live price data using API key | TBD |
| FR2 | The program shall request live indicator data using API key | TBD |
| FR3 | The program shall store live data within CSV file  | TBD |
| FR4 | The program shall load saved trading session data on startup. | TBD |
| FR5 | The program shall display real-time updates to the graphs during trading. | TBD |
### <Trade Management>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR6 | The program shall allow users to manually open a long or short trade. | TBD |
| FR7| The system shall allow users to close an open trade manually. | TBD |
| FR8 | The system shall support the addition of a stop loss for trades. | TBD |
| FR9 | The system shall support the addition of a take profit level for trades. | TDB |
| FR10 | The program shall execute trades automatically based on SMA strategy signals. | TBD |
### <User Interface>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| FR11 | The program shall use a desktop application interface. | TBD |
| FR12 | The UI shall allow users to pause automated trading. | TBD |
| FR13 | The UI shall display information within graphs. | TBD |
| FR14 | Users shall be able to deposit and withdraw funds via the interface. | TBD |
| FR15 | The UI shall allow users to set leverage for trades. | TBD |
| FR16 | The user shall be able to edit and manipulate strategies | TBD |

## Non-Functional Requirements
### <Data Management>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR1 | The data displayed shall be accurate to within 1 second of live updates. | TBD |
| NFR2 | The data shall update in a matter of a few seconds | TBD |
| NFR3 | The system shall log all trading activities | TBD |
| NFR4 | The trading data history shall be stored permanently | TBD |
| NFR5 | All data shall be timestamped for accurate record keeping | TBD |
### <Performance and Efficiency>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR6 | The program shall execute a manual trade within a second of user confirmation | TBD |
| NFR7 | Automated trades shall trigger within 1 second of a buy or sell signal | TBD |
| NFR8 | System startup shall take no longer than 5 seconds | TBD |
| NFR9 | Live graphs shall refresh without visible lag | TBD |
| NFR10 | The program shall process API data responses in under a second, per request. | TBD |
### <User Interface>
| ID | Requirement | Test Cases |
| :-------------: | :----------: | :----------: |
| NFR11 | The UI shall use visually distinct graphs for price, SMA, net worth, and profit data. | TBD |
| NFR12 | The UI shall show active trades showing price change percentage, the amount of money in the position, current profit/loss of the position | TBD |
| NFR13 | The UI shall allow the user to decide how much of an asset they want to purchase or sell | TBD |
| NFR14 | All interactive elements shall provide immediate feedback on activation. | TBD |
| NFR15 | The UI shall provide clear visual indicators for successful or failed trade execution. | TBD |
# Test Specification (if added)
<Description of what this section is>
## Unit tests
(copy/paste the below table a minimum of 4 times)
| ID | Description | Steps | Input Values | Expected Output | Actual Output
| Pass/Fail | Requirement Link |
| :-------------: | :----------: | :----------: | :----------: | :----------:
| :----------: | :----------: | :----------: |
| TC1 | <TC1 description> | <steps to execute TC1> | <input values to this
test case> | <expected output as a result of test case> | <actual output of
test case> | <did it pass or fail?> | <requirement IDs this test case is
linked to> |

## Integration tests
(copy/paste the above table a minimum of 3 times)

## System tests
(copy/paste the above table a minimum of 3 times)

# Software Artifacts
<Describe the purpose of this section>
* [I am a link](to_some_file.pdf)