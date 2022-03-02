"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

from .. import configs

def get_runs_upto():
	with open(configs.__RUN_INFO_FILE__, 'br') as f:
		try:
			while True:
				r = configs.pickle.load(f)
				print('Software ran', r, 'times since last reset or since installed')
				return r
		except:
			pass

def showCountDown(text, t):
	i = t
	print()

	while i != 0:
		print(text, str(i - 1), lang_dict['seconds'], '\r', end = '')
		configs.time.sleep(1)
		i -= 1

def ask(q):
	try:
		if input('\n' + str(q) + ' [y | n]: ') in ('Y', 'y'):
			return True
		else:
			return False
	except KeyboardInterrupt:
		return False

def printHeading(tree, width,sep_times = 5):
	# making something like :: Menu > Sub > sub-sub > ...
	s = ''
	for i in tree:
		if (i == tree[0]):
			s += i
		else:
			s += ' > ' + i

	# making something like :: ************** .......
	tb = width * '*'

	# counting spaces to put brfore and after the 's'
	spc = width - (len(s) + (2 * sep_times))

	if spc % 2 != 0:
		spc -= 1
	
	spc //= 2

	m = ('*' * sep_times) + (spc * ' ') + s + (spc * ' ') + ('*' * sep_times)

	# for clock
	time_struct = configs.time.localtime()
	time = (
			str(time_struct.tm_mday)
			+ '/' + str(time_struct.tm_mon)
			+ '/' + str(time_struct.tm_year)
			+ ' ' + str(time_struct.tm_hour)
			+ ':' + str(time_struct.tm_min)
	)
	time_spc = ((width - len(time)) * ' ')

	print()
	configs.os.system('cls')
	print(tb + '\n' + m + '\n' + tb + '\n')

	print(time_spc + time)

def insertInTableCmd(tbl_name, arr_col, arr_val):
	q = 'INSERT INTO ' + tbl_name + '('
	
	for i in arr_col:
		q += i

		if arr_col.index(i) != (len(arr_col) - 1):
			q += ', '
	else:
		i = None
		q += ') VALUES'

	for z in arr_val:
		theLast = False
		m = 0

		q += '('

		if not(type(z) in (str, list, tuple, set)):
			z = str(z)

		for i in z:
			m += 1
			if m == len(z):
				theLast = True

			if type(i) == str:
				q += '\'' + i + '\''
			else:
				q += str(i)

			if not theLast:
				q += ', '
		else:
			q += ')'

			if z == arr_val[-1]:
				q += ';'
			else:
				q += ', '

	return q

def generateId():
	return str(
		configs.uuid.uuid4()
	)

def isInDB(db, tbl_name, col_name, val):
	cur = db.cursor()

	cur.execute(
		'SELECT COUNT(*) FROM {} WHERE {} = \'{}\';'.format(
			tbl_name, col_name, val
		)
	)

	r = cur.fetchall()[0]

	if len(r) > 0 and r[0] > 0:
		return True
	else:
		return False

def checkStationTimmings():
	if configs.__DEBUG__:
		return {
			'status':	True
			, 'msg'	:	lang_dict['you_are_welcome']
		}

	if configs.__TRAIN_TIME_START__ <= configs.time.localtime().tm_hour <= configs.__TRAIN_TIME_END__:
		return  {
			'status':	True
			, 'msg'	:	lang_dict['you_are_welcome']
		}
	else:
		return {
			'status':	False
			, 'msg'	:	lang_dict['stations_are_closed_from']
						+ ' '
						+ str(configs.__TRAIN_TIME_END__)
						+ ' '
						+ lang_dict['to']
						+ ' '
						+ str(configs.__TRAIN_TIME_START__)
						+ ' '
						+ lang_dict['hours']
		}

def getAllRoutes(db):
	cur = db.cursor()
	rt_dict = dict()

	cur.execute('SELECT route_id, route_name FROM routes;')
	rts = cur.fetchall()

	if not(len(rts) <= 0):
		for x in rts:
			rt_dict[x[0]] = x[1]

	return rt_dict

def getAllStations(db):
	cur = db.cursor()
	st_dict = dict()

	cur.execute('SELECT station_id, station_name FROM stations;')
	sts = cur.fetchall()

	if not(len(sts) <= 0):
		for x in sts:
			st_dict[x[0]] = x[1]

	return st_dict

