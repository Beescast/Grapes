# -*- coding: utf-8 -*-
from danmu import DanMuClient
import Queue
import datetime
import time
from conf import *
import cmd
import re
import jieba
import jieba.analyse
import jieba.posseg
jieba.initialize()
# jieba.enable_parallel(4)
import random
import MySQLdb
import MySQLdb.cursors
import cStringIO
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def filter_msg(msg):
    msgHandler(msg)
    msg['enable'] = True
    if not msg['txt']:
        msg['enable'] = False
    else:
        for reg in regexp:
            try:
                if reg.search(msg['txt'].encode('utf-8')) or len(msg['txt']) <= 3:
                    msg['enable'] = False
                    return
            except Exception,e:
                msg['enable'] = False
    return
def msgHandler(msg):
    txt = msg['txt']
    txt = reg1.sub(''.decode('utf-8'),txt)
    txt = reg2.sub(''.decode('utf-8'),txt)
    msg['txt'] = txt


class wordcut():
    timestep = 20  #消息提取间隔时间
    topk=30  #选择关键词数量

    @staticmethod
    def data_get(rid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        db = conn.cursor()
        now=datetime.datetime.now()
        stime=now.strftime("%Y-%m-%d %H:%M:%S")
        etime=(now - datetime.timedelta(seconds=wordcut.timestep)).strftime("%Y-%m-%d %H:%M:%S")
        data={}
        select_sql="""select distinct txt from chatdata where rid='%s' and dteventtime>='%s' and dteventtime<='%s';"""\
                   %(rid,etime,stime)
        db.execute(select_sql)
        data =db.fetchall()
        conn.commit()
        return data

    @classmethod
    def getwords(cls,rid):
        data=cls.data_get(rid)
        txt=''
        for sentence in data:
            tmp=re.sub("[a-zA-Z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),sentence["txt"])
            segs=jieba.cut(tmp,cut_all=False)
            for seg in segs:
                seg = seg.encode('utf-8')
                if seg not in stopwords:
                    txt+=seg

        tags = jieba.analyse.textrank(txt, topK=cls.topk)
        return "|".join(tags)




class Danmucp(cmd.Cmd):
    dmc_instance = {}  # 保存房间对象
    mysql_instance={}
    bweight=60
    tweight=30
    sweight=10
    @classmethod
    def start(cls,rid):
        dmc = DanMuClient('http://www.douyu.com/%s'%rid)
        cls.dmc_instance[rid]=dmc
        cls.mysql_instance[rid]= MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        @dmc.danmu
        def danmu_fn(msg): #填充实时消息
            try:
                if str(msg['uid']) not in uid:
                    filter_msg(msg)
                    if msg['enable']:
                        cursor = cls.mysql_instance[rid].cursor()
                        insert_data = "insert into chatdata(rid,txt,dteventtime) values('%s','%s','%s')" % (
                            msg['rid'], msg['Content'], datetime.datetime.now())
                        cursor.execute(insert_data)
                        cls.mysql_instance[rid].commit()
            except:
                cls.mysql_instance[rid].close()
                cls.mysql_instance[rid] = MySQLdb.connect(
                    host='192.168.3.56',
                    port=3306,
                    db='grapes',
                    user='repl',
                    passwd='0831@Bees',
                    charset='utf8',
                    cursorclass=MySQLdb.cursors.DictCursor)
        dmc.start(blockThread=False)

    @classmethod
    def getmessage(cls,rid):
        myconn = MySQLdb.connect(
            host='192.168.3.56',
            port=3306,
            db='grapes',
            user='repl',
            passwd='0831@Bees',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        db = myconn.cursor()
        cate_id=room_type[rid]  #查询房间类型
        keys = wordcut.getwords(rid) #获取最近弹幕关键字
        danmu_data=[]
        before_now = (datetime.datetime.now() - datetime.timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        delete_history = "delete from pradata where rid='%s'" % rid
        insert_danmu = "insert into pradata (rid,txt,type,flag) values(%s,%s,%s,%s)"
        if keys:
            select_back_danmu="select distinct txt from danmu_bac_data where rid='%s' and txt REGEXP '%s' ORDER by rand() limit %s"%(rid,keys,cls.bweight)
            select_self_danmu = "select distinct txt from self_danmu  ORDER by rand() limit %s" % (cls.sweight)
            select_true_danmu ="select distinct txt from chatdata where dteventtime>='%s' and rid='%s' and txt REGEXP '%s' ORDER by rand() limit %s "% (before_now,rid,keys,cls.tweight)
        else:
            select_back_danmu = "select distinct txt from danmu_bac_data where rid='%s'  ORDER by rand() limit %s" % (rid, cls.bweight)
            select_self_danmu = "select distinct txt from self_danmu  ORDER by rand() limit %s" % (cls.sweight)
            select_true_danmu = "select distinct txt from chatdata where dteventtime>='%s' and rid='%s' ORDER by rand() limit %s"%(before_now, rid, cls.tweight)
        try:
            db.execute(select_back_danmu)
            tmp1 = db.fetchall()
            if tmp1:
                for item in tmp1:
                    a = (rid, item['txt'], 0, 0)
                    danmu_data.append(a)

            db.execute(select_self_danmu)
            tmp2 = db.fetchall()
            if tmp2:
                for item in tmp2:
                    a = (rid, item['txt'], 2, 0)
                    danmu_data.append(a)

            db.execute(select_true_danmu)
            tmp3 = db.fetchall()
            if tmp3:
                for item in tmp3:
                    a = (rid, item['txt'], 1, 0)
                    danmu_data.append(a)

            db.execute(delete_history)
            myconn.commit()
            db.executemany(insert_danmu, danmu_data)
            myconn.commit()
            db.close()
            myconn.close()
        except:
            print "insert into pradata error"
            print insert_danmu,danmu_data






# if __name__ =="__main__":
#     cli=Danmucp()
#     cli.start(822010)
#     cli.cmdloop()
#     # cli.getmessage(822010)


