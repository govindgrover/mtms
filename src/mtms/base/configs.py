"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# importing required modules and methods
# all dependent modules are impoerted here
try:
	import os
	import mysql.connector
	import uuid
	import time
	import datetime
	import sys
	import traceback
	import json
	import pickle
	import pyqrcode
except ImportError as e:
	exit('ERROR: Failed to import required modules!\n' + str(e))

# **************************************
# ********* START DO NOT TOUCH *********
# **************************************

# constants for the system
__DEBUG__ = False

__PACKAGE_NAME__	=	'mtms'
__PYTHON_PATH__		=	sys.path[4]

__PACKAGE_PATH__	=	__PYTHON_PATH__ + '\\Lib\\site-packages\\' + __PACKAGE_NAME__
__LOGS_PATH__		=	__PACKAGE_PATH__ + '\\logs'

__DB_STRUCT_FILE__		=	__PACKAGE_PATH__ + '\\initials\\database\\metro_db_struct.sql'
__DEFAULT_LANG_FILE__	=	__PACKAGE_PATH__ + '\\initials\\lang\\en.json'

__REQ_DB_TABLES__ = [('bookings'), ('cards'), ('fare_stations'), ('routes'), ('stations'), ('station_close_status'), ('tokens'), ('transactions'), ('users')]

__LANG_PATH__		=	__PACKAGE_PATH__ + '\\lang'
__LANG_CHOICES__ = {
	'hi'	:	'हिंदी'
	, 'en'	:	'English'
}

__RUN_INFO_FILE__  =	__PACKAGE_PATH__ + '\\' + __PACKAGE_NAME__ +'_run_info.dat'

# constants for the view
__SCREEN_WIDTH__ = os.get_terminal_size().columns

# **************************************
# ********** END DO NOT TOUCH **********
# **************************************


# TOUCHABLE
"""
	NOTE: THE DATABASE NAME HERE MUST MATCH WITH THE GIVENIN THE THE FILE
	<python_path>/mtms/initials/database/metro_db_struct.sql file
"""
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
