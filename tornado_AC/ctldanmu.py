# -*- coding: utf-8 -*-
import threading
import time
from danmu_data_v2 import *
import json
import requests
import ctypes
import inspect
import sys
reload(sys)
sys.setdefaultencoding('utf8')



class CTL(cmd.Cmd):
    the_threads={}

    def __init__(self):
        self.delay=20

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    @classmethod
    def start(cls,rid,room_data):
        info = 0
        if rid in Danmucp.dmc_instance.keys():
            info=1
        else:
            search_url = 'http://open.douyucdn.cn/api/RoomApi/room/%s' % (rid)
            r=None
            try:
                r = requests.get(search_url)
            except:
                pass
            response = r.text
            room = json.loads(response)

            if (room['error'] == 0):
                data = room['data']
                if data['room_status'] == '1':
                    cate_id=data['cate_id']
                    room_type[rid]=cate_id
                    danmucp = room_data[rid]['danmucp']
                    danmucp.start(rid)
                    word_cut = room_data[rid]['word']
                    ctl = room_data[rid]['ctl']
                    t = threading.Thread(target=ctl.danmu_update, args=(rid,danmucp,word_cut))
                    t.start()
                    cls.the_threads[rid]=t.ident
                    info=2
                else:
                    info=3
            else:
                info=4
        return info

    @staticmethod
    def stop(rid):
        try:
            Danmucp.dmc_instance[rid].stop()
            del Danmucp.dmc_instance[rid]
            CTL._async_raise(int(CTL.the_threads[rid]), SystemExit)
        except:
            pass




    def danmu_update(self,rid,danmucp,word_cut):
        while True:
            danmucp.getmessage(rid,word_cut)
            time.sleep(self.delay)

    @staticmethod
    def update(value):
        for keys in value:
            if keys == "delay":
                CTL.delay = value[keys]
            if keys == "size":
                Danmucp.size = value[keys]
            if keys == "topk":
                wordcut.topk = value[keys]
            if keys == "timestep":
                wordcut.timestep = value[keys]

    @staticmethod
    def info():
        print "[delay]     线程刷新时间     %s"%CTL.delay
        print "[topk]      关键字提取数量   %s"%wordcut.topk
        print "[timestep]  弹幕分析时间间隔 %s"%wordcut.timestep
        print "[rooms]     房间信息        %s" %[i for i in Danmucp.dmc_instance.keys()]


    def help_update(self):
        print "------------keywords------------------"
        print "[delay].................线程刷新时间"
        print "[size]..................消息队列大小"
        print "[topk]..................关键字提取数量"
        print "[timestep]..............弹幕分析时间间隔"
        print
        print "----usage:update keyword value--------"


    def do_update(self,line):
        argv = line.split()
        argc = len(argv)
        if argc == 1:
            self.help_update()
        value={argv[0]:argv[1]}
        self.update(value)


    def help_info(self):
        print "values of the keywords"

    def do_info(self,line):
        self.info()

    def help_start(self):
        print "usage:start roomid"


    def do_start(self,line):
        argv = line.split()
        argc = len(argv)
        if argc != 1:
            self.help_start()
        self.start(argv[0])


    def help_stop(self):
        print "usage:cmd roomid"


    def do_stop(self,line):
        argv = line.split()
        argc = len(argv)
        if argc != 1:
            self.help_stop()
        self.stop(argv[0])

#
# if __name__ =="__main__":
#     cli = CTL()
#     cli.cmdloop()

