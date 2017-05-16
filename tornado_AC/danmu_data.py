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


conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)



class wordcut():
    timestep = 20  #消息提取间隔时间
    topk=30  #选择关键词数量

    @staticmethod
    def data_get(rid):
        conn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
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
    dmc_data={} #保存房间信息
    @classmethod
    def start(cls,rid):
        dmc = DanMuClient('http://www.douyu.com/%s'%rid)
        cls.dmc_instance[rid]=dmc
        cls.dmc_data[rid]=cStringIO.StringIO()
        @dmc.danmu
        def danmu_fn(msg): #填充实时消息
            try:
                if str(msg['uid']) not in uid:
                    data= cls.msg_handle(msg['Content'])
                    if data:
                        # cursor = conn.cursor()
                        # insert_data = "insert into chatdata(rid,txt,dteventtime) values('%s','%s','%s')" % (
                        #     msg['rid'], msg['Content'], datetime.datetime.now())
                        # cursor.execute(insert_data)
                        # conn.commit()
                        data=msg['rid'], msg['Content'], datetime.datetime.now()
                        cls.dmc_data[rid].write()
            except:
                pass
        dmc.start(blockThread=False)

    @classmethod
    def getmessage(cls,rid):
        myconn = MySQLdb.connect(
            host='192.168.3.56',
            port=1234,
            db='grapes',
            user='repl',
            passwd='Bees@0831@',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor)
        db = myconn.cursor()
        cate_id=room_type[rid]  #查询房间类型
        keys = wordcut.getwords(rid) #获取最近弹幕关键字
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        before_now=(datetime.datetime.now() - datetime.timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        one_minute=(datetime.datetime.now() - datetime.timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        #更新前删除原来弹幕内容
        delete_history="delete from pradata where rid='%s'"%rid

        # 跟据关键字查询备用词库消息
        select_back_danmu_v1="select distinct txt from danmu_bac_data where cate_id='%s' and txt REGEXP '%s' ORDER by rand() limit 60" % (cate_id,keys)
        select_back_danmu_v2 = "select distinct txt from danmu_bac_data where rid='%s' and txt REGEXP '%s' ORDER by rand() limit 60" % (rid, keys)

        #查询实时弹幕消息
        select_true_danmu_v1="select distinct txt from chatdata where rid='%s' and substr(dteventtime,1,10)='%s' and dteventtime <'%s' and txt REGEXP '%s' ORDER by rand() limit 60 "%(rid,today,before_now,keys)
        select_true_danmu_v2="select distinct txt from chatdata where rid='%s' and dteventtime>='%s' and txt REGEXP '%s'" % (rid, before_now, keys)
        select_true_danmu_v3 = "select distinct txt from chatdata where rid='%s' and dteventtime>='%s' and txt not REGEXP '%s' " % (rid,one_minute,keys)

        #查询人工编写弹幕表
        select_self_danmu_v1 = "select distinct txt from self_danmu ORDER by rand() limit 60 "

        #保存消息
        insert_danmu="insert into pradata (rid,txt,type,flag) values(%s,%s,%s,%s)"
        danmu_data=[]

        if keys:
            db.execute(select_true_danmu_v2)
            tmp1 = db.fetchall()
            if tmp1:
                for item in tmp1:
                    a = (rid, item['txt'], 0,0)
                    danmu_data.append(a)
               # print "本房间30秒内",len(danmu_data)

            db.execute(select_true_danmu_v3)
            tmp2 = db.fetchall()
            if tmp2:
                for item in tmp2:
                    a = (rid, item['txt'], 0,0)
                    danmu_data.append(a)
               # print "本房间一分钟内弹幕", len(danmu_data)

            if len(danmu_data)<80:
                if int(cate_id) not in [201]:
                    db.execute(select_back_danmu_v2)
                    tmp3 = db.fetchall()
                    if tmp3:
                        for item in tmp3:
                            a = (rid, item['txt'], 1,0)
                            danmu_data.append(a)
                        #print "备用弹幕，非颜值区,随机提取60", len(danmu_data)

                else:
                    db.execute(select_back_danmu_v1)
                    tmp4 = db.fetchall()
                    if tmp4:
                        for item in tmp4:
                            a = (rid, item['txt'], 1,0)
                            danmu_data.append(a)
                       # print "备用弹幕，颜值区，随机60", len(danmu_data)
            if len(danmu_data)<120:
                db.execute(select_true_danmu_v1)
                tmp31 = db.fetchall()
                if tmp31:
                    for item in tmp31:
                        a = (rid, item['txt'], 1, 0)
                        danmu_data.append(a)
                        # print "本房间一天内弹幕，随机提取60", len(danmu_data)

        else:
            db.execute(select_self_danmu_v1)
            tmp5 = db.fetchall()
            for item in tmp5:
                a = (rid, item['txt'], 1,0)
                danmu_data.append(a)
           # print "自编弹幕", len(danmu_data)
        try:
            db.execute(delete_history)
            myconn.commit()
            db.executemany(insert_danmu, danmu_data)
            myconn.commit()
            db.close()
            myconn.close()
        except:
            pass



    @staticmethod
    def msg_handle(msg):
        msg = re.sub("[a-zA-Z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),msg)
        for words in filter_words:
            if re.search(words,msg):
                msg=None
        return msg





# if __name__ =="__main__":
#     cli=Danmucp()
#     cli.start(822010)
#     cli.cmdloop()
#     # cli.getmessage(822010)


