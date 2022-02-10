"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

class ConsoleTable():
	__col_headers__		=	list()
	__col_max_length__	=	list()
	__rows__			=	list()

	def __init__(self):
		pass

	def __sumUpLengths(self):
		# my appox-imation formula
		s = (len(self.__col_headers__) * 3) + 1

		for i in self.__col_max_length__:
			s += i

		return s

	def __makeListOfLengthOfEachInnerListItem(self):
		mx = []
		colArr = []

		# taking each row from array of rows
		for row in self.__rows__:

			# taking each col from the row
			i = 0
			for col in row:
				l = len(col)

				lch = len(self.__col_headers__[i])
				if lch > l:
					colArr.append(lch)
				else:
					colArr.append(l)

				i += 1

			# adding to main array
			mx.append(colArr)

			# nullifying initials
			colArr = []

		return mx

	def __getListOfThisIndexFromInnerLists(self, arr, index):
		z = list()
		for i in arr:
			z.append(i[index])

		return z

	def __setAutoMaxLengths(self):
		m = list()
		for i in range(len(self.__col_headers__)):
			m.append(max(
				self.__getListOfThisIndexFromInnerLists(
					self.__makeListOfLengthOfEachInnerListItem()
					, i)
			))

		self.__col_max_length__ = tuple(m)

	def __checkData(self):
		if (len(self.__col_headers__) == 0 and len(self.__rows__) == 0):
			return False

		return True

	"""
	@function	:	setColumnHeaders
	@description:	sets the headers for the table
	@params		:	cols <list of headers>
	"""
	def setColumnHeaders(self, cols):
		self.__col_headers__ = tuple(cols)

	"""
	@function	:	setRows
	@description:	sets the data/ row(s). It must match the headers indexing
	@params		:	rows <list of list of rows as per headers>
	"""
	def setRows(self, rows):
		# strfying each col data and striping
		temp_col = list()
		temp_row = list()

		for r in rows:
			for c in r:
				temp_col.append((str(c)).strip())
			else:
				temp_row.append(temp_col)
				temp_col = list()

		self.__rows__ = tuple(temp_row)
		self.__setAutoMaxLengths()

	"""
	@function	:	createTable
	@description:	prints the table on the screen
	"""
	def createTable(self):
		if (not(self.__checkData())):
			raise Exception('Data not provided!')

		# setting headers
		print(self.__sumUpLengths() * '-')

		head_index = 0
		for head in self.__col_headers__:
			a = self.__col_max_length__[head_index]
			a -= len(head)

			hr = head + (a *  ' ')

			if head_index == 0:
				print('| ' + hr, end = ' | ')
			else:
				print(hr, end = ' | ')
			
			head_index += 1
		else:
			del head_index
		# end setting headers

		# setting rows
		print('\n', (self.__sumUpLengths() * '-'), '\n', sep = '', end = '')

		for r in self.__rows__:
	
			col_index = 0
			for col in r:
				a = self.__col_max_length__[col_index]
				a -= len(col)

				hr = col + (a *  ' ')

				if col_index == 0:
					print('| ' + hr, end = ' | ')
				else:
					print(hr, end = ' | ')
			
				col_index += 1
			
			print('\n', end='')
		# end setting rows

		print(self.__sumUpLengths() * '-')
