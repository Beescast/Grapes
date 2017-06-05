from socks import *
import threading
import time
import urllib2
import random

poxys = [
{'proxytype':PROXY_TYPE_HTTP, 'addr':'60.21.132.218', 'port':63000, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'27.22.204.225', 'port':8118, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'180.76.154.5', 'port':8888, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'175.155.244.82', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'60.169.78.218', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'183.157.180.108', 'port':80, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'139.224.237.33', 'port':8888, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'110.73.55.101', 'port':8123, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'121.204.165.224', 'port':8118, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'58.209.151.126', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'119.5.0.14', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'36.249.28.170', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'115.213.203.38', 'port':808, 'count':0},
{'proxytype':PROXY_TYPE_HTTP, 'addr':'116.226.90.12', 'port':808, 'count':0},
		]

poxys = []
mutex = None

def updateThread():
	global poxys
	while (True):
		print 'Update poxys.'
		try:
			response = urllib2.urlopen('http://api.xicidaili.com/free2016.txt')
			content = response.read()
		except Exception, e:
			print e
			continue
		ip_list = content.split('\r\n')
		mutex.acquire()
		poxys = []
		for ip in ip_list:
			ipinfo = ip.split(':')
			addr = ipinfo[0]
			port = int(ipinfo[1])
			poxys.append({'proxytype':PROXY_TYPE_HTTP, 'addr':addr, 'port':port, 'count':0})
		mutex.release()
		time.sleep(15*60)

class MyPoxy:
	@staticmethod
	def startUpdate():
		global mutex
		if not mutex:
			mutex = threading.Lock()
		t = threading.Thread(target=updateThread)
		t.setDaemon(True)
		t.start()

	@staticmethod
	def getPoxy():
		global mutex
		global poxys
		mutex.acquire()
		index = random.randint(0, len(poxys)-1)
		if len(poxys) > 0:
			p = poxys[index]
		else:
			p = None
		mutex.release()
		return p

	@staticmethod
	def delPosy(p):
		global mutex
		global poxys
		mutex.acquire()
		poxys.remove(p)
		mutex.release()

	@staticmethod
	def setError(p):
		global mutex
		global poxys
		mutex.acquire()
		p['count'] += 1
		if p['count'] > 10:
			poxys.remove(p)
		mutex.release()