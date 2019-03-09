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


url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
html = requests.get(url).text
html = BeautifulSoup(html)
dct = build_post_data(html)
dct['__EVENTARGUMENT'] = 'drxiaoqu'
dct['drxiaoqu'] = '09'


newhtml = requests.post(url, dct).text
newhtml = BeautifulSoup(newhtml)


dct = build_post_data(newhtml)


dct['drxiaoqu'] = '09'
dct['drlou'] = '7号楼'
dct['txtRoomid'] = '0519'


finalhtml = requests.post(url, dct)
finalhtml = BeautifulSoup(finalhtml.text)
left_money = finalhtml.find('tr', {"id":"dxgvSubInfo_DXDataRow1"}).find("td", {"style":"border-right-width:0px;border-bottom-width:0px;"}).text

print(left_money)



