# coding=utf-8

import random
import time
import json
import threading
import requests
import Queue
from room import Room

class RoomsManage(threading.Thread):
	def __init__(self):
		super(RoomsManage, self).__init__()
		self.cmd_callback_list = {
			'addroom':self.addroom_hdlr,
			'delroom':self.delroom_hdlr,
			'pause':self.pause_hdlr,
			'freq':self.freq_hdlr,
			'interval':self.interval_hdlr,
			'num':self.num_hdlr,
			'sendmsgs':self.sendmsgs_hdlr,
		}
		self.rooms = {}  # 1876728, 592766
		self.cmdQueue = Queue.Queue()
		self.isRunning = False
		self.mutex = threading.Lock()

	def addroom_hdlr(self, cmd):
		rid = cmd['rid']
		if str(rid) not in self.rooms:
			room = Room(rid)
			room.setDaemon(True)
			room.start()
			self.rooms[str(rid)] = room

	def delroom_hdlr(self, cmd):
		rid = cmd['rid']
		try:
			room = self.rooms.pop(str(rid))
			if room:
				room.close()
		except:
			pass

	def pause_hdlr(self, cmd):
		rid = cmd['rid']
		status = cmd['status']
		room = self.rooms.get(str(rid))
		if room:
			room.setPause(status)

	def freq_hdlr(self, cmd):
		rid = cmd['rid']
		freq = cmd['freq']
		room = self.rooms.get(str(rid))
		if room:
			room.setFreq(freq)

	def interval_hdlr(self, cmd):
		rid = cmd['rid']
		interval = cmd['interval']
		room = self.rooms.get(str(rid))
		if room:
			room.setInterval(interval)

	def num_hdlr(self, cmd):
		rid = cmd['rid']
		a0 = cmd['a0']
		a1 = cmd['a1']
		a2 = cmd['a2']
		a3 = cmd['a3']
		room = self.rooms.get(str(rid))
		if room:
			room.setNumber(a0, a1, a2, a3)

	def sendmsgs_hdlr(self, cmd):
		rid = cmd['rid']
		msg_list = cmd['msgs']
		repeat = cmd['repeat']
		col = cmd['col']
		room = self.rooms.get(str(rid))
		if room and msg_list:
			room.sendMsgs(msg_list, repeat, col)

	def run(self):
		self.isRunning = True
		while self.isRunning:
			if not self.cmdQueue.empty():
				cmd = self.cmdQueue.get()
				cmd_type = cmd['type']
				function = self.cmd_callback_list.get(cmd_type)
				if function:
					function(cmd)
			else:
				time.sleep(1)

	def setPause(self, rid, status):  # True=pause; False=play
		cmd = {}
		cmd['type'] = 'pause'
		cmd['rid'] = rid
		cmd['status'] = status
		self.cmdQueue.put(cmd)

	def sendMsgs(self, rid, msg_list, repeat=-1, col=0):
		if repeat > 0:
			cmd = {}
			cmd['type'] = 'sendmsgs'
			cmd['rid'] = rid
			cmd['msgs'] = msg_list
			cmd['repeat'] = repeat
			cmd['col'] = col
			self.cmdQueue.put(cmd)

	def setFreq(self, rid, freq):
		if freq < 20:
			freq = 20
		cmd = {}
		cmd['type'] = 'freq'
		cmd['rid'] = rid
		cmd['freq'] = freq
		self.cmdQueue.put(cmd)

	def setNumber(self, rid, a0, a1, a2, a3):
		if a0 < 0:
			a0 = 0
		if a1 < 0:
			a1 = 0
		if a2 < 0:
			a2 = 0
		if a3 < 0:
			a3 = 0
		cmd = {}
		cmd['type'] = 'num'
		cmd['rid'] = rid
		cmd['a0'] = a0
		cmd['a1'] = a1
		cmd['a2'] = a2
		cmd['a3'] = a3
		self.cmdQueue.put(cmd)

	def addRoom(self, rid):
		cmd = {}
		cmd['type'] = 'addroom'
		cmd['rid'] = rid
		self.cmdQueue.put(cmd)

	def delRoom(self, rid):
		cmd = {}
		cmd['type'] = 'delroom'
		cmd['rid'] = rid
		self.cmdQueue.put(cmd)

	def setInterval(self, rid, interval):
		if interval < 0:
			interval = 0
		cmd = {}
		cmd['type'] = 'interval'
		cmd['rid'] = rid
		cmd['interval'] = interval
		self.cmdQueue.put(cmd)

	def close(self):
		self.isRunning = False
		for rid in self.rooms:
			room = self.rooms[rid]
			room.close()

	def roomsinfo(self):
		print 'unknown'

	def getDict(self):
		dict = {}
		for key in self.rooms:
			room = self.rooms[key]
			dict[str(room.rid)] = room.getDict()
		return dict