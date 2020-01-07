
'''
	本文档实现地理位置计算功能。
	by：Json Chen
	created：2019-05-10
'''




from math import radians, cos, sin, asin, sqrt
 
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
	'''
		功能：计算两个经纬度距离
		输入：
			lon1, lat1, lon2, lat2:必须，两点经纬度。
		返回：
			距离，单位为米
	'''
	
	try:
		# 将十进制度数转化为弧度
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	 
		# haversine公式
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371 # 地球平均半径，单位为公里
		return c * r * 1000
	except Exception as e:
		return None