def searchStations(db, like_name):
	from ..classes import ConsoleTable

	table = ConsoleTable.ConsoleTable()
	cur = db.cursor()

	like_name = like_name.strip()

	if like_name == '*':
		q = 'SELECT s.id, s.station_id, s.station_name, r.route_name FROM stations s, routes r WHERE s.route_id = r.route_id ORDER BY station_name ASC;'
	else:
		q = 'SELECT s.id, s.station_id, s.station_name, r.route_name FROM stations s, routes r WHERE station_name LIKE \'%{}%\' AND s.route_id = r.route_id ORDER BY station_name ASC;'.format(
			like_name
		)

	cur.execute(q)
	res = cur.fetchall()

	if len(res) <= 0:
		print(lang_dict['no_such_station_found'])
		return ''
	
	data_to_show = list()
	t = list()

	for r in res:
		i = 0
		for c in r:
			if i != 1:
				t.append(c)
			i += 1
		data_to_show.append(t)
		t = list()

	table.setColumnHeaders(
		[
			lang_dict['serial_id'] + '#'
			, lang_dict['station_name']
			, lang_dict['route_name']
		]
	)
	table.setRows(data_to_show)
	table.createTable()

	opt_id = input('\n' + lang_dict['enter_your_choice_from_serial_id_column'] + ': ')

	for x in res:
		if opt_id == str(x[0]):
			return x[1]
		else:
			continue
	else:
		return ''

def searchRoutes(db, like_name):
	from ..classes import ConsoleTable

	table = ConsoleTable.ConsoleTable()
	cur = db.cursor()

	like_name = like_name.strip()

	if like_name == '*':
		q = 'SELECT id, route_id, route_name FROM routes ORDER BY route_name ASC;'
	else:
		q = 'SELECT id, route_id, route_name FROM routes WHERE route_name LIKE \'%{}%\' ORDER BY route_name ASC;'.format(
			like_name
		)

	cur.execute(q)
	res = cur.fetchall()

	if len(res) <= 0:
		print(lang_dict['no_such_route_found'])
		return ''
	
	data_to_show = list()
	t = list()

	for r in res:
		i = 0
		for c in r:
			if i != 1:
				t.append(c)
			i += 1
		data_to_show.append(t)
		t = list()

	table.setColumnHeaders(
		[
			lang_dict['serial_id'] + '#'
			, lang_dict['route_name']
		]
	)
	table.setRows(data_to_show)
	table.createTable()

	opt_id = input('\n' + lang_dict['enter_your_choice_from_serial_id_column'] + ': ')

	for x in res:
		if opt_id == str(x[0]):
			return x[1]
		else:
			continue
	else:
		return ''

def showQR(txt, showTxt = False):
	if not configs.__USE_QR__:
		return 

	o = configs.pyqrcode.create(str(txt))

	configs.os.system('cls')

	print('\n' + lang_dict['scan_to_save_code'] + '\n')
	print(o.terminal(module_color = 'white', background = 'black', quiet_zone = 1))

	if showTxt:
		print(txt)

def checkStationClosure(db, sid):
	c = db.cursor()

	q = 'SELECT s.station_name, c.status, c.reason FROM stations s, station_close_status c WHERE c.station_id = \'{}\' and c.station_id = s.station_id;'.format(
		sid
	)

	try:
		c.execute(q)
		res = c.fetchall()[0]

		if res[1] == 1:
			return {
				'status': False
				, 'msg' : lang_dict['all_ok']
			}
		else:
			return {
				'status': True
				, 'msg' : (lang_dict['status_for']
								+ ' \"' + res[0] + '\" '
								+ lang_dict['is']
								+ ' \"closed\" '
								+ lang_dict['due_to_the_reason']
								+ ' \"' + res[2] + '\"'
				)
			}
	except:
		pass

	return {
		'status': True
		, 'msg' : lang_dict['please_choose_the_station_from_the_selected_above_only']
	}

# *********************************************************
db = None
lang_dict = None

def makeErrorLog():
	dtnow = str(configs.datetime.datetime.now())
	t = dtnow.split()[0].split('-')

	try:
		configs.os.mkdir(configs.__LOGS_PATH__)
	except FileExistsError:
		pass

	fname = configs.__LOGS_PATH__ + '\\' + configs.__PACKAGE_NAME__ + '_errors_' + t[0] + '_' + t[1] + '_' + t[2] + '.log'

	f = open(fname, 'a', encoding = 'utf-8')

	e1, e2, e3 = configs.sys.exc_info()

	err = configs.traceback.format_exception(
		e1, e2, e3
	)

	pre = '\n[ ' + dtnow + ' ] '
	f.write(pre + err[-1] + '\n')
	for i in range(len(err) - 1):
		f.write(err[i])

	f.close()

	return fname

