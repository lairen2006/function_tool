
'''
	本文档存储常用http操作的函数。
	by：Json Chen
	created：2018-10-26
	update record:
		2018-10-29	Json	新增url编解码函数
'''

import requests
from urllib.parse import unquote


def add_cookie(scrawer_session, name, value, **kwargs):
	"""
		功能：将自定义的cookie内容加载到requests.session对象中并返回该对象
		输入：
			scrawer_session：必须，requests.session对象。需要新增cookie的会话。
			name：必须，需添加的cookie名称
			value：必须，需添加的cookie值
			**kwargs：可选，cookie的其他对象，例如：path、domain
		返回：
			scrawer_session：requests.session对象
	"""
	c = requests.cookies.RequestsCookieJar()
	c.set(name, value, **kwargs) # example: c.set('Referer', refer_url, path='/', domain='www.cq315house.com')
	scrawer_session.cookies.update(c)
	return scrawer_session
	
	
	
def url_decode(text):
	"""
		功能：url解码
		输入：
			text：必须，string。需要解码的字符串。
		返回：
			解码后的字符串
	"""
	if isinstance(text,str):
		return unquote(text, 'utf-8')
	else:
		raise ValueError("text must be string type, {} got".format(type(text)))

		
		
def url_encode(text):
	"""
		功能：url编码
		输入：
			text：必须，string。需要编码的字符串。
		返回：
			编码后的字符串
	"""
	if isinstance(text,str):
		return quote(text, 'utf-8')
	else:
		raise ValueError("text must be string type, {} got".format(type(text)))	
		