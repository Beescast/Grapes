#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import urllib2
import hashlib
import random
import requests
import threading
from flask import *
from robot import Robot
from rooms_manage import RoomsManage
from utils.debug import *
from utils.general import *
from chat.network.poxy import MyPoxy
import MySQLdb
from utils.config import *

app = Flask(__name__)
roomsmanage = None

@app.route("/")
def index():
	amount = request.args.get('amount')
	return "Hello World!"

@app.route("/grapes/addroom")
def addRoom():
	rid = request.args.get('rid')
	try:
		roomsmanage.addRoom(int(rid))
	except Exception, e:
		return 'Please enter the correct room number'
	room_log('addRoom '+rid)
	return 'Successful operation'

@app.route("/grapes/delroom")
def delRoom():
	rid = request.args.get('rid')
	try:
		roomsmanage.delRoom(int(rid))
		room_log('delRoom '+rid)
		mysql_conn = MySQLdb.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset='utf8')
		mysql_cursor = mysql_conn.cursor()
		mysql_cursor.execute('DELETE FROM server_rooms WHERE rid=%d' % int(rid))
		mysql_conn.commit()
		mysql_cursor.close()
		mysql_conn.close()
		return 'Successful operation'
	except Exception, e:
		print e
		return 'Please enter the correct room number'

@app.route("/grapes/setroom")
def setRoom():
	try:
		rid = request.args['rid']
		int(rid)
	except Exception, e:
		return 'Please enter the correct room number'
	if rid not in roomsmanage.rooms:
		roomsmanage.addRoom(int(rid))
		# return 'Please add room ' + rid
	pause = request.args.get('pause', '0')
	if pause == '1':
		roomsmanage.setPause(int(rid), True)
	elif pause == '0':
		roomsmanage.setPause(int(rid), False)
	else:
		pause = '0'
	try:
		freq = request.args['freq']
		roomsmanage.setFreq(int(rid), int(freq))
	except Exception, e:
		freq = '30'
		pass
	try:
		interval = request.args['interval']
		roomsmanage.setInterval(int(rid), int(interval))
	except Exception, e:
		interval = '10'
		pass
	# try:
	#	 num = request.args['num']
	#	 roomsmanage.setNumber(int(rid), int(num))
	# except Exception, e:
	#	 pass
	try:
		a0 = request.args.get('a0', '0') # 自由账号
		if len(a0) == 0:
			a0 = '0'
		a1 = request.args.get('a1', '0') # 高等级账号
		if len(a1) == 0:
			a1 = '0'
		a2 = request.args.get('a2', '0') # 已挂粉丝团牌子
		if len(a2) == 0:
			a2 = '0'
		a3 = request.args.get('a3', '0') # 骑士团
		if len(a3) == 0:
			a3 = '0'
		roomsmanage.setNumber(int(rid), int(a0), int(a1), int(a2), int(a3))
	except Exception, e:
		pass

	room_log('setRoom '+'rid:'+rid+';pause:'+pause+':freq:'+freq+':interval:'+interval+':a0:'+a0+':a1:'+a1+':a2:'+a2+':a3:'+a3)
	mysql_conn = MySQLdb.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset='utf8')
	mysql_cursor = mysql_conn.cursor()
	mysql_cursor.execute('''REPLACE INTO server_rooms
						(rid, a0, a1, a2, a3, pause, freq, login_interval)
						VALUES
						(%s, %s, %s, %s, %s, %s, %s, %s)''' % (rid, a0, a1, a2, a3, pause, freq, interval))
	mysql_conn.commit()
	mysql_cursor.close()
	mysql_conn.close()
	return 'Successful operation'

@app.route("/grapes/sendmsg")
def sendmsgs():
	rid = request.args.get('rid')
	msgs = request.args.get('msg')
	repeat = request.args.get('repeat')
	col = request.args.get('col', '0')
	try:
		col = int(col)
	except Exception, e:
		col = 0
	if msgs:
		msg_list = urllib2.unquote(msgs).split('|')
	else:
		return 'Please enter msg'
	# for i in range(0, len(msg_list)):
	#	 msg_list[i] = urllib2.unquote(msg_list[i])
	try:
		roomsmanage.sendMsgs(int(rid), msg_list, repeat, col)
	except Exception, e:
		return 'Please enter the correct room number'
	room_log('sendmsgs '+'rid:'+rid+'msgs:'+msgs+'repeat:'+repeat+'col:'+col)
	return 'Successful operation'

