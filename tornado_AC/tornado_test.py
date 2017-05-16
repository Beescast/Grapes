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
from conf import danmu_back
from danmu_data_v2 import Danmucp
from random import randint,random,sample,choice
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
        db='test',
        user='repl',
        passwd='0831@Bees',
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
            port=3306,
            db='test',
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
        self.room_data = {}
        handlers = [(r"/", IndexHandler),
                    (r"/login/([0-9]*)", Login),
                    (r"/stop/([0-9]*)", Stop),
                    (r"/info", Info),
                    (r"/update", Update),
                    (r"/cookie",Cookie),
                    (r'/adcookie',AdCookie),
                    (r"/barrage/([0-9]*)/([0-9]*)", Barrage),
                    (r"/ctypeinfo", Ctypeinfo),
                    (r'/colordanmu',SaveColorDanmu),
                    (r'/updatecolor/(\d+)',UpdateColor),
                    (r'/roominfo/(\d+)',RoomInfo),
                    ]
        tornado.web.Application.__init__(self, handlers, debug=False,
                                         template_path=os.path.join(os.path.dirname(__file__), "templates")
                                         )


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class Login(tornado.web.RequestHandler):
    def get(self,rid):
        if rid not in self.application.room_data:
            self.application.room_data[rid] = {}
            self.application.room_data[rid]['danmucp'] = Danmucp()
            self.application.room_data[rid]['word'] = wordcut()
            self.application.room_data[rid]['ctl'] = CTL()
            data=CTL.start(rid,self.application.room_data)
        else:
            data = 1
        msg=""
        status={}
        if data==1:
            msg="the room has been logined before!"
        if data==2:
            msg="login success!"
        if data==3:
            msg="the room is not online!"
            self.application.room_data.pop(rid)
        if data==4:
            msg="can not get the room info!"
            self.application.room_data.pop(rid)
        status={"status":data,"msg":msg}
        self.write(status)


