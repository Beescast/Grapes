# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
import re

'''过滤关键字'''
stopwords = {}.fromkeys(['的', '包括', '等', '是',])
room_type={}
uid=[]
filter_words = [
    '[0-9a-zA-Z\.]{6,13}','微信', '威信','葳','溦','蓶','崴','v','V','weixin','wx','WX', '性爱', 'q','Q','3p',
    'jj','JJ','jb','JB','Jb','jB','艹','点播', '大片', '黄网','sb','SB','Sb','sB',"傻逼","傻B",'2B','2b',
    'av','AV','Av','aV','感谢','豆瓣','草粉',
    '直播','主播','小影片','小电影','房管', '超管','巨乳','办卡','鱼丸','鱼翅','福利','房间\d+','房间号','机器人',
    "蒙汗药", "迷奸", "催情药", "麻醉枪", "阴茎","阳具", "阴蒂", "肉棍", "肉棒", "肉洞", "荡妇", "阴囊",
    "睾丸", "阴户", "龟头", "你妈逼", '鸡巴',"插B", "操B", "狂插", "狂操", "狂搞", "裸聊", "操你",'激情',
    "色情", "催情药","蒙汗药", "迷奸", "透视", "偷拍", '看片',
    "颜射","狂插","狂操","狂搞","裸聊","操你","肉棍","淫靡","淫水",'赌钱','咪咪',
    ]

danmu_back = ['666','6666','66666','666666','2333333','111111111','233333333','扎心了，老铁','老铁，扎心了','瓜皮',
              '哈哈哈哈','全体起立','戳一下','辣鸡']

regexp = [re.compile(word) for word in filter_words]
reg1=re.compile(r"[\-\.\!\?\/_$%=,\^\*\(\)\+\"\']+".decode('utf-8'))
reg2 = re.compile(r'[！，。？、~@#￥%……&*（）]+'.decode('utf-8'))
reg3 = re.compile(r'\[emot:dy\d+\]'.decode('utf-8'))