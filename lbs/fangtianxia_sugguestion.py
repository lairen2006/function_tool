# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:08:41 2019

@author: wuhaoyu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:16:32 2019

@author: wuhaoyu
"""

import time
import hashlib
import requests 
from bs4 import BeautifulSoup
from lxml import etree
import re
from fake_useragent import UserAgent 

ua = UserAgent()

# 设置代理
orderno = "ZF20193243390rSvo4p"
secret = "10680482c9af4ed4b4ae6834601691fe"
ip = "forward.xdaili.cn"
port = "80"
ip_port = ip + ":" + port
timestamp = str(int(time.time()))                # 计算时间戳
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
string = string.encode()
md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
sign = md5_string.upper()                              # 转换成大写
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

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
    'Cache-Control': 'no-cache',
    "Proxy-Authorization": auth
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
    'Cache-Control': 'no-cache',
     "Proxy-Authorization": auth
    }

# 地图页抬头
headers3 = {  
   'Accept': '*/*',   
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'zh-CN',
   'Host': 'ditu.fang.com',
   'User-Agent':  ua.random,
   "Proxy-Authorization": auth
   }
data = {
        'atype':'4',
        }

city_Shorthand = {
    "北京" : "bj",
    "上海" : "sh",
    "广州" : "gz",
    "深圳" : "sz",
    "成都" : "cd",
    "重庆" : "cq",
    "天津" : "tj",
    "杭州" : "hz",
    "南京" : "nanjing",
    "苏州" : "suzhou",
    "济南" : "jn",
    "石家庄" : "sjz",
    "西安" : "xian",
    "昆明" : "km",
    "无锡" : "wuxi",
    "珠海" : "zh",
    "南宁" : "nn",
    "长沙" : "cs",
    "郑州" : "zz",
    "东莞" : "dg",
    "合肥" : "hf",
    "贵阳" : "gy",
    "宁波" : "nb",
    "南昌" : "nc",
    "包头" : "bt",
    "保定" : "bd",
    "北海" : "bh",
    "常德" : "changde",
    "常州" : "cz",
    "滁州" : "chuzhou",
    "长春" : "changchun",
    "大连" : "dl",
    "防城港" : "fangchenggang",
    "佛山" : "fs",
    "福州" : "fz",
    "赣州" : "ganzhou",
    "桂林" : "guilin",
    "哈尔滨" : "hrb",
    "海南" : "hn",
    "衡水" : "hs",
    "呼和浩特" : "nm",
    "黄石" : "huangshi",
    "惠州" : "huizhou",
    "吉林" : "jl",
    "济宁" : "jining",
    "嘉兴" : "jx",
    "江门" : "jm",
    "金华" : "jh",
    "九江" : "jiujiang",
    "昆山" : "ks",
    "兰州" : "lz",
    "廊坊" : "lf",
    "乐山" : "leshan",
    "连云港" : "lyg",
    "临沂" : "linyi",
    "柳州" : "liuzhou",
    "泸州" : "lf",
    "洛阳" : "ly",
    "梅州" : "meizhou",
    "绵阳" : "mianyang",
    "南充" : "nanchong",
    "南通" : "nt",
    "秦皇岛" : "qhd",
    "青岛" : "qd",
    "清远" : "qingyuan",
    "庆阳" : "qingyang",
    "泉州" : "qz",
    "三亚" : "sanya",
    "汕头" : "st",
    "绍兴" : "sx",
    "沈阳" : "sy",
    "台州" : "tz",
    "泰州" : "taizhou",
    "太原" : "taiyuan",
    "唐山" : "ts",
    "威海" : "weihai",
    "潍坊" : "wf",
    "温州" : "wz",
    "乌鲁木齐" : "xj",
    "芜湖" : "wuhu",
    "武汉" : "wuhan",
    "西宁" : "xn",
    "厦门" : "xm",
    "徐州" : "xz",
    "烟台" : "yt",
    "盐城" : "yancheng",
    "扬州" : "yz",
    "宜昌" : "yc",
    "银川" : "yinchuan",
    "岳阳" : "yueyang",
    "枣阳" : "hbzy",
    "湛江" : "zj",
    "漳州" : "zhangzhou",
    "镇江" : "zhenjiang",
    "中山" : "zs",
    "舟山" : "zhoushan",
    "淄博" : "zb",
        }

def new_housing_sugguestion_list(building_name,city_name):
    
    '''
    房天下新房联想,返回相关度最高的楼盘信息
    '''
    list_view = []
    city_name_code = city_Shorthand[city_name]
    # 根据项目城市及名称传入参数
    headers1['Host'] = '{}.newhouse.fang.com'.format(city_name_code)
    data['q'] =  building_name
    url = 'https://{}.newhouse.fang.com/house/web/proxy.php'.format(city_name_code)

    # 按克尔瑞项目名检索项目
    res = requests.post(url, headers = headers1, data = data,proxies = proxy ,verify=False,allow_redirects=False)
    soup = BeautifulSoup(res.content)
  
    # 提取房天下匹配信息
    info_list = soup.text.split(",")
    if len(info_list) > 1:
        info_list = info_list[1:]
    pattern = '(.*)\^.*\^1\^(.*)\^\^\^\d\^(.*)\^0\^0##(.*)\^\d+##(.*)\^0##(.*)\^0\^0\^0\^0'
    for i in info_list:
        match_result = re.match(pattern,i).groups()
        d = {
                "项目名": match_result[0],
                "网址" : match_result[1],
                "区域" : match_result[2],
                "房源信息" : match_result[3],
                "户型" : match_result[4]
                }
        list_view.append(d)
    return list_view

def new_housing_building_id(url):
    '''
    返回building_id
    
    url = match_result[1]
    格式：http://yayunyuanzhu.fang.com/ 
    '''
    headers2['Host'] = url[7:-1]
    
    res = requests.get(url, headers = headers2,proxies = proxy ,verify=False,allow_redirects=False)
    if res.status_code == 302 or res.status_code == 301 :
        loc = res.headers['Location']
        res = requests.get(loc, headers=headers2, proxies=proxy, verify=False, allow_redirects=False)
    html = etree.HTML(res.content.decode('gbk'))
    detail_url = html.xpath('//a[@id = "xfptxq_B03_08" or @id = "xfdsxq_B03_08" ]/@href')
    building_id = detail_url[0][-26:-16]
    
    return building_id



def new_housing_sugguestion_coordinate(building_id,city_name,url):
        '''
        返回坐标点
        格式：
        building_id = '2811887260'
        city_name_code = 'gz'
        url = 'http://yayunyuanzhu.fang.com/'
        '''
        city_name_code = city_Shorthand[city_name]
        map_url = 'https://ditu.fang.com/?c=channel&a=xiaoquNew&newcode={}&city={}&resizePage={}/house/web/map_resize.html'.format(building_id,city_name_code,url)
          
        # 获取坐标
       # map_url = 'https://ditu.fang.com/?c=channel&a=xiaoquNew&newcode={}&city={}&sign=pt&width=1200&height=455&resizePage={}/house/web/map_resize.html&category=residence'.format(building_id,city_name_code,url)
        res = requests.get(map_url, headers = headers3,proxies=proxy,verify=False,allow_redirects=False)
        html = etree.HTML(res.content.decode('gbk'))
        building_info_script = html.xpath('//body/script[1]/text()')[0]
        pattern = '.*"baidu_coord_x":"(\d+.\d+)","baidu_coord_y":"(\d+.\d+)".*'
        coordinate_info = re.match(pattern,building_info_script).groups()                                                           
        
        return coordinate_info
    
if __name__ == '__main__':
	pass