c_debug = False # вкл/выкл сообщения отладки
c_delay = 10
c_oldfriends = 'oldfriends.txt'

f = open('account.txt', 'r')
user_login = f.readline()
user_password = f.readline()
f.close()

def acc_save(new_pass):
	f = open('account.txt', 'w')
	f.write(user_login)
	f.write(new_pass)
	f.close()