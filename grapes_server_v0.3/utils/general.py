import os
import time
import datetime

def account_log(uid, nickname, msg):
	now_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	# now = datetime.datetime.now()

	if not nickname:
		nickname = ''
	msg = now_string+' ['+uid+':'+nickname+'] '+msg

	if 0:
		print msg

	if 0:
		if not os.path.exists("./logs"):
			os.makedirs("./logs")
		fp = open("./logs/%s.txt" % nickname)
		fp.write(msg + "\n")
		fp.close()

def room_log(msg):
	now_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	if not os.path.exists("./logs"):
		os.makedirs("./logs")
	fp = open("./logs/room.txt", 'a')
	fp.write(now_string+': '+msg + "\n")
	fp.close()
