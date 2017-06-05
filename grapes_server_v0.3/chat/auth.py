# -*- coding: UTF-8 -*-


from collections import OrderedDict
import network.client
import threading
import time
import logging
import random
import urllib
import json

from  network.swfapi  import  Swfapi

RAW_BUFF_SIZE = 4096
KEEP_ALIVE_INTERVAL_SECONDS = 45

SWFAPI_IP = "183.238.13.66"
SWFAPI_IP = "192.168.3.108"
SWFAPI_IP = "123.56.239.203"
SWFAPI_PORT = 12306


def  keep_live_fun(auth):
	vbw = 0
	swfapi = Swfapi(SWFAPI_IP, SWFAPI_PORT)

	# keepliveStr :  keeplive  respone packet
	if auth.keepliveStr != "":
		swf_req = {
			"func": "xxKeepGu",
			"vbw": vbw,
			"keepliveStr": auth.keepliveStr
		}
		swf_rst = swfapi.xxSwfApi(swf_req)
		auth.client.send_text(swf_rst['text'])
		auth.keepliveStr = ""
	else:
		swf_req = {
			"func": "xxKeepLive",
			"vbw": vbw
		}
		swf_rst = swfapi.xxSwfApi(swf_req)
		auth.client.send_text(swf_rst['text'])


class ChatAuth:

	def __init__(self, rid, host, port, cookie):

		self.client = None
		self.channel_id = 1  # Convention

		self.rid = rid
		self.host = host
		self.port = port
		self.cookie = cookie
		self.acf_uid = cookie['acf_uid']
		self.acf_nickname = urllib.unquote(cookie['acf_nickname'].encode('utf-8'))
		self.ver = '20150929'
		self.aver = '2017022801'
		self.keepliveStr = ""
		self.keeplive_flag = True
#	   self.devid = "982E835F911E5EBC354783C3E3BC9328"
		self.devid = self.getRanomdDid()

		self.callbacks = {}

		self.isRunning = True

	def close(self):
		self.isRunning = False
		if self.client:
			self.client.close()
		#print 'auth close'

	# Keep-Alive thread func
	def keep_live_thr(self, auth, delay):
		while self.isRunning:
			if not self.keeplive_flag:
				print 'keeplive_flag:', self.keeplive_flag
				self.close()
			self.keeplive_flag = False
			keep_live_fun(auth)
			time.sleep(delay)

	def thread_suq_hdlr(self, auth, str):
		time.sleep(0.7)
		auth.msg_suq_hdlr(str)
		# while self.isRunning:
		#	 time.sleep(2)

	def thread_vq_hdlr(self, auth, str):
		time.sleep(0.1)
		auth.msg_vq_hdlr(str)
		# while self.isRunning:
		#	 time.sleep(2)

	def  getRanomdDid(self):
		tab = "0123456789ABCDEF"
		did = ""
		for i in range(0, 32):
			did = did + tab[random.randint(0, 15)]
		return did

	def on(self, event_name, callback):
		callback_list = None
		try:
			callback_list = self.callbacks[event_name]
		except KeyError as e:
			callback_list = []
			self.callbacks[event_name] = callback_list
		callback_list.append(callback)

	def trigger_callbacks(self, event_name, message):
		callback_list = None

		try:
			callback_list = self.callbacks[event_name]
		except KeyError as e:
			logging.info('Message of type "%s" is not handled' % event_name)
			callback_list = self.callbacks.get('unknown')

		if callback_list is None or len(callback_list) <= 0:
			return

		for callback in callback_list:
			callback(self.rid, message)

	def login(self, rid, cookie):

		#type@=loginreq/username@=51425727/ct@=0/password@=870d8d6853e0843895ea6b477d64d8d7/
		#roomid@=210008/devid@=2B3F65BB2B06D73B542A5F13BD0FBFA8/rt@=1471601814/vk@=7d816a706dcd99dc9555d7656c16a557/
		#ver@=20150929/aver@=2016081801/ltkid@=98727346/biz@=1/stk@=abde9a6102dcff12/
		# Send AUTH request
