# -*- coding: utf-8 -*-
"""
@Time    : 2021/8/31 17:17
@Author  : WangFeng
"""
import random
import re
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
HouseTradeDataListPrice = []
# 成交价
HouseTradeTransactionPrice = []

pattern = re.compile(r'[0-9]+')  # 查找数字
base_url = 'https://su.lianjia.com/chengjiao/'
page_url = []
page_url.append(base_url)

zh2num = {
    '零': 0,
    '一': 1,
    '二': 2,
    '两': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
}

for i in range(2, 101):
    page_url.append(base_url + 'pg' + str(i))


def get_primary_data(primary_page_url):
    html = requests.get(primary_page_url).text
    time.sleep(5)
    sp = BeautifulSoup(html, "lxml")
    item_list = sp.body.find_all(class_='listContent')[0].contents
    for j in range(0, len(item_list)):
        # 房屋面积 几室几厅
        title = item_list[j].div.find_all(class_='title')[0].a.text
        if len(title.split(' ')) != 3:
            print('非房子')
            continue
        house_name = title.split(' ')[0]
        house_struct = title.split(' ')[1]
        house_square = title.split(' ')[2]
        print(house_name, house_square, house_struct)

        # 房屋朝向 房屋装修
        info = item_list[j].div.find_all(class_='houseInfo')[0].text
        print(info)
        list_a = info.replace(' ', '').split('|')
        house_orientation = list_a[0]
        house_renovation = list_a[1]
        print(house_orientation, house_renovation)

        # 成交日期
        deal_date = item_list[j].div.find_all(class_='dealDate')[0].text
        HouseTradeDataTradeTime.append(deal_date)
        print(deal_date)

        # 成交价
        total_price = item_list[j].div.find_all(class_='totalPrice')[0].text.replace('万', '')
        HouseTradeTransactionPrice.append(total_price)
        print(total_price)

        # 挂牌价 成交周期
        deal_info = item_list[j].div.find_all(class_='dealCycleTxt')[0].text
        # print(deal_info)
        result = pattern.findall(deal_info)
        list_price = result[0]
        trade_cycle = result[1]
        HouseTradeDataListPrice.append(list_price)
        print(list_price, trade_cycle)

        detail_page_url = item_list[j].div.find_all(class_='title')[0].a['href']
        get_detail_data(detail_page_url)
        # todo get_detail_data()