def setWorkingLang(dft = False):
	try:
		if not dft:
			langs = configs.__LANG_CHOICES__

			printHeading(['अपनी भाषा चुनें | Choose your language '], configs.__SCREEN_WIDTH__)

			for x in langs:
				print(x, ') ', langs[x], sep = '')
			print(
				(
					len(
						max(langs.values()
						)
					)
				* 2
				) * '-'
			)
			print('e) Exit')

			try:
				opt = input('\nEnter provided serial: ')
			except KeyboardInterrupt:
				exit('\nBye! :)')

			if (opt not in configs.__LANG_CHOICES__):
				if (opt == 'e'):
					exit('\nBye! :)')

				print('\nProvided language not found, switching to default language...')

				default_lang_file = open(configs.__DEFAULT_LANG_FILE__, 'r')
				ch_lang = configs.json.load(default_lang_file)
			else:
				lang_file = open(configs.__LANG_PATH__ + '\\' + opt + '.json', 'r', encoding = 'utf-8')
				ch_lang = configs.json.load(lang_file)
		else:
			default_lang_file = open(configs.__DEFAULT_LANG_FILE__, 'r')
			ch_lang = configs.json.load(default_lang_file)

	except KeyboardInterrupt:
		print('\n' + lang_dict['process_declined_by_user'])
		exit()

	return ch_lang

def importInitials(db = None, isReset = False):
	if db == None:
		print('\n' + lang_dict['please_provide_correct_database_information_in_the_config_file'])
		return False

	if isReset:
		printHeading(['सिस्टम कॉन्फ़िगरेशन | System Configration', 'रीसेट | Reset'], configs.__SCREEN_WIDTH__)
		print('\n' + lang_dict['warning_system_setup_is_disturbed_please_allow_to_resetup'] + '!!')

		if not ask(lang_dict['continue_reset_process']):
			exit()

		configs.os.remove(configs.__RUN_INFO_FILE__)
		isFirstLanuch()
	else:
		printHeading(['सिस्टम कॉन्फ़िगरेशन | System Configration', 'सेटअप | Setup'], configs.__SCREEN_WIDTH__)
		print('\n' + lang_dict['warn_setup_required_for_first_launch_of_the_system'] + '!')

		if not ask(lang_dict['continue_setup_process']):
			exit()
	
	# checking and setting up database
	fname = configs.__DB_STRUCT_FILE__
	c = db.cursor()

	with open(fname, 'r', encoding='utf8') as f:
		for x in f.read().split(';'):
			try:
				c.execute(x + ';')
			except:
				pass

	# checking and setting up lang options
	temp = 0
	for x in configs.__LANG_CHOICES__:
		try:
			open(
				configs.__LANG_PATH__ + '\\' + x + '.json'
				, 'r'
			)
		except FileNotFoundError:
			temp += 1
	else:
		if temp != 0:
			try:
				open(
					configs.__DEFAULT_LANG_FILE__
					, 'r'
				)
			except FileNotFoundError:
				raise Exception('Provided and default language files not found!')

	print(lang_dict['please_restart_the_console_and_try_again'])
	return True

def isFirstLanuch():
	pk =  configs.pickle

	try:
		f = open(configs.__RUN_INFO_FILE__, 'br+')
		flag = pk.load(f)
		flag += 1

		f.seek(0)

		pk.dump(flag, f)
	except FileNotFoundError:
		f = open(configs.__RUN_INFO_FILE__, 'bw')
		d = 1
		flag = None

		pk.dump(d, f)
	
	f.close()

	if flag == None:
		return True
	else:
		return False

def firstThingsFirst():
	configs.os.system('cls')
	global db, lang_dict

	# setting working langauge for current
	# session as default to show some massages
	lang_dict = setWorkingLang(True)

	print('\n' + lang_dict['notice_please_wait_while_performing_checks'])

	try:
		db = configs.mysql.connector.connect(
			user		=	configs.__DB_USER__
			, password	=	configs.__DB_PASS__
			, host		=	configs.__DB_HOST__
			, database	=	configs.__DB_NAME__
		)
	except configs.mysql.connector.Error as err:

		# creating required database in the mysql
		# for this software
		if err.errno == configs.mysql.connector.errorcode.ER_BAD_DB_ERROR:			
			db = configs.mysql.connector.connect(
				user		=	configs.__DB_USER__
				, password	=	configs.__DB_PASS__
				, host		=	configs.__DB_HOST__
			)
			db.cursor().execute('create database ' + configs.__DB_NAME__ + ';')
			db.cursor().execute('USE ' + configs.__DB_NAME__ + ';')
			db.commit()
		else:
			raise Exception(lang_dict['error_failed_to_connect_database'] + 'MySQL Error Code is \'' + str(err.errno) + '\'')

	if isFirstLanuch():
		importInitials(db)
		firstThingsFirst()
		return

	# setting working langauge for current
	# session acc. to user choice
	if configs.__DEBUG__:
		lang_dict = setWorkingLang(True)
	else:
		lang_dict = setWorkingLang()

	c = db.cursor()
	c.execute('show tables;')
	res = c.fetchall()

	# beautfying the fetched mysql tuples 
	n = list()
	for t in res:
		n.append(t[0])

	for x in configs.__REQ_DB_TABLES__:
		if x not in n:
			importInitials(db, True)
			exit()
