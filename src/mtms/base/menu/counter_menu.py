"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

from .. import configs as conf
from ..functions import functions as fn
from ..classes import Counter

co = Counter.Counter(fn.db)

if conf.__DEBUG__:
	co.login('counter', 'counter')

def login():
	n = input(fn.lang_dict['enter_counter_username'] + ': ')
	p = input(fn.lang_dict['enter_counter_password'] + ': ')

	print()
	print(
		co.login(n, p)['msg']
	)

def logout():
	if fn.ask(fn.lang_dict['are_you_sure']):
		print()
		print('\n'
			+ co.logout()['msg']
			)

def getBalance():
	_id = input(fn.lang_dict['enter_card_id'] + ': ')
	
	print()
	print('\n'
		+ co.getCardBalance(_id)['msg']
	)

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def buyCard():
	print()
	print('\n'
		+ co.buyNewCard()['msg']
	)

	print('\n', fn.lang_dict['press_enter_to_continue'], '...', sep = '')
	input()

def rechargeTheCard():
	_id = input(fn.lang_dict['enter_card_id'] + ': ')
	
	print()
	print('\n'
		+ co.rechargeCard(_id)['msg']
	)

def refundTheCard():
	_id = input(fn.lang_dict['enter_card_id'] + ': ')
	
	print()
	print('\n'
		+ co.refundCard(_id)['msg']
	)