@app.route("/grapes/addfollow")
def addFollow():
	rid = request.args.get('rid')
	nickname = request.args.get('nickname')
	url = follow_url+'/%s/%s' % (rid, nickname)
	try:
		urllib2.urlopen(url)
		return 'Successful operation'
	except Exception, e:
		return str(e.message)

@app.route("/grapes/delfollow")
def delFollow():
	rid = request.args.get('rid')
	nickname = request.args.get('nickname')
	return 'Successful operation'

def testThread(rid, msgs, repeat, col):
	if repeat > 200:
		repeat = 200
	delay = 0
	for i in range(0, repeat):
		robot = Robot(rid)
		robot.isTest = True
		robot.setPause(True)
		robot.setFreq(30)
		robot.setDelay(delay)
		delay += random.random()
		msg = msgs[random.randint(0, len(msgs)-1)]
		robot.sendMessage(msg)
		robot.start()

@app.route("/grapes/testmsg")
def testmsgs():
	rid = request.args.get('rid')
	msgs = request.args.get('msg')
	repeat = request.args.get('repeat')
	col = request.args.get('col', '0')
	try:
		repeat = int(repeat)
	except Exception, e:
		repeat = 0
	try:
		col = int(col)
	except Exception, e:
		col = 0
	if msgs:
		msg_list = urllib2.unquote(msgs).split('|')
	else:
		return 'Please enter msgs'
	# for i in range(0, len(msg_list)):
	#	 msg_list[i] = urllib2.unquote(msg_list[i])
	if rid and repeat>0:
		try:
			t = threading.Thread(target=testThread, args=(int(rid), msg_list, repeat, col))
			t.setDaemon(True)
			t.start()
		except Exception, e:
			return 'Please enter param'
		room_log('testmsgs '+'rid:'+rid+'msgs:'+msgs+'repeat:'+str(repeat))
		return 'Successful operation'
	else:
		return 'Please enter param'

@app.route("/grapes/roominfo")
def roominfo():
	rid = request.args.get('rid')
	infos = roomsmanage.getDict()
	if infos and rid:
		rid_info = infos.get(rid)
		if rid_info:
			return json.dumps(rid_info, ensure_ascii=False)
		else:
			return '{}'
	else:
		return json.dumps(infos, ensure_ascii=False)

@app.route("/grapes/setdebug")
def setdebug():
	flag = request.args.get('flag')
	status = request.args.get('status')
	if dbg_set_status(flag, status) == 0:
		return 'sucess'
	else:
		return 'failed'

@app.route("/grapes/debuginfo")
def debuginfo():
	return json.dumps(dbg_flags, ensure_ascii=False)

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	MyPoxy.startUpdate()
	roomsmanage = RoomsManage()
	roomsmanage.setDaemon(True)
	roomsmanage.start()
	mysql_conn = MySQLdb.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset='utf8')
	mysql_cursor = mysql_conn.cursor()
	mysql_cursor.execute('''SELECT rid, a0, a1, a2, a3, pause, freq, login_interval FROM server_rooms''')
	results = mysql_cursor.fetchall()
	for row in results:
		rid = row[0]
		a0 = row[1]
		a1 = row[2]
		a2 = row[3]
		a3 = row[4]
		pause = row[5]
		freq = row[6]
		interval = row[7]
		roomsmanage.addRoom(rid)
		if pause == 1:
			roomsmanage.setPause(rid, True)
		elif pause == 0:
			roomsmanage.setPause(rid, False)
		roomsmanage.setFreq(rid, freq)
		roomsmanage.setInterval(rid, interval)
		roomsmanage.setNumber(rid, a0, a1, a2, a3)
	mysql_cursor.close()
	mysql_conn.close()
	'''
	src = 'beesConsole' + str(int(time.time()))
	url = 'http://192.168.3.56:8081/out/index.php/apply/beesConsoleRoom?msg='+hashlib.md5(src).hexdigest()
	# url = 'http://grapes.beeslm.com:8081/out/index.php/apply/beesConsoleRoom?msg='+hashlib.md5(src).hexdigest()
	print url
	# params = {'msg':hashlib.md5(src).hexdigest()}
	# r = requests.post(url, data=params)
	try:
		r = requests.get(url, timeout=0.5)
		print r.text
	except Exception, e:
		print e
		'''
	app.run(host='0.0.0.0', port=5001, threaded=True, debug=True, use_reloader=False)
	print 'Done!'