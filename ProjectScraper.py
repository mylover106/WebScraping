# coding: utf-8


from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import random
import time
# import gensim
import numpy as np
import threading
import getopt
import sys


def scraper(words, fp):
    url = "http://corpus.zhonghuayuwen.org/CnCindex.aspx"
    length = len(words)
    for i, word in enumerate(words):
        data[word_key] = word
        while True:
            try:
                obj = requests.post(url, data)
                break
            except:
                time.sleep(0.7)
                print("trying          ", end='\r', flush=True)

        html = BeautifulSoup(obj.text, "html5lib")
        
        seq = html.find("div", {"class": re.compile("PNL\d")})
        try:
            seq = seq.find('font')
        except:
            print(word, end='\r', flush=True)
            continue
        fp.write(seq.text+'\n')
        print_meg = str(i) + '/' + str(length)

        print(print_meg, end='\r', flush=True)
        time.sleep(0.3)


if __name__ == "__main__":
    sep = 611536
    # load word2vec and get all the words
    # model_path = '../../GAN/word2vec.bin'
    # word_model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    print("loading finished")

    # get all the words
    # all_words = word_model.index2word
    all_words = np.load('wordvec.npy')
    # del word_model

    # build the scraper
    data = {
        "__VIEWSTATE": "/wEPDwUKLTQzNTczMjk0OGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgoFC1JCaW5kZXh3b3JkBQpSQmxpa2Vtb2RlBQpSQmxpa2Vtb2RlBQ5SQmZ1bGx0ZXh0bW9kZQUOUkJmdWxsdGV4dG1vZGUFDFJhZGlvQnV0dG9uMwUMUmFkaW9CdXR0b240BQxSYWRpb0J1dHRvbjQFDkNoZWNrQm94Q2h1Y2h1BRBDaGVja0JveEtXSUNtb2RliXMUgmdY+pySZotCIj8F0JS3PFzBmKGs9H+YCzdZF2Y=",
        "__VIEWSTATEGENERATOR": "3A0BE18D",
        "__EVENTVALIDATION": "/wEWDgKk5vuzCgLYiuv/CwLzuO7zDQL3uO7zDQLV+YmkCgLZ+YmkCgKM54rGBgK8u9naBwKJlM7DBwKAg8rcDgKWzvT1CAKWzuCuBwK2q5qHDgK/xfDTARYHJhVKxYBZXPemmOCC2HnYCjQGuded4R0NuAi/8QLO",
        "TextBoxCCkeywords": "的",
        "DropDownListPsize": 10,
        "Button1": "检  索",
        1: "RBlikemode",
        2: "RadioButton3",
        "CheckBoxChuchu": "on"
    }

    word_key = 'TextBoxCCkeywords'

    opts, args = getopt.getopt(sys.argv[1:], "n:", ["ith="])
    for opt in opts:
        if "-n" in opt:
            i = int(opt[1])

    print("start scraper")
    with open('word_data' + str(i) + '.txt', 'w') as fp:
        scraper(all_words[(i-1)*sep:i*sep], fp)

    print("finished")


    