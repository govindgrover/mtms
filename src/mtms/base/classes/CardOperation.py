"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# important imports
from ..functions import functions as fn

class CardOperation():
	__db	=	None
	__cur	=	None

	def __init__(self, db):
		self.__db   =	db
		self.__cur  =	self.__db.cursor()

	def __isActive(self, cid):
		self.__cur.execute(
			'SELECT is_active FROM cards WHERE card_id = \'{}\';'.format(
				cid
			)
		)
		res	= self.__cur.fetchall()

		if res[0][0] == 1:
			return True
		else:
			return False

	def __doCardChecks(self, cid):
		if fn.isInDB(self.__db, 'cards', 'card_id', cid):
			if self.__isActive(cid):
				return {
					'status'	:	True
					, 'msg'		:	''
				}
			else:
				return {
					'status'	:	False 
					, 'msg'		:	fn.lang_dict['card_is_inactive']
				}
		else:
			return {
				'status'	:	False 
				, 'msg'		:	fn.lang_dict['warn_no_such_card_found']
			}

	def __isInStation(self, cid):
		query = 'SELECT in_station FROM cards WHERE card_id = \'{}\';'.format(
			cid
		)

		self.__cur.execute(query)
		res = self.__cur.fetchall()

		if len(res) and res[0][0] == 1:
			return True
		else:
			return False

	def __stationEntry(self, cid, entry_sid):
		bid		=	fn.generateId()
		self.__cur.execute(
				'SELECT route_id FROM stations WHERE station_id = \'{}\';'.format(
				entry_sid
			)
		)

		route	=	self.__cur.fetchall()[0][0]

		booking_query = fn.insertInTableCmd(
			'bookings'
			, ['booking_id', 'medium_id', 'medium', 'route_id', 'stat_start', 'is_started']
			, [
				[bid, cid, 'c', route, entry_sid, 1]
			]
		)
		card_update_query = 'UPDATE cards SET in_station = 1, last_book = \'{}\' WHERE card_id = \'{}\';'.format(
			bid, cid
		)

		self.__cur.execute(booking_query)
		self.__cur.execute(card_update_query)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['entered_into_the_station_successfully']
		}

	def __stationExit(self, cid, exit_sid):
		# fetching booking id for last trip
		self.__cur.execute(
			'SELECT last_book FROM cards WHERE card_id = \'{}\';'.format(
				cid
			)
		)
		bid = self.__cur.fetchall()[0][0]

		# selecting starting station id for current trip
		self.__cur.execute(
			'SELECT stat_start FROM bookings WHERE booking_id = \'{}\''.format(
				bid
			)
		)
		start_sid = self.__cur.fetchall()[0][0]

		# selecting fare for the trip route
		self.__cur.execute(
			'SELECT amt FROM fare_stations WHERE from_station = \'{}\' AND to_station = \'{}\';'.format(
				start_sid, exit_sid
			)
		)
		fare = self.__cur.fetchall()[0][0]

		# updating booking data
		self.__cur.execute(
			'UPDATE bookings SET stat_end = \'{}\', fare = {}, is_complete = 1 WHERE booking_id = \'{}\';'.format(
				exit_sid, fare, bid
			)
		)

		# updating card info
		self.__cur.execute(
			'UPDATE cards SET bal = bal - {}, last_book = NULL, in_station = 0 WHERE card_id = \'{}\';'.format(
				fare, cid
			)
		)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['exited_the_station_successfully']
		}

	def isCard(self, cid):
		if fn.isInDB(self.__db, 'cards', 'card_id', cid):
			return True
		else:
			return False

	def onTouch(self, cid, cur_stat):
		# checking station closure
		c = fn.checkStationClosure(self.__db, cur_stat)

		if c['status']:
			return c

		# card id is exiting the station
		checks = self.__doCardChecks(cid)
		if not checks['status']:
			return checks['msg']

		if self.__isInStation(cid):
			return self.__stationExit(cid, cur_stat)
		else:
			return self.__stationEntry(cid, cur_stat)