class Stop(tornado.web.RequestHandler):
    def get(self,rid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        before_rooms=[i for i in Danmucp.dmc_instance.keys()]
        try:
            CTL.stop(rid)
            del self.application.room_data[rid]
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
        data = {}
        data['rooms'] = [i for i in Danmucp.dmc_instance.keys()]
        data['info'] = []
        for key in Danmucp.dmc_instance.keys():
            room = self.application.room_data.get(key,'')
            if room:
                dp = room['danmucp']
                info = {'rid':key,'total':dp.total,"bweight":dp.bweight,"tweight":dp.tweight,"sweight":dp.sweight,
                        'timestep':room['word'].timestep,'topk':room['word'].topk,'delay':room['ctl'].delay}
                data['info'].append(info)
        self.write(json.dumps(data))

class RoomInfo(tornado.web.RequestHandler):
    def get(self,rid):
        result = {}
        if rid not in self.application.room_data:
            result = {'code':0,'msg':'the rid is not login'}
        else:
            roomdata = self.application.room_data[rid]
            danmucp = roomdata['danmucp']
            word = roomdata['word']
            ctl = roomdata['ctl']
            total = danmucp.total
            bw = danmucp.bweight
            tw = danmucp.tweight
            sw = danmucp.sweight
            timestep = word.timestep
            topk = word.topk
            delay = ctl.delay
            data = {'total':total,'bw':bw,'tw':tw,'sw':sw,'timestep':timestep,'topk':topk,'delay':delay}
            result = {'code':1,'data':data}
        self.write(result)

class Update(tornado.web.RequestHandler):
    def get(self):
        self.render('update.html')
    def post(self):
        data = json.loads(self.request.body)
        rid = data.get('rid','')
        self.set_header('Access-Control-Allow-Origin', '*')
        if not rid or rid not in self.application.room_data:
            self.write({'code':1,'msg':'rid is not found'})
            self.finish()
            return
        room = self.application.room_data[rid]
        total = room['danmucp'].total
        bw = room['danmucp'].bweight
        tw = room['danmucp'].tweight
        sw = room['danmucp'].sweight
        delay = room['ctl'].delay
        timestep = room['word'].timestep
        topk = room['word'].topk

        if 'total' in data and data['total']:
            try:
                total = int(data['total'])
            except:
                self.write({'code':1,'msg':'total is not integer'})
                self.finish()
                return
        if 'bweight' in data:
            try:
                bw = float(data['bweight'])
            except:
                self.write({'code':1,'msg':'bweight is not float'})
                self.finish()
                return
        if 'tweight' in data:
            try:
                tw = float(data['tweight'])
            except:
                self.write({'code':1,'msg':'tweight is not float'})
                self.finish()
                return
        if 'sweight' in data:
            try:
                sw = float(data['sweight'])
            except:
                self.write({'code':1,'msg':'sweight is not float'})
                self.finish()
                return
        if 'delay' in data and data['delay']:
            try:
                delay = float(data['delay'])
            except:
                self.write({'code':1,'msg':'delay is not float'})
                self.finish()
                return
        if 'timestep' in data and data['timestep']:
            try:
                timestep = float(data['timestep'])
            except:
                self.write({'code':1,'msg':'timestep is not float'})
                self.finish()
                return
        if 'topk' in data and data['topk']:
            try:
                topk = int(data['topk'])
            except:
                self.write({'code':1,'msg':'topk is not integer'})
                self.finish()
                return
        self.application.room_data[rid]['danmucp'].total = total
        self.application.room_data[rid]['danmucp'].bweight = bw
        self.application.room_data[rid]['danmucp'].tweight = tw
        self.application.room_data[rid]['danmucp'].sweight = sw
        self.application.room_data[rid]['word'].timestep = timestep
        self.application.room_data[rid]['word'].topk = topk
        self.application.room_data[rid]['ctl'].delay = delay
        self.write({'code':0,'msg':'update success'})


class Ctypeinfo(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        rid = int(self.get_argument('rid', '0'))
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            charset='utf8',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        # rids = []
        # try:
        #     cursor.execute("select distinct rid from original_acc")
        #     for i in cursor.fetchall():
        #         rids.append(str(i['rid']))
        # except:
        #     pass
        #
        # if str(rid) not in rids:
        #     rid=0

        sql0 = 'select count(*) as num from original_acc where flag=0 and bat_type=0 and datediff(curdate(), get_time)<7'
        cursor.execute(sql0)
        data0 = cursor.fetchone()
        sql1 = 'select count(*) as num from original_acc where flag=0 and bat_type=1 and datediff(curdate(), get_time)<7'
        cursor.execute(sql1)
        data1 = cursor.fetchone()
        sql2 = 'select count(*) as num from original_acc where flag=0 and rid="%s" and FIND_IN_SET(2,bat_type) and datediff(curdate(), get_time)<7' % rid
        cursor.execute(sql2)
        data2 = cursor.fetchone()
        sql3 = 'select count(*) as num from original_acc where flag=0 and rid="%s" and FIND_IN_SET(3,bat_type) and datediff(curdate(), get_time)<7' % rid
        cursor.execute(sql3)
        data3 = cursor.fetchone()
        # the_sql = """
        #   SELECT rid,LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '0','')) as zero,
        #   LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '1','')) as one,
        # LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '2','')) as two,
        #   LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '3','')) as three
        #   from
        #  (select
        #   rid, group_concat(bat_type) as bstr from  original_acc where flag=0 and rid='%s' and datediff(curdate(), get_time)<7
        #  group by rid) a"""%rid
        conn.close()
        msg = {"0": int(data0['num']),
               "1": int(data1['num']),
               "2": int(data2['num']),
               "3": int(data3['num'])
               }
        self.write(msg)


class Cookie(tornado.web.RequestHandler):
    def get(self):
        self.application.lock.acquire()
        if "SlimerJS" in self.request.headers['User-Agent']:
            gift=1
        else:
            gift=0
        color = int(self.get_argument('color','0'))
        rid = int(self.get_argument('rid','0'))
        ctype = int(self.get_argument('type','0'))
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        flag=0
        cookie={}
        rids=[]
        data={}
        try:
            cursor.execute("select distinct tag from original_acc")
            for i in cursor.fetchall():
                rids.append(str(i['tag']))
        except:
            pass

        if str(rid) not in rids:
            rid=0

        if gift:
            select_sql="select uid,name,lev,cookie from original_acc where flag=0 and giftstatus=0 and datediff(curdate(), get_time)<7 limit 1"
        else:
            if not color:
                select_sql = "select uid,name,lev,cookie from original_acc where flag=0 and rid='%s' and FIND_IN_SET('%s',bat_type) and datediff(curdate(), get_time)<7 limit 1" % (rid, ctype)
            else:
                select_sql = "select uid,name,lev,cookie from original_acc where flag=0 and color>0 and rid='%s' and FIND_IN_SET('%s',bat_type) and datediff(curdate(), get_time)<7 limit 1" % (
                rid, ctype)
        try:
            print 'select_sql:',select_sql
            cursor.execute(select_sql)
            data = cursor.fetchone()
        except:
            pass
        if data:
            uid = data['uid']
            name = data['name']
            level = data['lev']
            dteventtime = datetime.datetime.now()
            cookie = json.loads(data['cookie'])
            select_color = 'select color from original_acc where uid="%s"' % uid
            cursor.execute(select_color)
            colors = cursor.fetchone()
            color_count = colors['color']
            update_cookie_state = "update original_acc set flag=1,giftstatus='%s' where uid='%s'" % (gift,uid)
            print 'update_cookie:',update_cookie_state
            cursor.execute(update_cookie_state)
            conn.commit()
            print 'update cookie state success'
            insert_cookie_used = "insert into cookie_used(uid,name,level,rid,dteventtime) values('%s','%s','%s','%s','%s')" % (
            uid, name, level, rid, dteventtime)
            print 'insert cookie:',insert_cookie_used
            cursor.execute(insert_cookie_used)
            conn.commit()
            print 'insert cookie used success'
            cursor.close()
        # else:
        #     if not gift:
        #         sql = 'select uid,name,lev,cookie from original_acc where flag=0 and tag=0 and find_in_set("0",bat_type) and datediff(curdate(),get_time)<7 limit 1'
        #         cursor.execute(sql)
        #         data2 = cursor.fetchone()
        #         if data2:
        #             uid = data2['uid']
        #             name = data2['name']
        #             level = data2['lev']
        #             dteventtime = datetime.datetime.now()
        #             cookie = json.loads(data2['cookie'])
        #             update_cookie_state = "update original_acc set flag=1,giftstatus='%s' where uid='%s'" % (gift, uid)
        #             cursor.execute(update_cookie_state)
        #             conn.commit()
        #             insert_cookie_used = "insert into cookie_used(uid,name,level,rid,dteventtime) values('%s','%s','%s','%s','%s')" % (
        #                 uid, name, level, rid, dteventtime)
        #             cursor.execute(insert_cookie_used)
        #             conn.commit()
        #             cursor.close()
        else:
            flag = 1
        self.set_header('Access-Control-Allow-Origin', '*')
        if flag:
            self.write({'cookie':"no cookie!!!",'color':0})
        else:
            self.write({'cookie':cookie,'color':color_count})
        conn.close()
        self.application.lock.release()

class AdCookie(tornado.web.RequestHandler):
    def get(self):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            charset='utf8',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        sql = 'select cookie from ad_cookie order by rand() limit 1'
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            cookie = data['cookie']
        else:
            cookie = ''
        self.write(cookie)
        cursor.close()
        conn.close()

class Barrage(tornado.web.RequestHandler):
    def get(self,rid,uid):
        self.application.lock.acquire()
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
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
        else:
            dm = choice(danmu_back)
            data = {'if_send':1,'msg':dm}
        conn.commit()
        cursor.close()
        conn.close()
        print "msg:",data['msg']
        self.write(data)
        self.application.lock.release()

class SaveColorDanmu(tornado.web.RequestHandler):
    def post(self):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            charset='utf8',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        data = json.loads(self.request.body)
        print data
        uid = int(data.get('uid','0'))
        num = int(data.get('color_num','0'))
        update_sql = 'update original_acc set color=%s where uid="%s"' % (num,uid)
        try:
            cursor.execute(update_sql)
            conn.commit()
            info = {'code':0,'msg':'update success'}
        except:
            conn.rollback()
            info = {'code':1,'msg':'update failed'}
        cursor.close()
        conn.close()
        self.set_header('Access-Control-Allow-Origin','*')
        self.write(info)

class UpdateColor(tornado.web.RequestHandler):
    def get(self,uid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='test',
            user='repl',
            charset='utf8',
            passwd='0831@Bees',
            cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        update_sql = 'update original_acc set color=color-1 where uid="%s"' % uid
        try:
            cursor.execute(update_sql)
            conn.commit()
            self.write('update success')
        except:
            conn.rollback()
            self.write('update failed')
        cursor.close()
        conn.close()



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