def get_detail_data(detail_page_url):
    time.sleep(2)
    html_1 = requests.get(detail_page_url).text
    sp = BeautifulSoup(html_1, "lxml")
    location_info = sp.body.find_all(class_='deal-bread')[0].text.split('>')
    primary_district = re.findall(r'(\w+)二手房成交', location_info[2])[0]
    secondary_district = re.findall(r'(.+)二手房成交', location_info[3])[0]
    HouseBasicDataPrimaryDistrict.append(primary_district)
    HouseBasicDataSecondaryDistrict.append(secondary_district)
    print(primary_district, secondary_district)
    house_follow = sp.body.find_all(class_='msg')[0].contents[4].label.text
    HouseTradeDataFollower.append(house_follow)
    print(house_follow)
    base_info_contents = sp.body.find_all(class_='content')[0].ul.contents
    for item in base_info_contents:
        base_info_label = item.span.text
        base_info_value = item.text.replace(' ', '').replace(base_info_label, '')
        print(base_info_label, ':', base_info_value)
        if base_info_label == '房屋户型':
            re_res = re.findall(r'[0-9]室', base_info_value)
            if len(re_res) != 0:
                bedroom_num = re_res[0][0]
            else:
                bedroom_num = None
            HouseBasicDataBedroom.append(bedroom_num)

            re_res = re.findall(r'[0-9]厅', base_info_value)
            if len(re_res) != 0:
                livingroom_num = re_res[0][0]

            else:
                livingroom_num = None
            HouseBasicDataLivingRoom.append(livingroom_num)

            re_res = re.findall(r'[0-9]厨', base_info_value)
            if len(re_res) != 0:
                kitchen_num = re_res[0][0]
            else:
                kitchen_num = None
            HouseBasicDataKitchen.append(kitchen_num)

            re_res = re.findall(r'[0-9]卫', base_info_value)
            if len(re_res) != 0:
                bathroom_num = re_res[0][0]
            else:
                bathroom_num = None
            HouseBasicDataBathroom.append(bathroom_num)

            print(bedroom_num, livingroom_num, kitchen_num, bathroom_num)

        if base_info_label == '所在楼层':
            floor = re.findall(r'(.+)\(共', base_info_value)[0]
            total_floor = re.findall(r'共([0-9]+)层', base_info_value)[0]
            HouseBasicDataTotalFloor.append(total_floor)
            HouseBasicDataFloor.append(floor)
            print(floor, total_floor)

        if base_info_label == '建筑面积':
            square = re.findall(r'([0-9]+(\.[0-9]+)?)㎡', base_info_value)[0][0]
            HouseBasicDataSquare.append(square)
            print(square)

        if base_info_label == '户型结构':
            house_struct = base_info_value
            HouseBasicDataHouseStructure.append(house_struct)
            print(house_struct)

        if base_info_label == '建筑类型':
            building_type = base_info_value
            HouseBasicDataBuildingType.append(building_type)
            print(building_type)

        if base_info_label == '房屋朝向':
            face = base_info_value
            HouseBasicDataOrientation.append(face)
            print(face)

        if base_info_label == '建成年代':
            built_age = base_info_value
            HouseBasicDataBuiltYear.append(built_age)
            print(built_age)

        if base_info_label == '装修情况':
            condition = base_info_value
            HouseBasicDataRenovationCondition.append(condition)
            print(condition)

        if base_info_label == '建筑结构':
            building_struct = base_info_value
            HouseBasicDataBuildingStructure.append(building_struct)
            print(building_struct)

        if base_info_label == '梯户比例':
            a = zh2num[re.findall(r'([\w]+)梯', base_info_value)[0]]
            b = zh2num[re.findall(r'(梯[\w]+)户', base_info_value)[0]]
            if b == 0:
                ratio = None
            else:
                ratio = a / b
            print(ratio)
            HouseBasicDataStairsHouseRatio.append(ratio)

        if base_info_label == '配备电梯':
            has_elv = base_info_value
            HouseBasicDataHasElevator.append(has_elv)
            print(has_elv)

    trade_info_contents = sp.body.find_all(class_='content')[1].ul.contents
    for item in trade_info_contents:
        base_info_label = item.span.text
        base_info_value = item.text.replace(' ', '').replace(base_info_label, '')
        print(base_info_label, ':', base_info_value)
        if base_info_label == '链家编号':
            id = base_info_value
            HouseBasicDataId.append(id)
            print(id)
        if base_info_label == '房屋年限':
            age = base_info_value
            HouseTradeDataAgeProperty.append(age)
            print(age)
        if base_info_label == '挂牌时间':
            HouseTradeDataDaysOnMarket.append(base_info_value)


for index, item in enumerate(page_url):
    #try:
    if index <= 52:
        continue
    else:
        get_primary_data(item)
        #except:
        print(item)
        house_data = pd.DataFrame({
            'Id': HouseBasicDataId,
            'square': HouseBasicDataSquare,
            'livingRoom': HouseBasicDataLivingRoom,
            'bedRoom': HouseBasicDataBedroom,
            'Kitchen': HouseBasicDataKitchen,
            'bathroom': HouseBasicDataBathroom,
            'totalFloor': HouseBasicDataTotalFloor,
            'floor': HouseBasicDataFloor,
            'buildingStructure': HouseBasicDataBuildingStructure,
            'builtYear': HouseBasicDataBuiltYear,
            'renovationCondition': HouseBasicDataRenovationCondition,
            'buildingType': HouseBasicDataBuildingType,
            'houseStructure': HouseBasicDataHouseStructure,
            'stairsHouseRatio': HouseBasicDataStairsHouseRatio,
            'hasElevator': HouseBasicDataHasElevator,
            'secondaryDistrict': HouseBasicDataSecondaryDistrict,
            'primaryDistrict': HouseBasicDataPrimaryDistrict,
            'orientation': HouseBasicDataOrientation,
            'tradeTime': HouseTradeDataTradeTime,
            'daysOnMarket': HouseTradeDataDaysOnMarket,
            'follower': HouseTradeDataFollower,
            'ageProperty': HouseTradeDataAgeProperty,
            'listPrice': HouseTradeDataListPrice,
            'transactionPrice': HouseTradeTransactionPrice,
        })
        house_data.to_csv('./' + str(index) + '.csv', encoding='utf-8')
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
        HouseTradeDataListPrice = []
        # 成交价
        HouseTradeTransactionPrice = []

