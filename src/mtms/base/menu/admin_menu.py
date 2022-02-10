"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

from .. import configs as conf
from ..functions import functions as fn
from ..classes import Admin
from ..classes import ConsoleTable

table = ConsoleTable.ConsoleTable()
ad = Admin.Admin(fn.db)

if conf.__DEBUG__:
	ad.login('admin', 'admin')

def login():
	n = input(fn.lang_dict['enter_admin_username'] + ': ')
	p = input(fn.lang_dict['enter_admin_password'] + ': ')

	print()
	print(ad.login(n, p)['msg'])

def logout():
	if fn.ask(fn.lang_dict['are_you_sure']):
		print('\n', ad.logout()['msg'], sep = '')


def addNewUser():
	username	=	input(fn.lang_dict['enter_usrname'] + ': ')
	email		=	input(fn.lang_dict['enter_email'] + ': ')
	password	=	input(fn.lang_dict['enter_password'] + ': ')
	role		=	int(input(fn.lang_dict['enter_role_0_admin_1_counter'] + ': '))

	print()
	if len(username) < 6 or len(password) < 6:
		print(fn.lang_dict['warn_name_email_pass_too_short_length'])
		return
	elif role not in (0, 1):
		print(fn.lang_dict['warn_please_provide_correct_rollno'])
		return

	print('\n'
		+ ad.addAccount(
			username
			, email
			, password
			, role
		)['msg']
	)

def addNewRoute():
	name = input(fn.lang_dict['enter_new_route_name'] + ': ')

	if len(name) < 6:
		print('\n' + fn.lang_dict['warn_min_length_is_6_char'])
		return

	print()
	print('\n' + ad.addRoute(name)['msg'])

def addNewStation():
	print('(' + fn.lang_dict['enter_asterisk_for_searching_all_stations'] + ')\n')

	print('\n' + fn.lang_dict['choose_route_on_which_the_new_station_will_be_placed'])

	srch = input('\n' + fn.lang_dict['enter_route_name_to_search'] + ': ')
	route = fn.searchRoutes(fn.db, srch)

	if not len(route):
		print('\n' + fn.lang_dict['warn_no_route_found'])
		return
	else:
		name = input(fn.lang_dict['enter_new_station_name'] + ': ')

		if len(name) < 6:
			print('\n' + fn.lang_dict['warn_min_length_is_6_char'])
			return

	print('\n\n'
		+ ad.addStation(
			name
			, route
		)['msg']
	)

def renameTheRoute():
	print('(' + fn.lang_dict['enter_asterisk_for_searching_all_stations'] + ')\n')

	srch = input(fn.lang_dict['enter_route_name_to_search'] + ': ')
	route = fn.searchRoutes(fn.db, srch)

	print()
	new = input(fn.lang_dict['enter_new_name_for_selected_route'] + ': ')

	if len(new) < 6:
		print('\n' + fn.lang_dict['warn_min_length_is_6_char'])
		return

	print()
	print('\n' + ad.renameRoute(route, new)['msg'])

def renameTheStation():
	print('(' + fn.lang_dict['enter_asterisk_for_searching_all_stations'] + ')\n')

	srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
	station = fn.searchStations(fn.db, srch)

	print()
	new = input(fn.lang_dict['enter_new_name_for_selected_station'] + ': ')

	if len(new) < 6:
		print('\n' + fn.lang_dict['warn_min_length_is_6_char'])
		return

	print()
	print('\n' + ad.renameStation(station, new)['msg'])

def changeFares():
	print('(' + fn.lang_dict['enter_asterisk_for_searching_all_stations'] + ')\n')

	srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
	_from = fn.searchStations(fn.db, srch)

	print()

	srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
	_to = fn.searchStations(fn.db, srch)

	print()
	new = float(input(fn.lang_dict['enter_new_fare_for_the_selcted'] + ': ₹'))

	print()
	print('\n'
		+ ad.modifyStationFares(_from, _to, new)['msg']
	)

def showAllRoutesAndStations():
	rs = ad.getAllRoutesAndStations()
	if rs['status']:
		if len(rs['data'][0]) == 1:
			table.setColumnHeaders(fn.lang_dict['routes'])
		elif len(rs['data'][0]) == 2:
			table.setColumnHeaders([
				fn.lang_dict['stations']
				, fn.lang_dict['routes']
			])

		table.setRows(rs['data'])
		table.createTable()

		print(fn.lang_dict['total_rows_are'], '=', len(rs['data']))
	else:
		print(rs['msg'])
	
	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def showAllUsers():
	u = ad.getAllUsers()

	if u['status']:
		table.setColumnHeaders([
			fn.lang_dict['username']
			, fn.lang_dict['email-id']
			, fn.lang_dict['role']
		])
		table.setRows(u['data'])
		table.createTable()
		print(fn.lang_dict['total_rows_are'], '=', len(u['data']))

		print('\n' + fn.lang_dict['role_0_admin_1_counter'])
	else:
		print(u['msg'])

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def takeBackup():
	print(ad.backupDatabase()['msg'])

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def modifyStationStatus():
	srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
	station = fn.searchStations(fn.db, srch)
	sts, rsn = None, None

	for i in range(3):
		sts = input(fn.lang_dict['enter_changed_status'] + ': ')

		if sts not in ('0', '1'):
			print('\n' + fn.lang_dict['warn_provide_correct_status'])
			continue

		print()
		rsn = (input(fn.lang_dict['enter_reason_for_closed_station_max_512_chars_min_10'] + ':\n')).strip()

		if len(rsn) < 10:
			print('\n' + fn.lang_dict['warn_length_of_reason_too_short'])
			continue

		break
	
	if sts != None and rsn != None:
		print(
			'\n', ad.changeStationStatus(station, int(sts), rsn)['msg']
			, sep = ''
		)
	else:
		print('\n', fn.lang_dict['warn_something_went_wrong_pls_try_again'], sep = '')

def viewStationStatus():
	srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
	station = fn.searchStations(fn.db, srch)

	print(
		'\n'
		, ad.viewStationStatus(station)['msg']
		, sep = ''
	)

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def resetEverthing():
	if fn.ask(fn.lang_dict['are_you_sure']):
		ad.resetDatabase()
	else:
		print(fn.lang_dict['process_declined_by_user'])
