"""
	@author: Govind Grover
	@description: Metro Train Management System (MTMS)
"""

from ..functions import functions as fn

admin_view = {
	'login'						:	fn.lang_dict['login']
	, 'logout'					:	fn.lang_dict['logout']
	, 'null_1'					:	'--------------------------------'
	, 'showAllUsers'			:	fn.lang_dict['show_all_users']
	, 'showAllRoutesAndStations':	fn.lang_dict['show_all_routes_amp_stations']
	, 'null_2'					:	'--------------------------------'
	, 'addNewUser'				:	fn.lang_dict['create_account']
	, 'addNewRoute' 			:	fn.lang_dict['add_route']
	, 'addNewStation' 			:	fn.lang_dict['add_station']
	, 'null_3'					:	'--------------------------------'
	, 'renameTheRoute'			:	fn.lang_dict['modify_route_name']
	, 'renameTheStation' 		:	fn.lang_dict['modify_station_name']
    , 'changeFares' 	    	:	fn.lang_dict['modify_station_fare']
	, 'null_4'					:	'--------------------------------'
	, 'viewStationStatus'		:	fn.lang_dict['view_station_status']
	, 'modifyStationStatus' 	:	fn.lang_dict['modify_station_status']
	, 'null_5'					:	'--------------------------------'
    , 'takeBackup' 	    		:	fn.lang_dict['take_backup']
    , 'resetEverthing' 	    	:	fn.lang_dict['reset_system']
	, 'null_6'					:	'--------------------------------'
	, 'back'					:	fn.lang_dict['go_back']
	, 'exit'					:	fn.lang_dict['exit']
}

counter_view = {
	'login'				:	fn.lang_dict['login']
	, 'logout'			:	fn.lang_dict['logout']
	, 'null_1'				:	'--------------------------------'
	, 'buyCard'			:	fn.lang_dict['buy_new_card']
	, 'refundTheCard'	:	fn.lang_dict['refund_card']
	, 'null_2'				:	'--------------------------------'
	, 'rechargeTheCard'	:	fn.lang_dict['recharge_card']
	, 'getBalance'		:	fn.lang_dict['check_card_balance']
	, 'null_3'				:	'--------------------------------'
	, 'back'			:	fn.lang_dict['go_back']
	, 'exit'			:	fn.lang_dict['exit']
}

customer_view = {
	'touch'				:	fn.lang_dict['enter_card_or_token_id']
	, 'getToken'		:	fn.lang_dict['buy_token']
	, 'null_1'			:	'--------------------------------'
	, 'back'			:	fn.lang_dict['go_back']
	, 'exit'			:	fn.lang_dict['exit']
}

menu_panels = {
	'1'		:	fn.lang_dict['customer_panel']
	, '2'	:	fn.lang_dict['counter_panel']
	, '3'	:	fn.lang_dict['admin_panel']
	, 'e'	:	fn.lang_dict['exit']
}

def showMenu(module, view, tree):
	refresh = 0

	sr = 1
	sr_list = list()
	for x in view:
		if x == 'exit':
			print('e)', view[x])
		elif x == 'back':
			print('b)', view[x])
		elif 'null' in x:
			print(view[x])
		else:
			print(sr, ') ', view[x], sep = '')
			sr_list.append(str(sr))
			sr += 1

	opt = input(fn.lang_dict['enter_your_choice'] + ': ')

	if opt == 'e':
		exit('Bye!! :)')
	elif opt == 'b':
		tree.pop()
		return
	else:
		if opt not in sr_list:
			print(fn.lang_dict['invalid_choice'])
		else:
			refresh = 1
			keys = list()
			for x in list(view.keys()):
				if 'null' not in x:
					keys.append(x)

			selectedKey = keys[int(opt) - 1]

			tree.append(
				view[selectedKey]
			)
			fn.printHeading(tree, fn.configs.__SCREEN_WIDTH__)
			print('(' + fn.lang_dict['press_ctrl_c_to_go_back_to_main_menu'] + ')' + '\n')

			eval(
				module
				+ '.'
				+ selectedKey
				+ '()'
			)

			tree.pop()

		if refresh:
			fn.showCountDown(fn.lang_dict['will_be_refreshed_in'] + ' ', 3)

		fn.printHeading(tree, fn.configs.__SCREEN_WIDTH__)
		print()
		showMenu(module, view, tree)


menu_tree = [fn.lang_dict['menu']]

while True:
	try:
		fn.printHeading(menu_tree, fn.configs.__SCREEN_WIDTH__)

		for i in menu_panels:
			print(i, ') ', menu_panels[i], sep = '')

		opt = input(fn.lang_dict['enter_your_choice'] + ': ')

		if opt != '':
			menu_tree.append(menu_panels[opt])
			fn.printHeading(menu_tree, fn.configs.__SCREEN_WIDTH__)

			if opt == '1':
				from . import customer_menu
				showMenu('customer_menu', customer_view, menu_tree)
			elif opt == '2':
				from . import counter_menu
				showMenu('counter_menu', counter_view, menu_tree)
			elif opt == '3':
				from . import admin_menu
				showMenu('admin_menu', admin_view, menu_tree)
			elif opt == 'e':
				exit('\nBye!! :)')
			else:
				print(fn.lang_dict['invalid_choice'])
		else:
			print(fn.lang_dict['invalid_choice'])
	except (KeyboardInterrupt, KeyError, ValueError):
		menu_tree = [fn.lang_dict['menu']]
		continue
