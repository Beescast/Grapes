
import socket
import time
import json
from utils import *
import datetime

MAX_RECV_SIZE = 40960

class Swfapi:
    def __init__(self, host, port):
        self.s = None  # Socket
        self.buff = None
        self.msg_buff = None
        self.stop_flag = False

        # Lock for avoiding race conditions when sending packets
        self.send_lock = threading.Lock()
        
        try:
            self.s = socket.create_connection((host, port)) # 
        except Exception, e:
            print (host, port, e)
            raise e

    def close(self):
        self.stop_flag = True
        self.s.close()
        print 'swfapi close'

    def receive(self):

        self.buff = ''
        self.msg_buff = ''

        while not self.stop_flag:

            data = self.s.recv(MAX_RECV_SIZE)

            if not data:
                time.sleep(0.01)
                continue
            yield data

    def send(self, data):
        self.send_lock.acquire()
        try:
            self.s.send(data)
        finally:
            self.send_lock.release()

    def xxSwfApi(self, req):
        req['req_t'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        req_str = json.dumps(req)
        self.send(req_str)

        data = self.s.recv(MAX_RECV_SIZE)

        data = data.encode('utf-8')
        rsp = json.loads(data)

        rst = deserialize(rsp["result"])

        return {'dict': rst, 'text': rsp["result"]}
