# encoding=utf-8

import sys
import getopt
import time
import re
import random
from urllib.request import urlretrieve, urlopen
import requests
from bs4 import BeautifulSoup
from PIL import Image
import matplotlib.pyplot as plt



if __name__ == "__main__":
    # get options
    opts, args = getopt.getopt(sys.argv[1:], "e:p:")
    for opt in opts:
        if "-e" in opt:
            email = opt[1]
        if "-p" in opt:
            passwd = opt[1]

    # get captcha and captcha's id
    try:
        url = "https://www.douban.com"
        html = urlopen(url)
        html = BeautifulSoup(html, "html5lib")
        html = html.find("img", {"id": "captcha_image"})

        link = html['src']
        urlretrieve(link, "./pic/captcha")
        img = Image.open("./pic/captcha")
        img.show()

        index_start = link.find('id=') + 3
        index_end = link.find('&')
        captcha_id = link[index_start:index_end]

        # input the captcha
        captcha_num = input()

        # pack the data
        data = {
            "source": "index_nav",
            "form_email": email,
            "form_password": passwd,
            "captcha-solution": captcha_num,
            "captcha-id": captcha_id
        }
    except Exception as e:
        data = {
            "source": "index_nav",
            "form_email": email,
            "form_password": passwd,
            # "captcha-solution": captcha_num,
            # "captcha-id": captcha_id
        }

    # post the request

    url = "https://accounts.douban.com/login"

    response = requests.post(url, data)
    print(response)
    response = BeautifulSoup(response.text, "html5lib")
    response = response.findAll("img")
    print(response[0].attrs)
    response = [r.attrs['src'] for r in response if "src" in r.attrs and re.match('[^"]+\.(png|jpg)', r.attrs['src'])]
    name = 0
    for link in response:
        urlretrieve(link, "./pic/" + str(name))
        name += 1
        print(str(name) + " saved")
    # print(response.text)

