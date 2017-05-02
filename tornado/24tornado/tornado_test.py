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
        port=3306,
        db='grapes',
        user='repl',
        passwd='0831@Bees',
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor)
    db = conn.cursor()
    select_uid="select distinct uid from original_acc"
    db.execute(select_uid)
    data=db.fetchall()
    for item in data:
        uid.append(item['uid'])
    conn.close()


def update(delay):
    while True:
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        db = conn.cursor()
        info_sql = "select uid,dteventtime from cookie_used"
        db.execute(info_sql)
        data = db.fetchall()
        now=datetime.datetime.now()
        if data:
            for keys in data:
                if (now - keys['dteventtime']).seconds > 60:
                    update_sql = "update original_acc set flag=0 where uid='%s'" % keys['uid']
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
                    (r"/barrage/([0-9]*)/([0-9]*)", Barrage),
                    (r"/ctypeinfo", Ctypeinfo)
                    ]
        tornado.web.Application.__init__(self, handlers, debug=False,
                                         template_path=os.path.join(os.path.dirname(__file__), "templates")
                                         )


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class Login(tornado.web.RequestHandler):
    def get(self,rid):
        data=CTL.start(rid)
        msg=""
        status={}
        if data==1:
            msg="the room has been logined before!"
        if data==2:
            msg="login success!"
        if data==3:
            msg="the room is not online!"
        if data==4:
            msg="can not get the room info!"
        status={"status":data,"msg":msg}
        self.write(status)


class Stop(tornado.web.RequestHandler):
    def get(self,rid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
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
        data={"消息更新间隔":CTL.delay,
              "关键词提取数量":wordcut.topk,
              "消息间隔时间":wordcut.timestep,
              "备用消息提取比列":Danmucp.bweight,
              "实时消息提取比例": Danmucp.tweight,
              "自编消息提取比例": Danmucp.sweight,
              "监控房间号":[i for i in Danmucp.dmc_instance.keys()]
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
        if key == "bweight":
            Danmucp.bweight = int(value)
        if key == "tweight":
            Danmucp.tweight = int(value)
        if key == "sweight":
            Danmucp.sweight = int(value)

        data = {"delay": CTL.delay,
                "topk": wordcut.topk,
                "timestep": wordcut.timestep,
                "bweight":Danmucp.bweight,
                "tweight":Danmucp.tweight,
                "sweight":Danmucp.sweight
                }
        self.write(data)


class Ctypeinfo(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        rid = int(self.get_argument('rid', '0'))
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            charset='utf8',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        rids = []
        try:
            cursor.execute("select distinct tag from original_acc")
            for i in cursor.fetchall():
                rids.append(str(i['tag']))
        except:
            pass

        if str(rid) not in rids:
            rid=0


        the_sql = """SELECT tag,LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '0','')) as zero,
          LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '1','')) as one,
        LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '2','')) as two,
          LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '3','')) as three
          from
         (select
          tag, group_concat(bat_type) as bstr from  original_acc where tag='%s' and flag=0
         group by tag) a"""%rid
        cursor.execute(the_sql)
        data = cursor.fetchone()
        conn.close()
        msg = {"0": int(data['zero']),
               "1": int(data['one']),
               "2": int(data['two']),
               "3": int(data['three'])
               }
        self.write(msg)




class Cookie(tornado.web.RequestHandler):
    def get(self):
        self.application.lock.acquire()
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        rid = int(self.get_argument('rid', '0'))
        ctype = int(self.get_argument('type', '0'))
        flag=0
        cookie={}
        rids=[]
        cursor.execute("select distinct tag from original_acc")
        for i in cursor.fetchall():
            rids.append(str(i['tag']))
        if str(rid) not in rids:
            rid=0

        if "SlimerJS" in self.request.headers['User-Agent']:
            gift=1
            select_sql = "select uid,name,lev,cookie from original_acc where flag=0 and giftcount=0 and datediff(curdate(), get_time)<7 limit 1"
        else:
            gift=0
            select_sql = "select uid,name,lev,cookie from original_acc where flag=0 and tag='%s' and FIND_IN_SET('%s',bat_type) and datediff(curdate(), get_time)<7 limit 1" % (rid, ctype)
        cursor.execute(select_sql)
        data = cursor.fetchone()
        if data:
            uid = data['uid']
            name = data['name']
            level = data['lev']
            dteventtime = datetime.datetime.now()
            cookie = json.loads(data['cookie'])
            update_cookie_state = "update original_acc set flag=1,giftcount='%s' where uid='%s'" % (gift,uid)
            cursor.execute(update_cookie_state)
            conn.commit()
            insert_cookie_used = "insert into cookie_used(uid,name,level,rid,dteventtime) values('%s','%s','%s','%s','%s')" % (
            uid, name, level, rid, dteventtime)
            cursor.execute(insert_cookie_used)
            conn.commit()
            cursor.close()
        else:
            flag = 1
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
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
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


