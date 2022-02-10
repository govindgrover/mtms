"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

from .. import configs
from ..functions import functions as fn
from ..classes import CardOperation
from ..classes import TokenOperation

co = CardOperation.CardOperation(fn.db)
to = TokenOperation.TokenOperation(fn.db)

def touch():
	c = fn.checkStationTimmings()

	if not c['status']:
		print('\n', c['msg'], sep = '')
		return

	_id = input(fn.lang_dict['enter_card_or_token_id'] + ': ')

	print()
	if to.isToken(_id):
		print(
			to.onTouch(_id)['msg']
		)
	elif co.isCard(_id):
		srch = input(fn.lang_dict['enter_station_name_to_search'] + ': ')
		current_station = fn.searchStations(fn.db, srch)

		print(
			co.onTouch(_id, current_station)['msg']
		)
	else:
		print(fn.lang_dict['invalid_id'])

def getToken():
	c = fn.checkStationTimmings()

	if not c['status']:
		print('\n', c['msg'], sep = '')
		return

	print('(' + fn.lang_dict['enter_asterisk_for_searching_all_stations'] + ')\n')

	f = input(fn.lang_dict['search_station_for_start_point'] + ': ')
	f_id = fn.searchStations(fn.db, f)

	# checking station closure
	c = fn.checkStationClosure(fn.db, f_id)

	if c['status']:
		print('\n' + c['msg'])
		return

	t = input('\n' + fn.lang_dict['search_station_for_end_point'] + ': ')
	t_id = fn.searchStations(fn.db, t)

	# checking station closure
	c = fn.checkStationClosure(fn.db, t_id)

	if c['status']:
		print('\n' + c['msg'])
		return

	if t_id == '' or f_id == '':
		print(fn.lang_dict['invalid_choice'])
		return

	mg = to.buyToken(f_id, t_id)['msg']

	if mg != '':
		print(
			'\n' + mg
		)

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()


