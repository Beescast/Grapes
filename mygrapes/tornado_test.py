# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import urllib
import json
import threading
import time
import datetime
import os
import sys
reload(sys)
from ctldanmu import *
from random import randint,random,sample
import threading
import MySQLdb
import MySQLdb.cursors
from tornado.options import define, options
define("port",default=8000,help="run on the given port",type=int)
define("host",default="0.0.0.0",help="run on the host",type=int)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
KEY = 'ad7c17900b894d8dbc508194fa9f0fc4'


def initialize():
    conn = MySQLdb.connect(
        host='192.168.3.56',
        port=1234,
        db='grapes',
        user='repl',
        passwd='Bees@0831@',
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor)
    db = conn.cursor()
    select_uid="select distinct uid from original_cookie"
    db.execute(select_uid)
    data=db.fetchall()
    for item in data:
        uid.append(item['uid'])
    conn.close()


def update(delay):
    while True:
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            cursorclass=MySQLdb.cursors.DictCursor)
        db = conn.cursor()
        info_sql = "select uid,dteventtime from cookie_used"
        db.execute(info_sql)
        data = db.fetchall()
        now=datetime.datetime.now()
        if data:
            for keys in data:
                if (now - keys['dteventtime']).seconds > 60:
                    update_sql = "update cookie_state set flag=0 where uid='%s'" % keys['uid']
                    db.execute(update_sql)
                    delete_sql = "delete from cookie_used where uid='%s'" % keys['uid']
                    db.execute(delete_sql)
        conn.commit()
        db.close()
        conn.close()
        time.sleep(delay)



class Application(tornado.web.Application):
    def __init__(self):
        self.lock = threading.Lock()
        handlers = [(r"/", IndexHandler),
                    (r"/login/([0-9]*)", Login),
                    (r"/stop/([0-9]*)", Stop),
                    (r"/info", Info),
                    (r"/update/(\w*)/([0-9]*)", Update),
                    (r"/cookie",Cookie),
                    (r"/barrage/([0-9]*)/([0-9]*)", Barrage)
                    ]
        tornado.web.Application.__init__(self, handlers, debug=False)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")


class Login(tornado.web.RequestHandler):
    def get(self,rid):
        data=CTL.start(rid)
        msg=""
        if data==1:
            msg="the room has been logined before!"
        if data==2:
            msg="login success!"
        if data==3:
            msg="the room is not online!"
        if data==4:
            msg="can not get the room info!"
        self.write(msg)


class Stop(tornado.web.RequestHandler):
    def get(self,rid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        before_rooms=[i for i in Danmucp.dmc_instance.keys()]
        try:
            CTL.stop(rid)
            delete_sql="delete from pradata where rid=%s"%rid
            cursor.execute(delete_sql)
            conn.commit()
            cursor.close()
            conn.close()

        except:
            pass
        data = {"before_rooms": before_rooms,
                "after_rooms": [i for i in Danmucp.dmc_instance.keys()]
                }
        self.write(data)

class Info(tornado.web.RequestHandler):
    def get(self):
        data={"delay":CTL.delay,
              "topk":wordcut.topk,
              "timestep":wordcut.timestep,
              "rooms":[i for i in Danmucp.dmc_instance.keys()]
              }
        self.write(data)

class Update(tornado.web.RequestHandler):
    def get(self, key, value):
        if key == "delay":
            CTL.delay = int(value)
        if key == "topk":
            wordcut.topk = int(value)
        if key == "timestep":
            wordcut.timestep = int(value)

        data = {"delay": CTL.delay,
                "topk": wordcut.topk,
                "timestep": wordcut.timestep
                }
        self.write(data)


class Cookie(tornado.web.RequestHandler):
    def get(self):
        self.application.lock.acquire()
        rid = self.get_argument('rid', '')
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        flag=0
        cookie={}
        if rid:
            # 查询是否有cookie可用
            get_cookie = "select uid,name,level,cookie from cookie_state where flag=0 and rids like '%s' order by level DESC, rand()  limit 1"%('%'+rid+'%')
            cursor.execute(get_cookie)
            data = cursor.fetchone()
            if data:
                uid=data['uid']
                name=data['name']
                level=data['level']
                dteventtime=datetime.datetime.now()
                cookie=json.loads(data['cookie'])
                update_cookie_state="update cookie_state set flag=1 where uid='%s'"%(uid)
                cursor.execute(update_cookie_state)
                conn.commit()
                insert_cookie_used="insert into cookie_used(uid,name,level,rid,dteventtime) values('%s','%s','%s','%s','%s')"%(uid,name,level,rid,dteventtime)
                cursor.execute(insert_cookie_used)
                conn.commit()
                cursor.close()
            else:
                flag=1
        else:
            get_cookie = "select uid,name,level,cookie from cookie_state where flag=0  and rids=0 order by rand() limit 1 "
            cursor.execute(get_cookie)
            data = cursor.fetchone()
            if data:
                uid = data['uid']
                name = data['name']
                dteventtime = datetime.datetime.now()
                cookie = json.loads(data['cookie'])
                update_cookie_state = "update cookie_state set flag=1 where uid='%s'" % (uid)
                cursor.execute(update_cookie_state)
                conn.commit()
                insert_cookie_used = "insert into cookie_used(uid,name,dteventtime) values('%s','%s','%s')" % (uid, name,dteventtime)
                cursor.execute(insert_cookie_used)
                conn.commit()
                cursor.close()
            else:
                flag=2
        if flag:
            self.write("no cookie!!!")
        else:
            self.set_header('Access-Control-Allow-Origin', '*')
            self.write(cookie)
        conn.close()
        self.application.lock.release()


class Barrage(tornado.web.RequestHandler):
    def get(self,rid,uid):
        self.application.lock.acquire()
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        data={"if_send":0,"msg":""}
        update_sql = "update cookie_used set dteventtime='%s' where uid='%s'" % (datetime.datetime.now(), uid)
        cursor.execute(update_sql)
        rand = random()
        if rand > 0.5:
            query_sql = "select * from pradata where rid='%s' and flag=0 ORDER by type limit 1" % rid
        else:
            query_sql = "select * from pradata where rid='%s'  and flag=0 ORDER by type DESC limit 1" % rid
        cursor.execute(query_sql)
        tmp=cursor.fetchone()
        if tmp:
            data = {"if_send": 1, "msg": tmp['txt']}
            del_sql = "update pradata set flag=1 where id='%s'" % tmp['id']
            cursor.execute(del_sql)
        conn.commit()
        cursor.close()
        conn.close()
        print "msg:",data['msg']
        self.write(data)
        self.application.lock.release()


if __name__ == "__main__":
    initialize()
    ts = threading.Thread(target=update, args=((10,)))
    ts.start()
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    # http_server.bind(options.port, options.host)
    # http_server.start(0)
    # tornado.ioloop.IOLoop.current().start()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


