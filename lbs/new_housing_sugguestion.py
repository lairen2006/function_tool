# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:16:32 2019

@author: wuhaoyu
"""


import requests 
from bs4 import BeautifulSoup
from lxml import etree
import re
from fake_useragent import UserAgent 

ua = UserAgent()

# 设置代理

# 关联匹配抬头
headers1 = {
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '52',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }

# 详情页抬头
headers2 = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }

# 地图页抬头
headers3 = {  
   'Accept': '*/*',   
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'zh-CN',
   'Host': 'ditu.fang.com',
   'User-Agent':  ua.random
   }
data = {
        'atype':'4',
        }

city_Shorthand = {
        '广州': 'gz',
        '佛山'：'fs',
        '东莞'：'dg',
        '中山'：'zs'
        }
 

def new_housing_sugguestion(building_name,city_name):
    
    '''
    房天下新房联想,返回相关度最高的楼盘信息
    '''

    global headers1
    global headers2
    
    try:
        city_name_code = city_Shorthand[city_name]
        # 根据项目城市及名称传入参数
        headers1['Host'] = '{}.newhouse.fang.com'.format(city_name_code)
        data['q'] =  building_name
        url = 'https://{}.newhouse.fang.com/house/web/proxy.php'.format(city_name_code)
    
        # 按克尔瑞项目名检索项目
        res = requests.post(url, headers = headers1, data = data)
        soup = BeautifulSoup(res.content)
        
        # 提取房天下匹配信息
        pattern = '(.*)\^.*\^1\^(.*)\^\^\^0\^(.*)\^0\^0##(.*)\^\d+##(.*)\^0##(.*)\^0\^0\^0\^0'
        match_result = re.match(pattern,soup.text).groups()
    
        url = match_result[1]
        headers2['Host'] = url[7:-1]
        
        res = requests.get(url, headers = headers2)
        html = etree.HTML(res.content.decode('gbk'))
        detail_url = html.xpath('//a[@id = "xfptxq_B03_08" or @id = "xfdsxq_B03_08" ]/@href')
        building_id = detail_url[0][-26:-16]
       
        # 获取坐标
        map_url = 'https://ditu.fang.com/?c=channel&a=xiaoquNew&newcode={}&city={}&sign=pt&width=1200&height=455&resizePage={}/house/web/map_resize.html&category=residence'.format(building_id,city_name_code,url)
        res = requests.get(map_url, headers = headers3)
        html = etree.HTML(res.content.decode('gbk'))
        building_info_script = html.xpath('//body/script[1]/text()')[0]
        pattern = '.*"baidu_coord_x":"(\d+.\d+)","baidu_coord_y":"(\d+.\d+)".*'
        coordinate_info = re.match(pattern,building_info_script).groups()                                                           
        return coordinate_info
    except:
        if city_name in building_name:
            building_name = building_name.replace(city_name,"")
            return new_housing_sugguestion(building_name,city_name)
        else:
            print("无相关新盘,请明确楼盘名")


if __name__ == "__main":
	new_housing_sugguestion('广州瑚璟花园','广州')
