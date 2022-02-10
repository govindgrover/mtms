"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# important imports
from ..functions import functions as fn
from .Payment import Payment

class Counter():
	__login_status__	=   False
	__db				=   None
	__cur				=   None

	def __init__(self, db):
		self.__db   =	db
		self.__cur  =	self.__db.cursor()

	def __isCardExists(self, card_id):
		if not(self.__login_status__):
			return

		self.__cur.execute(
			'SELECT COUNT(*) FROM cards WHERE card_id = \'{}\' AND is_active = 1;'.format(
				card_id
			)
		)

		t = self.__cur.fetchall()

		if len(t) > 0 and len(t[0]) > 0 and t[0][0] > 0:
			return True
		else:
			return False

	def login(self, username, password):
		q = 'SELECT * FROM users WHERE name = \'{}\' and password = \'{}\' and role = 1;'.format(
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

	def getCardBalance(self, cid, amt_only = False):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_counter_not_logged_in']
			}

		if not self.__isCardExists(cid):
			if amt_only:
				return 0
			else:
				return {
					'status': False
					, 'msg'	: fn.lang_dict['warn_no_such_card_found']
				}

		self.__cur.execute(
			'SELECT bal FROM cards WHERE card_id = \'{}\''.format(
				cid
			)
		)

		if amt_only:
			return self.__cur.fetchall()[0][0]
		else:
			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['balance_in_the_card'] + ' ₹' + str(self.__cur.fetchall()[0][0])
			}

	def printCard(self, cid):
		# doing operations on the file
		f_path = fn.configs.os.path.join(
					fn.configs.os.environ["HOMEDRIVE"]
					, fn.configs.os.environ["HOMEPATH"]
					, (fn.configs.__PACKAGE_NAME__ + '_cards')
		)

		try:
			fn.configs.os.mkdir(f_path)
		except FileExistsError:
			pass

		f_name = (f_path + '\\card-' + str(cid) + '.txt')

		f = open(f_name, 'w')

		f.write('CARD NUMBER: ' + str(cid) + '\n')
		f.write('ACTIVE BALANCE: ' + str(self.getCardBalance(cid, True)) + '\n')

		f.close()

		return f_name

	def buyNewCard(self):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_counter_not_logged_in']
			}

		pay = Payment(self.__db)
		pay.setAmount(
			fn.configs.__MIN_CARD_RECHARGE_AMOUNT__
		)
		pay.creditAmount()

		if pay.isSuccess:
			_id = fn.generateId()

			# default bal is in configs.py; is_active = 1; is_archived = 0;
			self.__cur.execute(
				fn.insertInTableCmd(
					'cards'
					, ['card_id', 'bal']
					, [
						[
							_id
							, (fn.configs.__MIN_CARD_RECHARGE_AMOUNT__ - fn.configs.__NEW_CARD_SECURITY__)
						]
					]
				)
			)
			self.__db.commit()
			
			fn.showQR(_id)

			if fn.ask(fn.lang_dict['want_to_print_the_card_number']):
				print(
					'\n'
					, fn.lang_dict['your_card_is_located_at']
					, ': \''
					, self.printCard(
						_id
					)
					, '\''
					, sep = ''
				)

				return {
					'status'	:	True
					, 'msg'		:	fn.lang_dict['your_card_id_is'] + ' ' + _id
				}
			else:
				return {
					'status'	:	True
					, 'msg'		:	fn.lang_dict['your_card_id_is'] + ' ' + _id
				}
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_could_not_make_payment']
			}

	def rechargeCard(self, cid):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_counter_not_logged_in']
			}

		if not self.__isCardExists(cid):
			return {
				'status': False
				, 'msg'	: fn.lang_dict['warn_no_such_card_found']
			}

		pay = Payment(self.__db)
		pay.setMaxAmount(fn.configs.__MAX_CARD_RECHARGE_AMOUNT__)
		pay.creditAmount()

		if pay.isSuccess:
			self.__cur.execute(
				'UPDATE cards SET bal = bal + {} WHERE card_id = \'{}\';'.format(
					pay.amountRecived(), cid
				)
			)
			self.__db.commit()

			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['card_successfully_recharged']
			}
		else:
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_could_not_make_payment']
			}

	def refundCard(self, cid):
		if not(self.__login_status__):
			return {
				'status'	:	False
				, 'msg'		:	fn.lang_dict['warn_counter_not_logged_in']
			}

		if not self.__isCardExists(cid):
			return {
				'status': False
				, 'msg'	: fn.lang_dict['warn_no_such_card_found']
			}

		# returning the balance to the card-holder and taking appr. actions on the bal 
		bal = self.getCardBalance(cid, True)

		if bal < 0:
			return {
				'status':	False
				, 'msg'	:	fn.lang_dict['warn_your_card_have_neg_balance_of'] + ' ₹ ' + str(bal) + ', ' + fn.lang_dict['please_pay_to_refund_the_card']
			}
		else:
			self.__cur.execute(
				'UPDATE cards SET bal = 0, is_active = 0 WHERE card_id = \'{}\';;'.format(
					cid
				)
			)
			self.__db.commit()

			return {
				'status'	:	True
				, 'msg'		:	fn.lang_dict['card_refunded_successfully_with_a_return_balance_of'] + ' ₹' + str(bal)
			}
