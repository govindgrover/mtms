"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# important imports
from ..functions import functions as fn
from .Payment import Payment

class TokenOperation():
	__db	=	None
	__cur	=	None

	__pay	=	None

	def __init__(self, db):
		self.__db   =	db
		self.__cur  =	self.__db.cursor()

		self.__pay	=	Payment(db)

	def __isActive(self, tid):
		self.__cur.execute(
			'SELECT is_active, in_station FROM tokens WHERE token_id = \'{}\';'.format(
				tid
			)
		)
		res	= self.__cur.fetchall()

		if len(res):
			if res[0][0]:
				return True
			else:
				if res[0][1]:
					return True

		return False

	def __doTokenChecks(self, tid):
		if fn.isInDB(self.__db, 'tokens', 'token_id', tid):
			if not self.__isActive(tid):
				return {
					'status'	:	False
					, 'msg'		:	fn.lang_dict['warn_token_expired']
				}
			elif self.__isTimeOut(tid):
				return {
					'status'	:	False
					, 'msg'		:	fn.lang_dict['warn_token_timeout_expired']
				}
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_no_such_token_found']
			}

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['all_ok']
		}

	def __isTimeOut(self, tid):
		q1 = 'SELECT TIMEDIFF(CURTIME(), TIME(datetime)) < \'{}\' FROM tokens WHERE token_id = \'{}\';'.format(
				fn.configs.__IN_STATION_TIME_DIFF__, tid
		)
		q2 = 'SELECT in_station FROM tokens WHERE token_id = \'{}\';'.format(
			tid
		)

		self.__cur.execute(q1)
		q1_res	= self.__cur.fetchall()

		if len(q1_res) and q1_res[0][0]:			# 1 for true and None for not modified column
			return False
		else:
			self.__cur.execute(q2)
			q2_res	= self.__cur.fetchall()
			
			# checking for that id which is in station
			# for more than max time alloted
			if len(q2_res) and q2_res[0][0]:
				return True
			else:
				return False

	def __isInStation(self, tid):
		query = 'SELECT in_station FROM tokens WHERE token_id = \'{}\';'.format(
			tid
		)

		self.__cur.execute(query)
		res = self.__cur.fetchall()

		if len(res) and res[0][0] == 1:
			return True
		else:
			return False

	def __makeBooking(self, info):
		bid = fn.generateId()

		self.__cur.execute(
			fn.insertInTableCmd(
				'bookings'
				, ['booking_id', 'medium', 'medium_id', 'stat_start', 'stat_end', 'fare']
				, [
					[bid, 't', info['m_id'], info['start_id'], info['stop_id'], info['fare']]
				]
			)
		)
		self.__db.commit()

		return bid
	
	def __markJourney(self, f, t):
		q_amt = 'SELECT amt FROM fare_stations WHERE from_station = \'{}\' AND to_station = \'{}\';'.format(
				f
				, t
		)
		self.__cur.execute(q_amt)
		amt = self.__cur.fetchall()[0][0]

		return {
			'status'		:	True
			, 'start_id'	:	f
			, 'stop_id'		:	t
			, 'fare'		:	amt
		}
	
	
	def __stationEntry(self, tid):
		self.__cur.execute(
			'UPDATE bookings SET is_started = 1 WHERE medium_id = \'{}\';'.format(
				tid
			)
		)
		self.__cur.execute(
			'UPDATE tokens SET in_station = 1, is_active = 0 WHERE token_id = \'{}\';'.format(
				tid
			)
		)
		self.__db.commit()

		return {
			'status':	True
			, 'msg'	:	fn.lang_dict['entry_successful']
		}
	
	def __stationExit(self, tid):
		# since token id is unique every time so we are
		# not fetching booking id from bookings as we
		# have done in card operatiton
		self.__cur.execute(
			'UPDATE bookings SET is_complete = 1 WHERE medium_id = \'{}\';'.format(
				tid
			)
		)
		self.__cur.execute(
			'UPDATE tokens SET is_active = 0, in_station = 0 WHERE token_id = \'{}\';'.format(
				tid
			)
		)
		self.__db.commit()

		return {
			'status':	True
			, 'msg'	:	fn.lang_dict['exit_successful']
		}

	def printTicket(self, bid):
		flag = False
		
		# getting details to be printed from databse
		q_bdetails = 'SELECT stat_start, stat_end, fare, datetime, medium_id FROM bookings WHERE booking_id = \'{}\';'.format(
			bid
		)
		self.__cur.execute(q_bdetails)
		bdetails = self.__cur.fetchall()[0]
		
		if bdetails[0] == bdetails[1]:
			flag = True

		q_names = 'SELECT station_name FROM stations WHERE station_id IN (\'{}\', \'{}\');'.format(
			bdetails[0], bdetails[1]
		)
		self.__cur.execute(q_names)
		names = self.__cur.fetchall()

		# doing operations on the file
		f_path = fn.configs.os.path.join(
					fn.configs.os.environ["HOMEDRIVE"]
					, fn.configs.os.environ["HOMEPATH"]
					, (fn.configs.__PACKAGE_NAME__ + '_tickets')
		)

		try:
			fn.configs.os.mkdir(f_path)
		except FileExistsError:
			pass

		f_name = (f_path + '\\ticket-' + str(bid) + '.txt')

		f = open(f_name, 'w')

		f.write('TOKEN NUMBER: ' + str(bdetails[4]) + '\n')
		f.write('Single Journey' + '\n\n')

		if flag:
			f.write(names[0][0] + ' TO ' + names[0][0] + '\n')
		else:
			f.write(names[0][0] + ' TO ' + names[1][0] + '\n')
		
		date = str(bdetails[3].day) + '-' + str(bdetails[3].month) + '-' + str(bdetails[3].year)
		
		f.write(
			'DATE: '
			+ date
			+ '\n'
		)
		f.write(
			'TIME OF PURCHASE: '
			+ fn.configs.datetime.datetime.strftime(bdetails[3], "%H")
			+ ':'
			+ fn.configs.datetime.datetime.strftime(bdetails[3], "%M")
			+ ' Hrs.'
			+ '\n'
		)
		f.write(
			'FARE: Rs. '
			+ str(bdetails[2])
			+ '\n'
		)

		f.write(
			'\nVALID UPTO: '
			+ (
				bdetails[3]
				+ fn.configs.datetime.timedelta(
					minutes = int(fn.configs.__IN_STATION_TIME_DIFF__.split(':')[1])
				)
			).ctime()
			+ '\n'
		)

		f.close()

		return f_name

	def isToken(self, tid):
		if fn.isInDB(self.__db, 'tokens', 'token_id', tid):
			return True
		else:
			return False

	def buyToken(self, _from, _to):
		jdata = self.__markJourney(_from, _to)

		if not jdata['status']:
			return jdata

		_id = fn.generateId()

		self.__pay.setAmount(jdata['fare'])
		self.__pay.creditAmount()

		if self.__pay.isSuccess:
			self.__cur.execute(
				fn.insertInTableCmd(
					'tokens'
					, ['token_id']
					, [
						[_id]
					]
				)
			)
			self.__db.commit()

			jdata['m_id']	=	_id
			booking_id = self.__makeBooking(jdata)

			fn.showQR(_id)

			if fn.ask(fn.lang_dict['want_to_print_the_ticket']):
				print(
					'\n'
					, fn.lang_dict['your_ticket_is_located_at']
					, ': \''
					, self.printTicket(
						booking_id
					)
					, '\''
					, sep = ''
				)

				rtn = {
					'status'	:	True
					, 'msg'		:	''
				}
			else:
				rtn = {
					'status'	:	True
					, 'msg'		:	fn.lang_dict['your_token_id_is'] + ' ' + _id
				}
			
		else:
			rtn = {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_could_not_make_payment']
			}

		return rtn

	def onTouch(self, tid):
		checks = self.__doTokenChecks(tid)

		if checks['status'] != True:
			return checks

		if self.__isInStation(tid):
			return self.__stationExit(tid)
		else:
			return self.__stationEntry(tid)