#		devid = str(uuid.uuid4()).replace("-", "").upper()
#		rt = str(int(time.time()))
#		devid = '2B3F65BB2B06D73B542A5F13BD0FBFA8'
#		strs = rt + '7oE9nPEG9xXV69phU31FYCLUagKeYtsF' + devid
#		vk = hashlib.md5(strs).hexdigest()

		swfapi = Swfapi(SWFAPI_IP, SWFAPI_PORT)
		swf_req = {
			"func":	 "xxUserLogin",
			"username": cookie['acf_username'],
			"password": cookie['acf_auth'],
			"devid":	cookie.get('acf_devid', ''),
			"ltkid":	cookie['acf_ltkid'],
			"biz":	  cookie['acf_biz'],
			"stk":	  cookie['acf_stk'],
			"roomid":   str(rid),
			"ct":	   cookie['acf_ct'],
			"ver":	  self.ver,
			"aver":	 self.aver,
		}

		swf_rst = swfapi.xxSwfApi(swf_req)
		self.client.send_text(swf_rst['text'])

	def logout(self, rid, cookie):
		swfapi = Swfapi(SWFAPI_IP, SWFAPI_PORT)
		swf_req = {
			"func":	 "xxUserLogin",
			"username": cookie['acf_username'],
			"password": cookie['acf_auth'],
			"devid":	cookie.get('acf_devid', ''),
			"ltkid":	cookie['acf_ltkid'],
			"biz":	  cookie['acf_biz'],
			"stk":	  cookie['acf_stk'],
			"roomid":   str(rid),
			"ct":	   cookie['acf_ct'],
			"ver":	  self.ver,
			"aver":	 self.aver,
		}

		swf_rst = swfapi.xxSwfApi(swf_req)
		self.client.send_text(swf_rst['text'])

	def send_msg(self, msg, col=0):
		#type@=chatmessage/receiver@=0/content@=bbbbbbbbbbbb/scope@=/col@=0/
		send_par = {
					'type'	  : 'chatmessage',
					'receiver'  : 0,
					'content'   : msg
					}
		if col < 0 or col > 6:
			col = random.randint(1, 6)
		if col > 0:
			send_par['col'] = col
			send_par['pid'] = 3
		try:
			self.client.send(send_par)
		except Exception, e:
			print e, 'send_msg'
			self.close()

	def msg_suq_hdlr(self, str):
		swfapi = Swfapi(SWFAPI_IP, SWFAPI_PORT)
		swf_req = {
			"func":   "xxSuq",
			"pwd":	self.cookie['acf_stk'],
			"str":	str
		}
		swf_rst = swfapi.xxSwfApi(swf_req)
		self.client.send_text(swf_rst['text'])

	def msg_vq_hdlr(self, str):
		swfapi = Swfapi(SWFAPI_IP, SWFAPI_PORT)
		swf_req = {
			"func":   "xxVq",
			"str":	str
		}
		swf_rst = swfapi.xxSwfApi(swf_req)
		self.client.send_text(swf_rst['text'])

	# Start running
	def knock(self):

		self.client = network.client.Client(self.host, self.port)

		self.login(self.rid, self.cookie)
		# Handle messages
		for message in self.client.receive():

			if not message:
				continue

			msg_type = message.attr('type')
			# print message.body
			if msg_type == 'loginres':
				time.sleep(0.1)
				self.client.send(OrderedDict([('type', 'qtlnq')]))

				time.sleep(0.1)
				self.client.send(OrderedDict([('type', 'qtlq')]))

				t = threading.Thread(target=self.keep_live_thr, args=(self, KEEP_ALIVE_INTERVAL_SECONDS))
				t.setDaemon(True)
				t.start()

				time.sleep(0.1)
				self.client.send(OrderedDict([('type', 'get_online_noble_list'), ('rid', str(self.rid))]))

				time.sleep(0.1)
				self.client.send(OrderedDict([('type', 'qrl'), ('rid', str(self.rid)), ('et', '0')]))

			elif msg_type == 'keeplive':
				self.keeplive_flag = True
				self.keepliveStr = message.raw

			elif msg_type == "suq":
				t = threading.Thread(target=self.thread_suq_hdlr, args=(self, message.raw))
				t.setDaemon(True)
				t.start()

			elif msg_type == "vq":
				t = threading.Thread(target=self.thread_vq_hdlr, args=(self, message.raw))
				t.setDaemon(True)
				t.start()

			elif msg_type == 'setmsggroup':
				pass

			elif msg_type == "rlcn":
				pass

			elif msg_type == 'error':
				pass
				# print self.acf_uid, ':', message.body
				# if message.body.get('code', '51') != '51':
				#	 filename = 'error/'+message.body['code']+'-'+self.acf_uid+'-'+self.acf_nickname+'.txt'
				#	 text = json.dumps(self.cookie, ensure_ascii=False)
				#	 f = open(filename, 'w')
				#	 f.write(urllib.unquote(text))
				#	 f.close()
			# elif msg_type == 'chatres':
			#	 print message.body
			#	 #{'res': '0', 'type': 'chatres', 'len': '50', 'cd': '1'}
			if msg_type != 'keeplive':
				self.trigger_callbacks(msg_type, message)

