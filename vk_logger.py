import sys
import vk_api as vk
import time
import datetime
import pickle
import os
#
import vk_guard
from vk_config import *
global user_password

print('------------------------------')
print('Логгер друзей ВК | by RadioMan')
print('   ver 02.11.2016 build 945')
print('------------------------------')
print('Авторизация...')

if user_login == '\n' or user_password == '\n':
	print('[!!!] Пожалуйста, отредактируйте ваши данные для входа в файле account.txt')
	time.sleep(5)
	sys.exit()

if '#RSES#' not in user_password:
	print('Закодируем пароль в файле конфигурации... На всякий случай.')
	user_password = vk_guard.encode(user_password)
	acc_save(user_password)
	print('Готово!')

vk_session = vk.VkApi(user_login, vk_guard.decode(user_password))

try:
	vk_session.authorization()
	vk = vk_session.get_api()
except vk.AuthorizationError as error_msg:
	print(error_msg)
	sys.exit()

print('Успешно авторизовались!\n')

# стандартный заголовок окончен

first_launch = True
friends_before = {}
friends_now = {}

while True:	
	if not first_launch:
		#time.sleep(c_delay)
		print('[Нажмите Enter для получения новых данных для сравнения либо закройте программу и запустите ее потом...]')
		input()
		
	time_now = datetime.datetime.now()
	t_processing = '[' + time_now.strftime('%d. %b %Y %I:%M%p') + ']'
	print(t_processing + ' Получаем друзей...')
	
	try:
		if first_launch:
			first_launch = False
			
			if os.path.isfile('old.txt'): os.remove('old.txt') #старый тип данных
			
			if not os.path.isfile(c_oldfriends):
				print('Старых данных о друзьях не обнаружено. Получаем новые и сохраняем...')
				friends_before = vk.friends.get()
				with open(c_oldfriends, 'wb') as f:
					pickle.dump(friends_before, f)
			else:
				print('Обнаружены старые данные о друзьях. Используем их для анализа...')
				with open(c_oldfriends, 'rb') as f:
					friends_before = pickle.load(f)
		else:		
			friends_now = vk.friends.get()
			f = open('log.txt', 'a')
			f.write(s_processing + '\n')
			
			for human_id in friends_before['items']:
				if human_id not in friends_now['items']:
					human_info = vk.users.get(user_ids = human_id)
					human_d = '[-] ' + human_info[0]['first_name'] + ' ' + human_info[0]['last_name'] + ' (' + str(human_id) + ')'
					print(human_d + '\n')
					f.write(human_d + '\n')

			for human_id in friends_now['items']:
				if human_id not in friends_before['items']:
					human_info = vk.users.get(user_ids = human_id)
					human_n = '[+] ' + human_info[0]['first_name'] + ' ' + human_info[0]['last_name'] + ' (' + str(human_id) + ')'
					print(human_n + '\n')
					f.write(human_n + '\n')
					
			friends_before = friends_now
			with open(c_oldfriends, 'wb') as f:
					pickle.dump(friends_before, f)
			f.close()
		print('Обработка друзей окончена.\n')
				
	except BaseException as error_msg:
		print(error_msg)
		sys.exit()