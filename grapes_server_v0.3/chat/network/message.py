
from utils import *


class Message:
	def __init__(self, body):
		self._serialized_size = 0
		self.raw = ""

		self.body = body

	def to_text(self):
		text = serialize(self.body)
		return text

	def size(self):
		return self._serialized_size

	def attr(self, attr_name):
		if self.body is None:
			return None
		try:
			result = self.body[attr_name]
			return result
		except KeyError as e:
			return None

	@staticmethod
	def sniff(buff):

		if buff is None or len(buff) <= 0:
			return None

		msg_bodies = buff.split('\0')
		if len(msg_bodies) <= 1:
			return None

		return Message.from_raw(msg_bodies[0])

	@staticmethod
	def from_raw(raw):
		result = Message(deserialize(raw))
		result._serialized_size = len(raw)
		result.raw = raw
		return result
