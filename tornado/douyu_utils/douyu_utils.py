#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import sys
import time
import re
import requests
from urllib import unquote

reload(sys)
sys.setdefaultencoding('utf-8')


def douyu_get_room_info(rid):

    header = {
    'Host': "www.douyu.com",
    'Referer': "http://www.douyu.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }

    ret = []

    search_url = 'http://open.douyucdn.cn/api/RoomApi/room/%d' % (rid)

    try:
        r = requests.get(search_url, headers=header)
    except:
        print "", __file__, sys._getframe().f_lineno
        return ret

    response = r.text
    room = json.loads(response)

    if(room['error'] == 0):
        data = room['data']

        if data['room_status'] == '1':
            reachable = 1
        else:
            reachable = 0

        ret = {"ad_reachable": reachable,
               "ad_owner_unique_id": data['room_id'],
               'ad_href_url'   : "http://www.douyu.com/%s" % data['room_id'],
               "ad_imag_uri": data['room_thumb'],
               "ad_title": data['room_name'],
               "online_num": data['online']
               }

    return ret


def douyu_live_online_cmp(x, y):
    if(x['online'] > y['online']):
        return 1
    elif (x['online'] < y['online']):
        return -1
    else:
        return 0


def  douyu_get_dir_max_online_room(dirs):
    header = {
    'Host': "www.douyu.com",
    'Referer': "http://www.douyu.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }

    ret = []

    search_url = "http://open.douyucdn.cn/api/RoomApi/live/%s?limit=5" % (dirs)

    try:
        r = requests.get(search_url, headers=header)
    except:
        print "", __file__, sys._getframe().f_lineno
        return ret

    response = r.text
    live = json.loads(response)

    if(live['error'] == 0):
        data = live['data']
        data.sort(douyu_live_online_cmp, reverse = True)

        if len(data) > 0:
            each = data[0]
            ret = {
                    'ad_reachable'  : 1,
                    'ad_owner_unique_id' : each['room_id'],
                    'ad_href_url'   : "http://www.douyu.com/%s" % each['room_id'],
                    'ad_imag_uri'   : each['room_src'],
                    'ad_title'      : each['room_name'],
                    'online_num'    : each['online'],
                    'anchor_uid'    : each['owner_uid'],
                    'anchor_nn'     : each['nickname'],
                    'game_name'     : each['game_name'],
                    'short_name'    : dirs
                    }
    return ret

def  douyu_get_dir_all_room(dir, offset):
    header = {
    'Host': "www.douyu.com",
    'Referer': "http://www.douyu.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }

    ret = []

    search_url = "http://open.douyucdn.cn/api/RoomApi/live/%s?limit=100&offset=%d" % (dir, offset)

    try:
        r = requests.get(search_url)
    except:
        print "", __file__, sys._getframe().f_lineno
        return ret

    response = r.text
    live = json.loads(response)

    if(live['error'] == 0):
        data = live['data']

        for each in data:
            tmp = {
                    'ad_reachable'  : 1,
                    'ad_owner_unique_id' : each['room_id'],
                    'ad_href_url'   : "http://www.douyu.com/%s" % each['room_id'],
                    'ad_imag_uri'   : each['room_src'],
                    'ad_title'      : each['room_name'],
                    'online_num'    : each['online'],
                    'anchor_uid'    : each['owner_uid'],
                    'anchor_nn'     : each['nickname'],
                    'game_name'     : each['game_name'],
                    'short_name'    : dir
                    }
            ret.append(tmp)

    return ret


def  douyu_get_danmu_auth_server(rid):
    header = {
    'Host': "www.douyu.com",
    'Referer': "http://www.douyu.com/",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }

    ret = []
    search_url = 'http://www.douyu.com/%d' % (rid)

    try:
        r = requests.get(search_url, headers=header)
    except:
        print "", __file__, sys._getframe().f_lineno
        return ret

    auth_server_json = re.search('\$ROOM\.args\s=\s({.*});', r.text).group(1)

    try :
        server_json = json.loads(auth_server_json)['server_config']
        ret = json.loads(unquote(server_json))
    except:
        print "", __file__, sys._getframe().f_lineno
        return ret

    return ret
