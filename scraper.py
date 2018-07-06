from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
import time


def get_links(url):
    url = "http://baike.baidu.com" + url
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html5lib")
    name = bs_obj.find("dd", {"class": "lemmaWgt-lemmaTitle-title"}).h1.get_text()
    print(name)
    print(url)
    print()

    link_source = bs_obj.html.body.find("div", {"class": "body-wrapper"})
    link_source = link_source.find("div", {"class": "content-wrapper"})
    link_source = link_source.find("div", {"class": "content"})
    link_source = link_source.find("div", {"class": "main-content"})
    link_source = link_source.findAll("div", {"class": "para"})
    # print(link_source[0].attrs)
    link_source = [li.a for li in link_source if li.a != None]
    # print(link_source[0].attrs)
    link_source = [li['href'] for li in link_source if 'href' in li.attrs and re.match("^(/item/)", li.attrs['href'])]
    return link_source


if __name__ == "__main__":
    searched_list = ["/item/%E5%AE%8B%E6%B1%9F/7539"]
    Links = get_links("/item/%E5%AE%8B%E6%B1%9F/7539")

    for i in range(100):
        link = random.choice(Links)

        while link in searched_list:
            link = random.choice(Links)
            print("select")

        searched_list.append(link)
        temp_links = get_links(link)
        if bool(temp_links):
            Links = temp_links
        # print(Links)
        time.sleep(0.5)
