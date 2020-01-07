

'''
	本文档实百度地图相关API功能。
	by：Json Chen
	created：2019-04-30
	update record:
		2019-06-05	Json	添加输入联想功能函数
'''


import requests
import json





def region_search(query,city,tag=None, scope=1):
	'''	
		功能：地点检索服务，检索某一城市内的地点信息
		输入：
			query:必须，检索关键字。
			city：必须，输入行政区划名或对应cityCode。例如：北京、131
			tag：可选，默认为None，检索分类偏好，与q组合进行检索，多个分类以","分隔（POI分类），如果需要严格按分类检索，请通过query参数设置。
			scope：检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
		返回：
			解析结果。参考http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
	'''
	assert type(query) == str
	assert type(city) == str
	other_parameters_str = ''
	if tag:
		assert type(tag) == str
		tag_str = 'tag={}'.format(tag)
		other_parameters_str += '&' + tag_str
	else:
		tag_str = ''
		
	url = 'http://api.map.baidu.com/place/v2/search?query={}&region={}&output=json&ak=3rzLf34kGHElNZVDUonuOwE2vFY8jgvL&scope={}'.format(query, city, scope) + other_parameters_str
	res = requests.get(url)
	return json.loads(res.text)
	


def geo_encode(address,city=None,ret_coordtype=None):
	'''	
		功能：正向地理编码，将结构化地址（省/市/区/街道/门牌号）解析为对应的位置坐标
		输入：
			address:必须，待解析的地址。最多支持84个字节。
			city：可选，默认为None。地址所在的城市名。用于指定上述地址所在的城市。
			ret_coordtype：可选，默认为None，返回百度坐标。可选'gcj02ll'或'bd09mc'，添加后返回国测局经纬度坐标或百度米制坐标。
		返回：
			解析结果。参考http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
	'''
	assert type(address) == str
	
	other_parameters_str = ''
	if city:
		assert type(city) == str
		city_str = 'city={}'.format(city)
		other_parameters_str += '&' + city_str
	else:
		city_str = ''
	if ret_coordtype:
		assert type(ret_coordtype) == str
		ret_coordtype_str = 'ret_coordtype={}'.format(ret_coordtype)
		other_parameters_str += '&' + ret_coordtype_str
	else:
		ret_coordtype_str = ''
	url = 'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=3rzLf34kGHElNZVDUonuOwE2vFY8jgvL&callback=showLocation'.format(address) + other_parameters_str
	res = requests.get(url)
	return eval(res.content[26:])
	
	
	
	
def geo_decode(lng, lat, **kwargs):
	"""
	根据地理坐标获取地址信息
	:param lng,lat: 地理坐标
	:param kwargs:
	:return: if success return
		{ 'location': {'lat':, 'lng'},
		  'origin_location': {'lat':, 'lng'}, # 这是请求的location, 并非百度原始返回的
		  'formatted_address":, # 结构化地址信息
		  'business':, # 商圈
		  'addressComponent': # 地址信息
			{ 'country":, # 国家
			  'province':, # 省名
			  'city':, # 城市名
			  'district':, # 区县名
			  'street':, # 街道名
			  'street_number':, # 街道门牌号
			  'country_code':, # 国家code
			  'direction':, # 和当前坐标点的方向
			  'distance': # 和当前坐标点的距离
			}
		  'pois': # 周边poi数组
			{ 'addr':, # 地址信息
			  'cp':, # 数据来源
			  'direction':, # 和当前坐标点方向
			  'distance':, # 离坐标点距离
			  'name':, # poi名称
			  'poiType':, # poi类型, 如'办公大楼, 商务大厦'
			  'point':, # poi坐标
			  'tel':, # 电话
			  'uid':, # poi唯一标识
			  'zip':, # 邮编
			}
		  'sematic_description':, # 当前位置结合POI的语义化结果描述
		} or return None.
	:raise ParamError: if location is None.
	"""
	if lng is None or lat is None:
		raise ParamError(u'经纬度不能为空')
	params = {'ak': '3rzLf34kGHElNZVDUonuOwE2vFY8jgvL', 'output': 'json', 'location': '{lat},{lng}'.format(lat=lat,lng=lng),
			  'coordtype': kwargs.get('coordtype', 'bd09ll'), 'pois': kwargs.get('pois', 0)}
	try:
		r = requests.get("http://api.map.baidu.com/reverse_geocoding/v3/", params=params)
		r.raise_for_status()

		data = json.loads(r.text)
		return data
	except Exception as e:
		print(e)

	
	
def geo_suggestion(query, city):
	'''	
		功能：地点输入提示，匹配用户输入关键词的地点推荐列表
		输入：
			query:必须，输入建议关键字（支持拼音）。
			city：必须，支持全国、省、城市及对应百度编码（Citycode）。
		返回：
			解析结果。参考http://lbsyun.baidu.com/index.php?title=webapi/place-suggestion-api
	'''
	assert type(query) == str
	assert type(city) == str
	url = "http://api.map.baidu.com/place/v2/suggestion?query={}&region={}&city_limit=true&output=json&ak=3rzLf34kGHElNZVDUonuOwE2vFY8jgvL".format(query,city)
	res = requests.get(url)
	return json.loads(res.text)
	
	
	