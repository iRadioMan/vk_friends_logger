# Не забыть удалить исходник перед релизом!
# Оставить только скомпилированный файл.
# Это простая защита от случайного просмотра пароля третьим лицом

def encode(old_pass):
	new_pass = ''
	
	for ch in old_pass:
		new_pass += chr(int(ord(ch) + 2))
	new_pass = '#RSES#' + new_pass
	
	return new_pass
	
def decode(old_pass):
	new_pass = ''
	
	old_pass = old_pass[6:]
	
	for ch in old_pass:
		new_pass += chr(int(ord(ch) - 2))
	
	return new_pass