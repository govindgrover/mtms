# Metro Train Management System (MTMS)

### A School Project in Python (CBSE India)


<br />
<p align="center">
    <img src="https://img.shields.io/badge/license-GPL-orange.svg" />
	<img src="https://img.shields.io/badge/python-%3E%3D%203.8-yellow" />
	<img src="https://img.shields.io/badge/pip-%3E%3D%2020.1-blue" />
    <img src="https://img.shields.io/badge/Module Version-1.0.1-green" />
</p>

<br />

## Table of contents

- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Description](#description)
	- [Hardware Requirements](#hardware-requirements)
	- [Software Requirements](#software-requirements)
	- [Understanding the System](#understanding-the-system)
	- [Limitations](#limitations)
	- [Module Dependencies](#module-dependencies)
	- [User-defined Functions](#user-defined-functions)
	- [Data Files](#data-files)
- [Copyright and license](#copyright-and-license)


# Quick Start

Several quick start options are available:

- Install from pip: `pip install mtms`
- Clone the repo: `gh repo clone govindgrover/mtms`
- Clone the repo: `https://github.com/govindgrover/mtms.git`

<br />

# Configuration 
You can change the default configuration s in the file:
```python
<python-path>/Lib/site-packages/mtms/base/config.py
```

The default configuration  is as follow:
```python
# DATABASE INITIALS
__DB_USER__ = 'root'
__DB_PASS__ = 'password'
__DB_HOST__ = 'localhost'
__DB_NAME__ = 'metro_db'

# MUST BE IN 24-hour FORMAT
# AT WHICH OF CLOCK THE STATIONS WILL OPEN
__TRAIN_TIME_START__ = 9
# AT WHICH OF CLOCK THE STATIONS WILL CLOSE
__TRAIN_TIME_END__ = 23

# SECURITY AMOUNT TO BE TAKEN FROM THE CUSTOMER
__NEW_CARD_SECURITY__ = 50
# MINIMUM AMOUNT TO BE RECHARGED
__MIN_CARD_RECHARGE_AMOUNT__ = 200
# MAXIMUM AMOUNT TO BE RECHARGED
__MAX_CARD_RECHARGE_AMOUNT__ = 2000

# TIME FOR WHICH ONE CAN STAY AT STATION WHICH BEING ON THE TRAIN
__IN_STATION_TIME_DIFF__ = '00:20:00'

# WANT TO USE QR OR NOT
__USE_QR__ = True
```

In the above <b>\_\_DB\_NAME\_\_</b> the database name must match which is given in the initial database file. so it will be good if you take care of it. Otherwise if you really want to change it, you can do it at:

'''python
<python path>/Lib/site-packages/mtms/initials/database/metro_db_struct.sql
'''



<br />

---

# Description

<br />

## Hardware Requirements

| **Hardware Requirements** |
| --- |
| PC or Laptop satisfying the below software requirements |

<br />

## Software Requirements

| **Software Requirements**| |
| --- | --- |
| **OS** | Any; _Preferred: Windows 10_ |
| **Python** | &gt;= 3.8 |
| **pip** | &gt;= 20.1 |
| **Command Prompt** | Yes; _Preferred: Windows Terminal from Windows 10 Store - [download](https://www.microsoft.com/store/productId/9N0DX20HK701)_ |
| **Font** | Consolas; _Preferred: Any Hindi supporting font_ |

<br />

## Understanding the System

<br />

Aim of this module is to bring easiness for everyone who works as a staff member at metro or a daily job person who uses metro as transport.

**Metro Train Management System** helps one to manage different stations and their routes along with the counter system and customer booking system.

<br />

## Limitations

- Line Routes are mentioned but there is no use of them because then it will become more tedious on our hand.
- Customer cannot view his/her journey going on screen.
- Customer has to remember a 36-character long token/card ID.

<br />

# Module Dependencies

- OS
- mysql.connection
- uuid
- time
- datetime
- sys
- traceback
- json
- pickle
- pyqrcode

# User-defined Functions

<br />

_/\_\_init\_\_.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| run | Void | None | Starts the main system |

_/base/classes/Admin.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_addFareForStation | station\_info : dict | Boolean | Assign fare for the added station whose _station\_id_ is given through the parameter |
| login | username : str, password : str | dict | Login the admin user if the credentials matched |
| logout | Void | dict | Logout the admin user |
| addAccount | username : str, email : str, password : str, role : int | dict | Adds new user account based on the given data.Role is 0 for admin and 1 for counter |
| addRoute | route\_name : str | dict | Adds new route |
| addStation | station\_name : str, route\_id : str | dict | Adds new station and assign it on the provided route |
| renameRoute | \_id : str, new\_name : str | dict | Rename the provided route |
| renameStation | \_id : str, new\_name : str | dict | Rename the provided station |
| modifyStationFares | f\_id : str, t\_id : str, amt : float | dict | Modify the fare charges for the provided pair of stations |
| getAllRoutesAndStations | Void | dict | Gives all of the stations name and their assigned route names |
| getAllUsers | Void | dict | Gives a list of users their emails and roles |
| backupDatabase | Void | dict | Backup the current database to the location:&lt;Python folder&gt;/Lib/mtms/\_backups/db\_backup.sql |
| resetDatabase | Void | dict | It will reset the database and recreate it from the initial file |
| changeStationStatus | sid : str, status : int, reason : str | dict | It will set the station closure status as specified with a reason to the provided station |
| viewStationStatus | sid : str | dict | It will tell the station closure station for the provided station |

_/base/classes/CardOperation.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_isActive | cid : str | Boolean | Checks weather the provided Card - ID is valid or not |
| \_\_doCardChecks | cid : str | dict | Performs checks on the provided Card – ID |
| \_\_isInStation | cid : str | Boolean | Checks weather the provided card has checked-in a station or not |
| \_\_stationEntry | cid : str, entry\_sid : str | dict | Mark the provided card as in-station for the provided station and make a new booking |
| \_\_stationExit | cid : str, exit\_sid : str | dict | Mark the provided card as out-station for the provided station and make a complete the opened booking |
| isCard | cid : str | Boolean | Tells weather the provided Card-ID is valid and original or not |
| onTouch | cid : str, cur\_stat : str | dict | It performs action on the provided Card-ID according to the state which it is in with respect to the current station |

_/base/classes/ConsoleTable.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_sumUpLengths | Void | int | It tells the number of columns in total for the provided data for creatin the table borders |
| \_\_makeListOfLengthOfEachInnerListItem | Void | list | It makes a list which contains length of all columns data provided |
| \_\_getListOfThisIndexFromInnerLists | arr : list, index : int | list | It calculates the maximum number of characters occurring in the respected column at that index |
| \_\_setAutoMaxLengths | Void | None | It sets the maximum character length needed for a good looking table |
| \_\_checkData | Void | Boolean | It checks weather the number of provided columns and rows is greater than zero or not |
| setColumnHeaders | cols : list | None | Set headers |
| setRows | rows : list | None | Set rows |
| createTable | Void | None | Prints a final table output |

_/base/classes/Counter.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_isCardExists | card\_id | Boolean | Checks weather the provided Card-ID exists or not |
| login | username : str, password : str | dict | Login the counter user if the credentials matched |
| logout | Void | dict | Logout the counter user |
| getCardBalance | cid : str, amt\_only : bool = False | dict | Gives card balance for the provided card and if amt\_onlysets to Truethen it will return only float amount |
| printCard | cid : str | str | Prints the provided Card-ID with its amount into a text file |
| buyNewCard | Void | dict | Create a new metro card |
| rechargeCard | cid : str | dict | Recharge the card |
| refundCard | cid : str | dict | Disable the card when refunded successfully |

_/base/classes/Payment.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_selectMode | Void | None | Sets the current payment mode as per user&#39;s choice |
| \_\_takeAmount\_and\_Proceed | Void | None | Asks to user to enter the amount and do some checks then accordingly approves or disapproves the transaction |
| \_\_confirmAmt\_and\_Proceed | Void | None | Asks the user for confirmation for the transaction of pre-defined balance |
| setAmount | to\_charge : float | None | Sets the pre-defined amount |
| setMaxAmount | max\_to\_charge : float | None | Sets the max amount that the users can enter |
| amountRecived | Void | Float | Returns the amount entered by the user |
| creditAmount | Void | None | Performs the main transaction with user interaction |

_/base/classes/TokenOperation.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| \_\_isActive | tid : str | Boolean | Checks weather the provided Token - ID is valid or not |
| \_\_doTokenChecks | tid : str | dict | Performs checks on the provided Token – ID |
| \_\_isTimeOut | tid : str | Boolean | Checks weather the token is expired or not |
| \_\_isInStation | tid : str | Boolean | Checks weather the provided token has checked-in a station or not |
| \_\_stationEntry | tid : str | dict | Mark the provided token as in-station and make a new booking |
| \_\_stationExit | tid : str | dict | Mark the provided token as out-station and make a complete the opened booking |
| \_\_makeBooking | info : dict | str | Makes a new booking when a token is purchased based on the provided data |
| \_\_markJourney | f : str, t : str | dict | Helps to fetch the fare for the provided pair of stations |
| isToken | tid : str | Boolean | Tells weather the provided Token-ID is valid and original or not |
| onTouch | cid : str | dict | It performs action on the provided Token - ID according to the state which it is in |
| printTicket | bid : str | str | Prints the ticket into a text file based on the booking data |
| buyToken | \_from : str, \_to : str | dict | Makes a new token and assign a new booking to it for the provided pair of stations |

_/base/functions/functions.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| get\_runs\_upto | Void | int | Tells how many time the system is ran till now from the time of setup |
| showCountDown | text : strt : int | None | It shows a countdown for t time with the provided text |
| ask | q : str | Boolean | Asks the user provided question and tells weather he said yes or no |
| printHeading | tree : list, width : int, sep\_times : int = 5 | None | Print a heading at top of the console screen after clearing all the past printed lines |
| insertInTableCmd | tbl\_name : str, arr\_col : list, arr\_val : list | str | Returns a SQL insert query based on the data provided |
| generateId | Void | str | Generates a unique id through the python&#39;s UUID module |
| isInDB | db : object, tbl\_name : str, col\_name : str, val : any | Boolean | Checks weather the provided record is exists or not |
| checkStationTimmings | Void | dict | Checks and tells weather the station is opened or closed during the hours |
| getAllRoutes | db : object | dict | Fetch all of routes |
| getAllStations | db : object | dict | Fetch all of stations |
| searchStations | db : object, like\_text : str | str | Helps the user to search the stations based on the provided input and return the station\_id for the selected station |
| searchRoutes | db : object, like\_text : str | str | Helps the user to search the routes based on the provided input and return the route\_id for the selected route |
| showQR | txt : str, showTxt : str | None | Generates and show the QR Code for thr provided text string |
| checkStationClosure | db : object, sid : str | dict | Checks weather a specific station is closed or not |
| makeErrorLog | Void | str | Makes an error log file for the errors raised during the execution of the program through the traceback module |
| setWorkingLang | dft : bool = False | dict | Return a dictionary of lines used in the program by reading a language file from users&#39; choice |
| importInitials | db : object = None, isReset : bool = False | Boolean | it imports and sets important data at its place |
| isFirstLanuch | Void | Boolean | Tells weather the system is running for the first time or not |
| firstThingsFirst | Void | None | The very first function to be executed for the system |

_/base/menu/admin\_menu.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| login | Void | None | Login the admin user if the credentials matched |
| logout | Void | None | Logout the admin user |
| addNewUser | Void | None | Adds new user account based on the given data.Role is 0 for admin and 1 for counter |
| addNewRoute | Void | None | Adds new route |
| addNewStation | Void | None | Adds new station and assign it on the provided route |
| renameTheRoute | Void | None | Rename the provided route |
| renameTheStation | Void | None | Rename the provided station |
| changeFares | Void | None | Modify the fare charges for the provided pair of stations |
| showAllRoutesAndStations | Void | None | Gives all of the stations name and their assigned route names |
| showAllUsers | Void | None | Gives a list of users their emails and roles |
| takeBackup | Void | None | Backup the current database to the location:&lt;Python folder&gt;/Lib/mtms/\_backups/db\_backup.sql |
| modifyStationStatus | Void | None | It will set the station closure status as specified with a reason to the provided station |
| viewStationStatus | Void | None | It will tell the station closure station for the provided station |
| resetEverthing | Void | None | It will drop the current database and then recreate it from the initials |

_/base/menu/counter\_menu.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| login | Void | None | Login the counter user if the credentials matched |
| logout | Void | None | Logout the counter user |
| getBalance | Void | None | Gives card balance for the provided card and if amt\_onlysets to Truethen it will return only float amount |
| buyCard | Void | None | Create a new metro card |
| rechargeTheCard | Void | None | Recharge the card |
| refundTheCard | Void | None | Disable the card when refunded successfully |

_/base/menu/customer\_menu.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| touch | Void | None | Performs functionalities according to the type of touch |
| getToken | Void | None | Performs functionalities for buying a new token |

_/base/menu/customer\_menu.py_

| **Function Name** | **Parameter(s)** | **Return** | **Description** |
| --- | --- | --- | --- |
| showMenu | module : object, view : dict, tree : list | None | Show menu depending on the provided information |

<br />

# Data Files

| **File Name** | **Location** | **Description** |
| --- | --- | --- |
| mtms\_run\_info.bin | &lt;Python folder&gt;/Lib/mtms/ | Stores number of times the system is ran from the first setup |

# Copyright and license

Code and documentation copyright 2021-22 Govind Grover Code released under the [GPL License](https://github.com/govindgrover/mtms/blob/master/LICENSE). Docs released under [Creative Commons](https://creativecommons.org/licenses/by/4.0/).
