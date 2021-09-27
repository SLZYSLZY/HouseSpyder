# -*- coding: utf-8 -*-
"""
@Time    : 2021/9/26 14:57
@Author  : WangFeng
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

def get_suburl(base_url):
    html = requests.get(base_url).text
    sp = BeautifulSoup(html, "lxml")
    item_list = sp.body.find_all(class_='position')[0].contents

    list2 = []
    for item in item_list[3].contents[3].div.contents[3].contents:
        if item != '\n':
            list2.append(item)

    list3 = []
    for item in list2:
        if item.name == 'a':
            list3.append(item)

    sub_list = []
    for item in list3:
        time.sleep(2)
        html = requests.get('https://su.lianjia.com' + item['href']).text
        sp = BeautifulSoup(html, "lxml")
        total_page = json.loads(sp.body.find_all(class_='page-box house-lst-page-box')[0]['page-data'])['totalPage']

        sub_list.append(('https://su.lianjia.com' + item['href'], item.text, total_page))

    print(sub_list)
    return sub_list

# get_suburl('https://su.lianjia.com/chengjiao/gongyeyuan/')
