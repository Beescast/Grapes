# coding=utf-8

from Queue import Queue
import json
import random
import requests
import threading
from robot import Robot
from utils.debug import *
from utils.config import *

class Room(threading.Thread):
	def __init__(self, rid):
		super(Room, self).__init__()
		dbg_flag_add(str(rid), 1)
		self.rid = rid
		self.freq = 30
		self.pause = False
		self.interval = 10
		self.a0 = 0
		self.a1 = 0
		self.a2 = 0
		self.a3 = 0
		self.robots0 = []
		self.robots1 = []
		self.robots2 = []
		self.robots3 = []
		self.room_status = -1 # 房间开关博状态，2关播，1开播
		self.isRunning = True
		self.msgQueue = Queue()

	def run(self):
		while self.isRunning:
			roomapi_url = 'http://open.douyucdn.cn/api/RoomApi/room/%d' % self.rid
			r = None
			response = None
			info = None
			try:
				r = requests.get(roomapi_url)
			except Exception, e:
				dbg_dump('ERR', str(self.rid), str(e)+" "+roomapi_url)
			if r:
				response = r.text
			try:
				info = json.loads(response)
			except Exception, e:
				dbg_dump('ERR', str(self.rid), str(e)+" "+roomapi_url)
			if info and info['error'] == 0:
				data = info['data']
				room_status = data['room_status']
				dbg_dump('VERB', str(self.rid), 'room_status: '+room_status)
				if room_status != self.room_status:
					self.room_status = room_status
					dbg_dump('INFO', str(self.rid), 'room status: '+self.room_status)
					if room_status == '2': # 关播
						while len(self.robots0) > 0:
							robot = self.robots0.pop(0)
							robot.close()
						while len(self.robots1) > 0:
							robot = self.robots1.pop(0)
							robot.close()
						while len(self.robots2) > 0:
							robot = self.robots2.pop(0)
							robot.close()
						while len(self.robots3) > 0:
							robot = self.robots3.pop(0)
							robot.close()
						url = logout_url+'/%d' % self.rid
						try:
							requests.get(url)
						except Exception, e:
							dbg_dump('ERR', str(self.rid), str(e))
						dbg_dump('DEBUG', str(self.rid), url)
					else: # 开播
						while self.isRunning:
							url = login_url+'/%d' % self.rid
							try:
								r = requests.get(url)
							except Exception, e:
								dbg_dump('ERR', str(self.rid), str(e))
							dbg_dump('DEBUG', str(self.rid), url)
							response = r.text
							dbg_dump('DEBUG', str(self.rid), response)
							data = {}
							try:
								data = json.loads(response)
							except Exception, e:
								dbg_dump('ERR', str(self.rid), str(e))
							status = data.get('status', 4)
							if status != 4:
								break
							else:
								dbg_dump('WARN', str(self.rid), response)
						self.setNumber(self.a0, self.a1, self.a2, self.a3)
			else:
				dbg_dump('DEBUG', str(self.rid), response)
			time.sleep(10)

	def setInterval(self, interval):
		dbg_dump('VERB', str(self.rid), 'setInterval: ' + str(interval))
		self.interval = interval

	def close(self):
		dbg_dump('VERB', str(self.rid), 'close')
		self.isRunning = False;
		for robot in self.robots0:
			robot.close()
		self.robots0 = []
		for robot in self.robots1:
			robot.close()
		self.robots1 = []
		for robot in self.robots2:
			robot.close()
		self.robots2 = []
		for robot in self.robots3:
			robot.close()
		self.robots3 = []

		url = logout_url + '/%d' % self.rid
		try:
			requests.get(url)
		except Exception, e:
			dbg_dump('ERR', str(self.rid), str(e))
		dbg_dump('DEBUG', str(self.rid), url)

	def setFreq(self, freq):
		dbg_dump('VERB', str(self.rid), 'setFreq: ' + str(freq))
		if freq < 20:
			freq = 20
		self.freq = freq
		for robot in self.robots0:
			robot.setFreq(freq)
		for robot in self.robots1:
			robot.setFreq(freq)
		for robot in self.robots2:
			robot.setFreq(freq)
		for robot in self.robots3:
			robot.setFreq(freq)

	def setPause(self, status):
		dbg_dump('VERB', str(self.rid), 'setPause: ' + str(status))
		self.pause = status
		for robot in self.robots0:
			robot.setPause(status)
		for robot in self.robots1:
			robot.setPause(status)
		for robot in self.robots2:
			robot.setPause(status)
		for robot in self.robots3:
			robot.setPause(status)

	def setNumber(self, a0, a1, a2, a3):
		dbg_dump('VERB', str(self.rid), 'setNumber: ' + str(a0)+',' + str(a1)+',' + str(a2)+',' + str(a3))
		self.a0 = a0
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3
		if self.room_status != '1':
			return
		while a0 < len(self.robots0):
			robot = self.robots0.pop(len(self.robots0)-1)
			robot.close()
		while a1 < len(self.robots1):
			robot = self.robots1.pop(len(self.robots1)-1)
			robot.close()
		while a2 < len(self.robots2):
			robot = self.robots2.pop(len(self.robots2)-1)
			robot.close()
		while a3 < len(self.robots3):
			robot = self.robots3.pop(len(self.robots3)-1)
			robot.close()
		delay = 0
		while a0 > len(self.robots0):
			robot = Robot(self.rid, self.msgQueue, 0)
			robot.setDaemon(True)
			robot.setDelay(delay+random.random())
			robot.setFreq(self.freq)
			robot.setPause(self.pause)
			robot.start()
			self.robots0.append(robot)
			delay += self.interval
		while a1 > len(self.robots1):
			robot = Robot(self.rid, self.msgQueue, 1)
			robot.setDaemon(True)
			robot.setDelay(delay+random.random())
			robot.setFreq(self.freq)
			robot.setPause(self.pause)
			robot.start()
			self.robots1.append(robot)
			delay += self.interval
		while a2 > len(self.robots2):
			robot = Robot(self.rid, self.msgQueue, 2)
			robot.setDaemon(True)
			robot.setDelay(delay+random.random())
			robot.setFreq(self.freq)
			robot.setPause(self.pause)
			robot.start()
			self.robots2.append(robot)
			delay += self.interval
		while a3 > len(self.robots3):
			robot = Robot(self.rid, self.msgQueue, 3)
			robot.setDaemon(True)
			robot.setDelay(delay+random.random())
			robot.setFreq(self.freq)
			robot.setPause(self.pause)
			robot.start()
			self.robots3.append(robot)
			delay += self.interval

	def sendMsgs(self, msg_list, repeat, col=0):
		dbg_dump('VERB', str(self.rid), 'sendMsgs: ' + str(msg_list)+','+str(repeat))
		for i in range(0, repeat):
			msg = msg_list[random.randint(0, len(msg_list)-1)]
			self.msgQueue.put(msg)

	def getDict(self):
		dict = {}
		dict['freq'] = self.freq
		dict['pause'] = self.pause
		dict['interval'] = self.interval
		dict['a0'] = self.a0
		dict['a1'] = self.a1
		dict['a2'] = self.a2
		dict['a3'] = self.a3
		dict['ss'] = self.room_status
		threads = []
		for robot in self.robots0:
			if robot.isLogin:
				threads.append(robot.getDict())
		for robot in self.robots1:
			if robot.isLogin:
				threads.append(robot.getDict())
		for robot in self.robots2:
			if robot.isLogin:
				threads.append(robot.getDict())
		for robot in self.robots3:
			if robot.isLogin:
				threads.append(robot.getDict())
		dict['threads'] = threads
		dict['threads_num'] = len(threads)
		return dict