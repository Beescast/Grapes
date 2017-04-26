
import network.client
import threading
import time
import logging

RAW_BUFF_SIZE = 4096
KEEP_ALIVE_INTERVAL_SECONDS = 40

HOST = 'openbarrage.douyutv.com'
PORT = 8601

class ChatRoom(threading.Thread):

    def __init__(self, rid):
        super(ChatRoom, self).__init__()
        self.rid = rid
        self.client = None
        self.channel_id = -9999  # Convention
        self.callbacks = {}
        self.stop_flag = False

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
            return

        if callback_list is None or len(callback_list) <= 0:
            return

        for callback in callback_list:
            callback(message)

    # Start running
    def run(self):

        self.client = network.client.Client(HOST, PORT)

        # Send AUTH request
        self.client.send({'type': 'loginreq','roomid': str(self.rid)})

        # Start a thread to send KEEPALIVE messages separately
        threading.Thread(target=self.keep_alive, args=(self.client, KEEP_ALIVE_INTERVAL_SECONDS)).start()

        # Handle messages
        for message in self.client.receive():

            if not message:
                continue

            # print json.dumps(message.body)
            msg_type = message.attr('type')

            # Send JOIN_GROUP request
            if msg_type == 'loginres':
                self.client.send({'type': 'joingroup', 'rid': str(self.rid), 'gid': self.channel_id})

            self.trigger_callbacks(msg_type, message)

    # Keep-Alive thread func
    def keep_alive(self, client, delay):
        while not self.stop_flag:
            current_ts = int(time.time())
            client.send({
                'type': 'keeplive',
                'tick': current_ts
            })
            time.sleep(delay)

    def close(self):
        if self.client:
            self.client.close()
            self.client = None