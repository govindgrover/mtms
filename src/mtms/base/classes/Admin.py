"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# important imports
from ..functions import functions as fn

class Admin():
	__login_status__	=   False
	__db				=   None
	__cur				=   None

	def __init__(self, db):
		self.__db   =	db
		self.__cur  =	self.__db.cursor()

	def __addFareForStation(self, station_info):
		if not(self.__login_status__):
			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}
		
		try:
			to_add = []
			cnt = 1

			outputs = fn.getAllStations(self.__db)

			if outputs == {}:
				outputs = [list(station_info.values())]

			len_outputs = len(outputs)

			for x in outputs:
				try:
					theFare = float(
						input(
							str(cnt)
							+ ' of '
							+ str(len_outputs)
							+ ') '
							+ fn.lang_dict['enter_fare_for']
							+ ' from '
							+ station_info['name']
							+ ' to '
							+ outputs[x]
							+ ': '
						)
					)
				except:
					fn.makeErrorLog()
					self.__db.rollback()
					return False

				to_add.append(
					[station_info['id'], x, theFare]
				)
				if not(station_info['id'] == x):
					to_add.append(
						[x, station_info['id'], theFare]
					)

				cnt += 1

			self.__cur.execute(
				fn.insertInTableCmd(
					'fare_stations'
					, ['from_station', 'to_station', 'amt']
					, to_add
				)
			)
			
			self.__cur.execute(
				fn.insertInTableCmd(
					'station_close_status'
					, ['station_id', 'status']
					, [[station_info['id'], 1]]
				)
			)

			# commiting the station and acc.ly fares
			self.__db.commit()
			return True
		except:
			fn.makeErrorLog()
			self.__db.rollback()
			return False 

	def login(self, username, password):
		q = 'SELECT id FROM users WHERE name = \'{}\' and password = \'{}\' and role = 0;'.format(
			username, password
		)

		self.__cur.execute(q)
		o = self.__cur.fetchall()

		if len(o) > 0 and len(o[0]) > 0:
			self.__login_status__ = True
			return {
				'status':	True
				, 'msg'	:	fn.lang_dict['loggedin_successfully']
			}
		else:
			return {
				'status':	False
				, 'msg'	:	fn.lang_dict['invalid_credentials']
			}

	def logout(self):
		self.__login_status__ = False

		return {
			'status':	True
			, 'msg'	:	fn.lang_dict['loggedout_successfully']
		}

	def addAccount(self, username, email, password, role):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		self.__cur.execute(
			fn.insertInTableCmd(
				'users'
				, ['name', 'email', 'password', 'role']
				, [
					[username, email, password, role]
				]
			)
		)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['account_added']
		}

	def addRoute(self, route_name):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		_id = fn.generateId()

		self.__cur.execute(
			fn.insertInTableCmd(
				'routes'
				, ['route_id', 'route_name']
				, [
					[_id, route_name]
				]
			)
		)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['route_added']
		}

	def addStation(self, name, route_id):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		self.__cur.execute(
			'SELECT id FROM routes WHERE route_id = \'{}\''.format(
				route_id
			)
		)

		if len(self.__cur.fetchall()) <= 0:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_no_route_found']
			}

		_id = fn.generateId()

		self.__cur.execute(
			fn.insertInTableCmd(
				'stations'
				, ['station_id', 'station_name', 'route_id']
				, [
					[_id, name, route_id]
				]
			)
		)

		# since fares are not entered, not commiting the query
		tmp = self.__addFareForStation({
			'id'	:	_id
			, 'name':	name
		})

		if tmp:
			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['station_and_fares_added']
			}
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['could_not_add_station_and_fares']
			}

	def renameRoute(self, _id, new_name):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		if not fn.ask(fn.lang_dict['are_you_sure']):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['process_declined_by_user']
			}

		# id_to_change = list(routes.keys())[opt]

		q = 'UPDATE routes SET route_name = \'{}\' WHERE route_id = \'{}\';'.format(
			new_name, _id
		)

		self.__cur.execute(q)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['route_renamed']
		}

	def renameStation(self, _id, new_name):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		if not fn.ask(fn.lang_dict['are_you_sure']):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['process_declined_by_user']
			}

		q = 'UPDATE stations SET station_name = \'{}\' WHERE station_id = \'{}\';'.format(
			new_name, _id
		)

		self.__cur.execute(q)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	fn.lang_dict['station_renamed']
		}

	def modifyStationFares(self, f_id, t_id, amt):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		if not fn.ask(fn.lang_dict['are_you_sure']):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['process_declined_by_user']
			}

		q = 'UPDATE fare_stations SET  amt = {} WHERE from_station = \'{}\' AND to_station = \'{}\';'.format(
				amt, f_id, t_id
		)

		self.__cur.execute(q)
		self.__db.commit()

		return {
			'status'	:	True
			, 'msg'		:	'Fare modified'
		}

	def getAllRoutesAndStations(self):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}
		
		q1 = 'SELECT s.station_name, r.route_name FROM stations s, routes r WHERE r.route_id = s.route_id ORDER BY s.station_name ASC;'
		self.__cur.execute(q1)

		res = self.__cur.fetchall()
		if len(res):
			q2 = 'SELECT "- NO STATION ASSIGNED -", r.route_name FROM routes r LEFT JOIN stations s ON s.route_id = r.route_id WHERE s.route_id is NULL;'
			self.__cur.execute(q2)
	
			res.extend(self.__cur.fetchall())

			return {
				'status'	:	True
				, 'data'	:	res
			}
		else:
			self.__cur.execute(
				'SELECT route_name FROM routes ORDER BY route_name ASC;'
			)
			r = self.__cur.fetchall()
			if len(r):
				return {
					'status':	True
					, 'data':	r
				}
			else:
				return {
					'status'	:	False
					, 'msg'		:	fn.lang_dict['warn_no_records_found']
				}

	def getAllUsers(self):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}
		
		q = 'SELECT name, email, role FROM users ORDER BY role ASC;'
		self.__cur.execute(q)

		res = self.__cur.fetchall()
		if len(res):
			return {
				'status'	:	True
				, 'data'	:	res
			}
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_no_records_found']
			}


	def backupDatabase(self):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		try:
			bdir = fn.configs.__PACKAGE_PATH__ + '\\_backups\\'
			bfile = bdir + 'db_backup.sql'

			try:
				fn.configs.os.mkdir(bdir)
			except FileExistsError:
				pass

			cmd = 'mysqldump -u {} -p{} --databases {} > {}'.format(
					fn.configs.__DB_USER__
					, fn.configs.__DB_PASS__
					, fn.configs.__DB_NAME__
					, bfile
			)

			fn.showCountDown(fn.lang_dict['backup_starts_in'], 2)
			print('\n')

			fn.configs.os.system(cmd)
			
			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['backup_successful_and_located_at'] + ' \'' + bfile + '\''
			}
		except:
			fn.makeErrorLog()
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['failed_to_backup']
			}
	
	def resetDatabase(self):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}

		if fn.importInitials(self.__db, True):
			fn.configs.os.remove(fn.configs.__RUN_INFO_FILE__)
			exit()
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_something_went_wrong_pls_try_again_later']
			}

	def changeStationStatus(self, sid, status, reason):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}
		
		try:
			q = 'UPDATE station_close_status SET status = {}, reason = \'{}\' WHERE station_id = \'{}\''.format(
				status, reason, sid
			)

			self.__cur.execute(q)
			self.__db.commit()

			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['station_status_changed_successfully']
			}
		except:
			fn.makeErrorLog()
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_failed_to_change_station_status']
			}
			
	def viewStationStatus(self, sid):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_admin_not_logged_in']
			}
		
		try:
			q = 'SELECT s.station_name, c.status, c.reason FROM stations s, station_close_status c WHERE c.station_id = \'{}\' and c.station_id = s.station_id;'.format(
				sid
			)

			self.__cur.execute(q)
			d = self.__cur.fetchall()

			n = d[0][0]
			r = d[0][2]

			if d[0][1] == 0:
				s = fn.lang_dict['closed']
				msg = (fn.lang_dict['status_for']
						+ ' \"' + n + '\" '
						+ fn.lang_dict['is']
						+ ' \"' + s + '\" '
						+ fn.lang_dict['due_to_the_reason']
						+ ' \"' + r + '\"'
				)
			else:
				s = fn.lang_dict['open']
				msg = (fn.lang_dict['status_for']
						+ ' \"' + n + '\" '
						+ fn.lang_dict['is']
						+ ' \"' + s + '\" '
				)

			return {
				'status'	:	True
				, 'msg'		:	msg
			}
		except:
			if fn.configs.__DEBUG__:
				fn.makeErrorLog()

			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_failed_to_view_station_status']
			}
			
