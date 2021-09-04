# -*- coding: utf-8 -*-
"""
@Time    : 2021/8/31 17:17
@Author  : WangFeng
"""
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random


# 要爬取的数据：
# 基础属性
HouseBasicDataId = []
HouseBasicDataSquare = []
HouseBasicDataLivingRoom = []
HouseBasicDataBedroom = []
HouseBasicDataKitchen = []
HouseBasicDataBathroom = []
# 总楼层
HouseBasicDataTotalFloor = []
HouseBasicDataFloor = []
# 建筑结构
HouseBasicDataBuildingStructure = []
# 建成年代
HouseBasicDataBuiltYear = []
# 装修情况
HouseBasicDataRenovationCondition = []
# 建筑类型
HouseBasicDataBuildingType = []
# 户型结构
HouseBasicDataHouseStructure = []
# 梯户比
HouseBasicDataStairsHouseRatio = []
HouseBasicDataHasElevator = []
HouseBasicDataSecondaryDistrict = []
HouseBasicDataPrimaryDistrict = []
HouseBasicDataOrientation = []

# 交易属性
# 小区均价
HouseTradeDataCommunityAveragePrice = []
# 成交时间
HouseTradeDataTradeTime = []
# 挂牌时间
HouseTradeDataDaysOnMarket = []
# 关注人数
HouseTradeDataFollower = []
# 是否满五年
HouseTradeDataAgeProperty = []
# 挂牌价
HouseTradeDataListPrise = []
# 成交价
HouseTradeTransactionPrice = []



base_url = 'https://su.lianjia.com/chengjiao/'
page_url = []
page_url.append(base_url)
for i in range(2, 101):
    page_url.append(base_url + 'pg' + str(i))


def get_primary_data(primary_page_url):
    html = requests.get(primary_page_url).text
    BeautifulSoup(html, "lxml")
    sp = BeautifulSoup(html, "lxml")
    item_list = sp.body.find_all(class_='listContent')[0].contents
    for j in range(0, len(item_list)):
        title = item_list[j].div.find_all(class_='title')[0].a.text
        house_name = title.split(' ')[0]
        house_struct = title.split(' ')[1]
        house_square = title.split(' ')[2]

        detail_page_url = item_list[j].div.find_all(class_='title')[0].a['href']
        # todo get_detail_data()


    sp.body.find_all(class_='listContent')[0].contents[0].div.find_all(class_='title')[0].a['href']



'https://su.lianjia.com/chengjiao/107104076340.html'


sp.body.find_all(class_='listContent')[0].contents[0].div.find_all(class_='title')[0].a.text
'香堤澜湾 2室2厅 76.11平米'


class HouseSpider():
    def __init__(self):
        # 通过fake_useragent库，随机切换UserAgent,简单伪装爬虫
        self.headers = {'User-Agent': UserAgent().random}

    def all_page_url(self, url):
        for i in range(1, 24):  # 一共24页数据
            page_url = url + str(i) + "/"  # 生成了24页的url地址
            self.one_page(page_url)
        print("Done")

    def request(self, page_url):
        # 使用get方式发送请求
        html = requests.get(page_url, headers=self.headers)
        time.sleep(random.randint(1, 4))  # 随机时间休眠
        html.encoding = "GBK"  # 解决中文乱码问题
        return html

    def one_page(self, page_url):
        page_html = self.request(page_url)
        sp = BeautifulSoup(page_html.text, "lxml")  # 使用lxml解析方式
        first = sp.find_all(class_='nlcd_name')  # 抓取class属性为=“nlcd_name”对应的内容

        # 抓取楼盘名称
        for name in first:  # 依次取出first里面的每一条内容
            name1 = name.find_all("a")  # 查找first中a标签的内容
            for name2 in name1:
                a_name.append(name2.get_text().strip())  # 通过get_text()获取name2的内容，并添加到a_name列表里面。
        print(len(a_name))  # 打印出每一次循环以后a_name列表的长度，每一次循环对应一页的内容，该长度代表每一页抓取到的数量

        # 抓取楼盘所处区域
        Address = sp.find_all(class_="address")
        for address in Address:
            for address1 in address.select("a"):  # 通过select选择器选择address里面的a标签。
                b_address.append(address1.text.strip()[0:5].strip())
        print(len(b_address))

        # 抓取楼盘价格
        Price = sp.find_all(class_="nhouse_price")  # 找到所有的Price，以列表形式保存
        for price in Price:
            # 这里select的是有明确价格与价格待定的
            for price1 in price.select("span"):
                c_price.append(price1.get_text())
            # 这里select的是价格待定、往期的
            for price2 in price.select('div > div.nlc_details > div.nhouse_price > label:nth-of-type(1)'):
                c_price.append(price2.get_text())
                # 这里select的是新房已卖出的
        for price3 in sp.select(' div > div.nlc_details > div.kanesf > p > a'):
            c_price.append(price3.get_text())
        print(len(c_price))

        # 开始抓取楼盘对应评论数量的循环，循环注释与前面类似
        value_num = sp.find_all(class_="house_value clearfix")
        for j in value_num:
            value_num2 = j.find(class_="value_num")
            if value_num2:
                d_comment_value.append(value_num2.get_text()[1:-4])
            else:
                d_comment_value.append('0')
        print(len(d_comment_value))

    # 保存数据到指定路径的csv文件
    def data_save(self):
        data = {"name": a_name, "address": b_address, "price": c_price, "comments": d_comment_value}  # 生成字典
        house = pd.DataFrame(data)  # 创建DataFrame对象
        # encoding='utf_8_sig'为了让保存下来的中文不出现乱码,index=False是不需要索引
        house.to_csv('D:\pachong\pachong_suzhouf.csv', index=False, encoding='utf_8_sig')


suzhou = HouseSpider()
suzhou.all_page_url("https://suzhou.newhouse.fang.com/house/s/b9")
suzhou.data_save()
