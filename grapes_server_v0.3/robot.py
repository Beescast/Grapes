# coding=utf-8

from chat.auth import *
from utils.douyu_utils import *
from utils.servers import servers
from utils.general import *
from utils.debug import *
from utils.config import *

class Robot(threading.Thread):
	def __init__(self, rid, msgQueue=None, account_type=0):
		super(Robot, self).__init__()
		self.rid = rid
		self.msgQueue = msgQueue
		self.account_type = account_type
		self.delay = 0
		self.isRunning = True
		self.auth = None
		self.pause = False
		self.freq = 30 # 最大发言间隔，最小值为20
		self.lastmsg = None
		self.cookie = None
		self.uid = None
		self.nickname = ''
		self.isLogin = False
		self.send_count = 0
		self.max_send = random.randint(20,40)
		self.isTest = False
		self.sendmsg_thread = None
		self.msg = None

	# cookie_type: 0None， 1高等级账号， 2已挂粉丝团牌子， 3骑士团
	def get_cookie_from_server(self, cookie_type=0):
		url = cookie_url+'?rid=%d&type=%d' % (self.rid, self.account_type)
		r = None
		response = None
		cookie = None
		while (not cookie) and self.isRunning:
			try:
				r = requests.get(url)
			except Exception, e:
				dbg_dump('ERR', str(self.rid), str(e)+' '+url)
			if r:
				response = r.text
			# response = '''{"acf_ct": "0", "acf_biz": "1", "acf_did": "D262628736F077C40ECE7583A5F82D22", "acf_stk": "f708f064823fb6f1", "acf_uid": "126973039", "acf_auth": "7d98gBRzE6Eq1f0oTAUM6f%2BUITkwDXWcLorHhCY8xf6%2FYagTw%2FnLnlpKXSmtOdgjPod0G2jtOV2s1cixY4IshbxVPgGTj3tWKXvXJ06MeElu7hlwPQ01oJU", "acf_devid": "5241fedbfa9560de9a41013a16f82bb3", "acf_ltkid": "48314133", "acf_groupid": "1", "acf_nickname": "xx%E7%A5%9E%E6%95%99%E6%95%99%E4%B8%BB", "acf_own_room": "0", "acf_username": "126973039", "wan_auth37wan": "f2318b9a36beDGlmmfGtuoZbxfEQIn2facsHettKqskp5gpW9IS%2BV92OLY7nTCBuU2bHzo%2BtxSszhIGFGckGIhQLP%2BGrdFrUTzBuBLDzDtZqtcXJIoQ", "acf_phonestatus": "1", "_dys_refer_action_code": "show_recommend_livelist_room", "Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7": "1493200740,1493273947,1493692988,1493699045"}'''

			if response:
				dbg_dump('INFO', str(self.rid), response.encode('utf-8'))
				try:
					data = json.loads(response)
					cookie = data['cookie']
					self.uid = cookie['acf_uid']
					self.nickname = urllib.unquote(cookie['acf_nickname'].encode('utf-8'))
					dbg_flag_add(self.nickname, 1)
					break
				except Exception, e:
					dbg_dump('ERR', str(self.rid), str(e)+' '+url)
					dbg_dump('ERR', str(self.rid), 'response: '+response)
			else:
				dbg_dump('ERR', str(self.rid), 'response is None')
			time.sleep(30+random.random())
		return cookie

	def get_barrage_from_server(self):
		url = barrage_url+'/%d/%s' % (self.rid, self.uid)
		try:
			r = requests.get(url)
		except Exception, e:
			dbg_dump('ERR', self.nickname, str(e)+' '+url)
			return None

		response = r.text
		# print response
		data = None
		try:
			dbg_dump('VERB', str(self.rid), 'response: '+response)
			data = json.loads(response)
		except Exception, e:
			dbg_dump('ERR', self.nickname, str(e) + ' ' + url)
			dbg_dump('ERR', self.nickname, 'response: ' + response)
			#raise e
		#if data.get('if_send', 1) == 0:
		#	print url
		#	print data.get('msg', None)
		return data

	def error_hdlr(self, rid, msg):
		dbg_dump('ERR', self.nickname, json.dumps(msg.body, ensure_ascii=False))
		account_log(self.uid, self.nickname, json.dumps(msg.body, ensure_ascii=False))
		if self.auth:
			self.auth.close()
			self.auth = None
		self.isLogin = False
		self.cookie = None
		# if msg.body['code'] == '51':

	def loginres_hdlr(self, rid, msg):
		dbg_dump('INFO', self.nickname, json.dumps(msg.body, ensure_ascii=False))
		self.lastmsg = None
		self.send_count = 0
		self.max_send = random.randint(20,40)
		self.isLogin = True
		account_log(self.uid, self.nickname, json.dumps(msg.body, ensure_ascii=False))
		if not self.sendmsg_thread:
			self.sendmsg_thread = threading.Thread(target=self.send_msg)
			self.sendmsg_thread.setDaemon(True)
			self.sendmsg_thread.start()

	def chatres_hdlr(self, rid, msg):
		dbg_dump('INFO', self.nickname, json.dumps(msg.body, ensure_ascii=False))
		account_log(self.uid, self.nickname, json.dumps(msg.body, ensure_ascii=False))
		res = msg.body.get('res', '1')
		if msg.body.get('res', '1') == '0':
			pass
		else:
			self.send_count = self.max_send + 1

	def unknown_hdlr(self, rid, msg):
		dbg_dump('VERB', self.nickname, json.dumps(msg.body, ensure_ascii=False))
		print json.dumps(msg.body, ensure_ascii=False)

	def send_msg(self):
		while self.isRunning:
			if self.isTest:
				time.sleep(3)
				if self.msg:
					self.auth.send_msg(self.msg)
					dbg_dump('INFO', self.nickname, self.msg)
					self.msg = None
				self.close()
				break
			time.sleep(random.uniform(20, self.freq))
			if not self.isRunning:
				break
			if not self.msgQueue.empty():
				try:
					msg = self.msgQueue.get(timeout=1)
				except Exception, e:
					continue
				if self.auth:
					self.auth.send_msg(msg)
					dbg_dump('INFO', self.nickname, 'say: '+msg)
					self.send_count += 1
			elif not self.pause:
				msg = '666'
				barrage = self.get_barrage_from_server()
				if barrage and barrage['if_send'] and len(barrage['msg'])>0:
					msg = barrage['msg']
				elif barrage:
					dbg_dump('INFO', self.nickname, json.dumps(barrage, ensure_ascii=False))
					account_log(self.uid, self.nickname, json.dumps(barrage, ensure_ascii=False))
					if barrage['if_send'] == 0 and self.isRunning:
						url = login_url + '/%d' % self.rid
						try:
							r = requests.get(url)
						except Exception, e:
							dbg_dump('ERR', self.nickname, str(e))
						dbg_dump('INFO', self.nickname, url)
						response = r.text
						dbg_dump('VERB', self.nickname, 'response: '+response)
					barrage = None
				else:
					dbg_dump('WARN', self.nickname, 'barrage is None')
					account_log(self.uid, self.nickname, 'barrage is None')
				if barrage and self.auth and self.lastmsg != msg:
					try:
						self.auth.send_msg(msg)
						self.lastmsg = msg
						self.send_count += 1
						dbg_dump('INFO', self.nickname, 'say: '+msg)
					except Exception, e:
						print e
						self.sendmsg_thread = None
						self.send_count = self.max_send+1
						break
			if self.send_count > self.max_send:
				self.sendmsg_thread = None
				if self.auth:
					self.auth.close()
					self.auth = None
				self.isLogin = False
				self.cookie = None
				break

	def run(self):
		time.sleep(self.delay)
		while self.isRunning:
			#servers = douyu_get_danmu_auth_server(self.rid)
			if len(servers) == 0:
				dbg_dump('WARN', self.nickname, "servers length: "+str(len(servers)))
				continue
			try:
				self.send_count = 0
				server = servers[random.randint(0, len(servers ) -1)]
				danmu_ip = server['ip']
				danmu_port = server['port']
				self.cookie = self.get_cookie_from_server()
				if self.cookie:
					dbg_dump('VERB', self.nickname, 'use server IP: '+server['ip']+':'+str(server['port']))
					self.auth = ChatAuth(self.rid, danmu_ip, danmu_port, self.cookie)
					self.auth.on('loginres', self.loginres_hdlr)
					self.auth.on('chatres', self.chatres_hdlr)
					self.auth.on('error', self.error_hdlr)
					# self.auth.on('unknown', self.unknown_hdlr)
					self.auth.knock()
					dbg_dump('INFO', self.nickname, 'closed')
			except Exception, e:
				dbg_dump('ERR', self.nickname, str(e))
				if self.auth:
					self.auth.close()
					self.auth = None
				self.isLogin = False
				self.cookie = None
			time.sleep(10+random.random())

	def close(self):
		dbg_dump('INFO', self.nickname, 'close')
		self.isRunning = False;
		if self.auth:
			self.auth.close()
		self.isLogin = False
		self.cookie = None

	def setFreq(self, freq):
		dbg_dump('INFO', self.nickname, 'setFreq: '+str(freq))
		if freq < 20:
			freq = 20
		self.freq = freq

	def setPause(self, status):
		dbg_dump('INFO', self.nickname, 'setPause: '+str(status))
		self.pause = status

	def sendMessage(self, msg):
		dbg_dump('INFO', self.nickname, 'sendMessage: '+str(msg))
		self.msg = msg

	def setDelay(self, delay):
		dbg_dump('INFO', self.nickname, 'setDelay: '+str(delay))
		self.delay = delay

	def getDict(self):
		dict = {}
		dict['rid'] = self.rid
		dict['type'] = self.account_type
		dict['run'] = self.isRunning
		dict['pause'] = self.pause
		dict['freq'] = self.freq
		dict['nickname'] = self.nickname
		dict['send_count'] = self.send_count
		dict['max_send'] = self.max_send
		return dict