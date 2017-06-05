
import socket
import time
import threading
from packet import Packet
from message import Message
import socks
from poxy import MyPoxy

MAX_RECV_SIZE = 40960

from utils import *

class Client:
	def __init__(self, host, port):
		self.buff = None
		self.msg_buff = None
		self.isRunning = True
		self.host = host
		self.port = port

		# Lock for avoiding race conditions when sending packets
		self.send_lock = threading.Lock()

		self.s = None
		if True: # True   False
			self.s = socket.create_connection((host, port))
		else:
			while self.isRunning and (not self.s):
				try:
					self.s = socks.socksocket()
					p = MyPoxy.getPoxy()
					self.s.setproxy(p['proxytype'], p['addr'], p['port'])
					self.s.connect((host, port))
				except Exception, e:
					print e
					# MyPoxy.setError(p)
					self.s = None
					time.sleep(1)

	def close(self):
		self.isRunning = False
		if self.s:
			self.s.close()
			self.s = None
		#print 'client close'

	def receive(self):

		self.buff = ''
		self.msg_buff = ''

		while self.isRunning:
			try:
				data = self.s.recv(MAX_RECV_SIZE)
			except Exception, e:
				print (self.host, self.port, e)
				raise e

			if not data:
				time.sleep(0.01)
				continue

			self.buff += data

			while self.isRunning:

				packet = Packet.sniff(self.buff)
				if packet is None:
					break

				# Slice buffer
				self.buff = self.buff[packet.size():]

				# Append text data
				self.msg_buff += packet.body

				while self.isRunning:

					message = Message.sniff(self.msg_buff)
					if message is None:
						break

					# Slice message buffer
					self.msg_buff = self.msg_buff[(message.size() + 1):]  # +1 means to skip '\0' in the end

					yield message

	def send(self, message_body):
		self.send_lock.acquire()
		if self.s:
			try:
				self.s.send(Packet(Message(message_body).to_text()).to_raw())
			except Exception, e:
				print (self.host, self.port, e)
				self.send_lock.release()
				raise e
		self.send_lock.release()

	def send_text(self, message_text):
		message_text = message_text.encode('utf-8')
		self.send_lock.acquire()
		if self.s:
			try:
				self.s.send(Packet(message_text).to_raw())
			except Exception, e:
				print (self.host, self.port, e)
				self.send_lock.release()
				raise e
		self.send_lock.release()
