# -*- coding: utf-8 -*-
import random
import MySQLdb
import MySQLdb.cursors
from danmu import DanMuClient
import datetime
'''
conn=MySQLdb.connect(
     host='192.168.3.56',
     port=3306,
     db='grapes',
     user='repl',
     charset='utf8',
     passwd='0831@Bees',
     cursorclass=MySQLdb.cursors.DictCursor)
cursor = conn.cursor()
the_sql="""SELECT tag,LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '0','')) as zero,
  LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '1','')) as one,
LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '2','')) as two,
  LENGTH (a.bstr) - LENGTH (REPLACE(a.bstr, '3','')) as three
  from
 (select
  tag, group_concat(bat_type) as bstr from  original_acc where tag='%s'
 group by tag) a"""%244548
cursor.execute(the_sql)
data=cursor.fetchone()
msg={"0":int(data['zero']),
"1":int(data['zero']),
"2":int(data['zero']),
"3":int(data['zero'])
     }

print msg
for key,value in msg.items():
     print key,value'''
# for j in  cursor.fetchall():
#      for s in  j[0].split(','):
#           if s not in a:
#                a.append(s)
# print ','.join(a)

# cursor.executemany("insert into pradata (rid,txt,type,flag) values(%s,%s,%s,%s)", [(u'506510', u'\u6012\u9001\u4e00\u8840\uff0c\u7ed9\u5927\u5bb6\u6765\u4e2a\u60ca\u559c', 1, 0), (u'506510', u'\u8d3c\u559c\u6b22\u6d9b\u5f1f\u7684\u89e3\u8bf4', 1, 0), (u'506510', u'\u559c\u6b22\u6d9b\u54e5\u7ed9\u6211\u53e3', 1, 0), (u'506510', u'\u5783\u573e\u91d1\u91d1\u5462\uff1f\u643a\u5de8\u6b3e\u8dd1\u8def\u4e86', 1, 0)])
# cursor.execute("insert into pradata (rid,txt,type,flag) values('506510', '\u6012\u9001\u4e00\u8840\uff0c\u7ed9\u5927\u5bb6\u6765\u4e2a\u60ca\u559c', 1, 0)")

# select_back_danmu="select distinct txt from danmu_bac_data where rid='%s' ORDER by rand() limit %s"%(244548,60)
# cursor.execute(select_back_danmu)
# print len(cursor.fetchall())
# for row in cursor.fetchall():
#      print row[0]





# insert_data="insert into pradata (rid,txt,type) values(%s,%s,%s)"
# data=[(u'430489', u'\u6709\u7684\u5149\u7f06\u4e5f\u8d70\u4e0b\u6c34\u9053', 1), (u'430489', u'\u83ab\u4e71\u6392\u6c34\uff0c\u6392\u5230\u7535\u7f06\u7ba1\u9053\u4f60\u5c31GG\u4e86', 1), (u'430489', u'\u62bd\u5230\u7535\u7f06\u4e95\u91cc', 1), (u'430489', u'\u5148\u770b\u770b \u5858\u91cc\u6709\u8d27\u5192', 1), (u'430489', u'\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27', 0), (u'430489', u'\u69a8\u83dc\u662f\u8001\u4e8c\u7684\u724c', 0), (u'430489', u'\u5148\u4e0b\u4e1d\u7f51\u641e\u641e', 0), (u'430489', u'\u6709\u8d27\u5c31\u641e \u5192\u5f97\u641e\u8d77\u6765\u4e5f\u5192\u5f97\u610f\u601d\u554a', 0), (u'430489', u'\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27\u770b\u8d27', 0), (u'430489', u'\u8def\u4e0a\u4e0b\u6c34\u9053\u53ef\u4ee5', 0), (u'430489', u'\u5148\u4e0b\u7f51\u770b\u770b\u6709\u6ca1\u6709\u8d27', 0), (u'430489', u'\u5c31\u8fd9\u4e48\u5b9a\u4e86\uff0c\u4ece\u4e0b\u6c34\u9053\u6392', 0), (u'430489', u'\u69a8\u83dc', 0), (u'430489', u'\u8def\u4e0a\u4e0b\u6c34\u7ba1\u9053', 0), (u'430489', u'\u90a3\u662f\u4e0b\u6c34\u7ba1', 0), (u'430489', u'\u90a3\u660e\u660e\u662f\u96e8\u6c34\u4e95\uff0c\u7535\u7f06\u4e95\u4f60\u80fd\u6253\u5f00\u7b11\u8bdd', 0), (u'430489', u'\u8def\u8fb9\u4e0b\u6c34\u7ba1\u9053', 0), (u'430489', u'\u6536\u5de5', 0), (u'430489', u'\u5feb\u70b9\u554a\u51e0\u70b9\u5b8c\u4e8b\u554a\uff01', 0), (u'430489', u'\u8bf7\u95ee\u8fd9\u662f\u5927\u578b\u6237\u5916\u770b\u5858\u8282\u76ee\u5417\uff1f', 0)]
# db.executemany(insert_data,data)

# test_sql="""insert  into chatdata(rid,txt,dteventtime) values("430489","我的天","2017-04-13 10:34:46")"""
# test_sql="select * from danmu_bac_data"
# db.execute(test_sql)
# print db.execute(test_sql)ta_cookie
# inser="insert into chatdata(rid,txt,dteventtime) values('61372','596个会员了，赶紧来4个兄弟上车，让郭技师给你们口一哈','2017-04-14 17:28:59.367000')"
# cursor.execute(inser)
# conn.commit()
#
#
# conn.commit()

# for item in random.sample(tmp4, 60):
#      print item['txt']

#
# dmc = DanMuClient('https://www.douyu.com/280072')
# @dmc.danmu
# def danmu_fn(msg):  # 填充实时消息
#      print msg['Content']
#      # insert_data = "insert into chatdata(rid,txt,dteventtime) values('%s','%s','%s')" % (
#      #      msg['rid'], msg['Content'], datetime.datetime.now())
#      # print insert_data
#      # cursor.execute(insert_data)
#      # conn.commit()
# dmc.start(blockThread=True)

#
# import cStringIO
# import StringIO
# import time
#
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#
# s = cStringIO.StringIO()
# dmc = DanMuClient('http://www.douyu.com/%s'%244548)
# a=0
# @dmc.danmu
# def danmu_fn(msg):  # 填充实时消息
#      data =u"%s|%s|%s\n" %(msg['rid'],msg['Content'],datetime.datetime.now())
#      s.write(data)


#
# def danmu_m1()
#      if keys:
class T():
    l = []
    def get(self):
        print self.l
    @classmethod
    def set(cls,i):
        cls.l.append(i)
    @staticmethod
    def get():
        return T.l

t = T()
t.set(1)
t.get()
print T.l
print t.get()




