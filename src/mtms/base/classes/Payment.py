"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

# important imports
from ..functions import functions as fn

class Payment():
	isSuccess   	=   None
	isCanclled  	=   None

	__db	=	None
	__cur	=	None

	__amount_r__		=   0
	__to_charge__		=	0
	__max_to_charge__	=	0
	__modes__	=	{
		0	:	fn.lang_dict['text_upi']
		, 1	:	fn.lang_dict['text_debit_credit_card']
		, 2	:	fn.lang_dict['text_cash']
	}

	def __init__(self, db):
		self.__db	=	db
		self.__cur	=	self.__db.cursor()

	def __selectMode(self):
		sr = 1
		for i in self.__modes__:
			print(sr, ') ', self.__modes__[i], sep = '')
			sr += 1
		
		opt = (int(input('\n' + fn.lang_dict['enter_choose_pay_mode'] + ': ')) - 1)

		self.__pay_mode__ = opt

	def __takeAmount_and_Proceed(self):
		amt = float(input('\n' + fn.lang_dict['enter_amt_to_be_taken'] + ': '))
		self.__amount_r__ = amt
		
		if fn.ask(fn.lang_dict['are_you_sure_to_make_payment_of'] + ' ' + str(amt)):
			if self.__amount_r__ > self.__max_to_charge__:
				print('\n' + fn.lang_dict['warn_given_amt_exceeds_limit_which_is'] + ': ' + str(fn.configs.__MAX_CARD_RECHARGE_AMOUNT__))
				self.isSuccess  =   False
				self.isCanclled =   True
			else:
				self.isSuccess      =   True
				self.isCanclled     =   False
		else:
			self.isSuccess  =   False
			self.isCanclled =   True

	def __confirmAmt_and_Proceed(self):
		if fn.ask(fn.lang_dict['are_you_sure_to_make_payment_of'] + ' ' + str(self.__to_charge__)):
			self.isSuccess      =   True
			self.isCanclled     =   False
		else:
			self.isSuccess  =   False
			self.isCanclled =   True

	def setAmount(self, to_charge):
		self.__to_charge__ = to_charge

	def setMaxAmount(self, max_to_charge):
		self.__max_to_charge__ = max_to_charge

	def amountRecived(self):
		return self.__amount_r__

	def creditAmount(self):
		self.__selectMode()

		# select payment mode
		if self.__pay_mode__ == 0:
			upi_id = input('\n' + fn.lang_dict['enter_upi_id'] + ': ')

			t = {
				'mode'		:	'upi'
				, 'upi_id'	:	upi_id
			}

		elif self.__pay_mode__ == 1:
			card_no = int(input('\n' + fn.lang_dict['enter_card_number'] + ': '))
			card_exp = input('\n' + fn.lang_dict['enter_card_expiry'] + ': ')
			cvv = int(input('\n' + fn.lang_dict['enter_card_cvv'] + ': '))

			# clearing cvv for security
			cvv = 000
			del cvv

			t = {
				'mode'		:	'netBanking'
				, 'card_no'	:	str(card_no)[-1:-5]
				, 'card_exp':	card_exp
			}

		elif self.__pay_mode__ == 2:
			t = {
				'mode'	:	'cash'
			}

		# pay and go
		if self.__to_charge__ != 0:
			self.__confirmAmt_and_Proceed()
		else:
			self.__takeAmount_and_Proceed()

		t['trans_id']	=	fn.generateId()
		t['amount']		=	self.__to_charge__ or self.__amount_r__

		self.__cur.execute(
			fn.insertInTableCmd(
				'transactions'
				, list(t.keys())
				, [
					list(t.values())
				]
			)
		)

		return False
