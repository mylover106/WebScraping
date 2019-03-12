#!/usr/bin/env python
# coding: utf-8

import sys
import getopt
import time
import re
import random
from urllib.request import urlretrieve, urlopen
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from sendmail import SendEmail


def build_post_data(html):
    post_dict = {"__EVENTTARGET":"",
             "__EVENTARGUMENT":"",
             "__LASTFOCUS":"",
             "drxiaoqu":"",
             "drlou":"",
             "dxbtnQuery":"",
             "DXScript":"1_42,1_74,2_22,2_29,1_46,1_54,2_21,1_67,1_64,2_16,2_15,1_52,1_65,3_7"}
    lst = html.findAll("input")
    for key in lst:
        try:
            # print(key["value"])
            post_dict[key["name"]] = key["value"]
        except:
            # print(None)
            post_dict[key["name"]] = ""
    # fill up the dxdateStart$DDD$C and dxdateEnd_$DDD$C
    post_dict["dxdateStart$DDD$C"] = formatDate(post_dict["dxdateStart"])
    post_dict["dxdateEnd$DDD$C"] = formatDate(post_dict["dxdateEnd"])
    return post_dict


def formatDate(Str):
    lst = re.split(r'[年|月|日]', Str)
    Str = lst[1] + '/' + lst[2] + '/' + lst[0]
    return Str + ':' + Str


def getNameVal(html):
    lst = html.findAll("option")
    name2value = {"校区":dict(), "楼名":dict()}
    for x in lst:
        if x.text == "校区":
            name = "校区"
            continue
        if x.text == "楼名":
            name = "楼名"
            continue
        name2value[name][x.text] = x["value"]
    return name2value


def ElecRoomQuery(xiaoqu, louming=None, roomid=None):
    if roomid is not None:
        if len(roomid) < 4:
            roomid = '0' + roomid
        if len(roomid) > 4:
            roomid = roomid[-4:]
    
    url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
    html = requests.get(url).text
    html = BeautifulSoup(html, 'html.parser')
    name2val = getNameVal(html)
    dct = build_post_data(html)
    dct['__EVENTARGUMENT'] = 'drxiaoqu'
    dct['drxiaoqu'] = name2val['校区'][xiaoqu]


    newhtml = requests.post(url, dct).text
    newhtml = BeautifulSoup(newhtml, 'html.parser')


    dct = build_post_data(newhtml)

    name2val = getNameVal(newhtml)
    if roomid is None:
        return name2val

    dct['drxiaoqu'] = name2val['校区'][xiaoqu]
    dct['drlou'] = name2val['楼名'][louming]
    dct['txtRoomid'] = roomid


    finalhtml = requests.post(url, dct)
    finalhtml = BeautifulSoup(finalhtml.text, 'html.parser')
    # print(finalhtml)
    left_money = finalhtml.findAll('td', {"class":"dxgv", "align":"center", "style":"border-right-width:0px;"})[0].text
    return float(left_money)


if __name__ == "__main__":
    while True:
        xiaoqu = "曾厝安学生公寓"
        louming = "7号楼"
        roomid = "519"
        try:
            left = ElecRoomQuery(xiaoqu, louming, roomid)
        except:
            SendEmail('1066616102@qq.com', From="电费检查器", To="Myself", Subject="电费查询失败", Message="电费查询失败，请检查输入！")
            continue
        # print(xiaoqu + louming + roomid + "电费剩余" + str(left) + "元str。")
        if left < 5:
            Str = xiaoqu + louming + roomid + "电费剩余" + str(left) + "元。" + "请尽快充值！"
            SendEmail('1066616102@qq.com', From="电费检查器", To="Myself", Subject="电费查询成功", Message=Str)
        days = 24 * 60 * 60
        time.sleep(days)
    # print(left_money)



