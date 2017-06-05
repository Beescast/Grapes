
USE_56 = True
USE_JIANGSU = not USE_56

if USE_56:
	mysql_host = '192.168.3.56'
	mysql_port = 3306
	mysql_user = 'repl'
	mysql_passwd = '0831@Bees'
	mysql_db = 'grapes'

	follow_url = 'http://192.168.3.56:8000/follow'
	cookie_url = 'http://192.168.3.56:8000/cookie'
	barrage_url = 'http://192.168.3.56:8000/barrage'
	login_url = 'http://192.168.3.56:8000/login'
	logout_url = 'http://192.168.3.56:8000/stop'
elif USE_JIANGSU:
	mysql_host = '127.0.0.1'
	mysql_port = 3306
	mysql_user = 'repl'
	mysql_passwd = '0831@Bees'
	mysql_db = 'grapes'

	follow_url = 'http://127.0.0.1:8000/follow'
	cookie_url = 'http://127.0.0.1:8000/cookie'
	barrage_url = 'http://127.0.0.1:8000/barrage'
	login_url = 'http://127.0.0.1:8000/login'
	logout_url = 'http://127.0.0.1:8000/stop'