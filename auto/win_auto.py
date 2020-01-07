
'''
	功能：该脚本实现windows自动化操作，包括剪贴板、文件等
	by：Json Chen
	created: 2019-1-11
'''



import win32con
import win32clipboard as w


def get_clipboard():
	'''
		功能：获取剪贴板内容
		输入：
			无
		返回：
			剪贴板内容字符串
	'''
	w.OpenClipboard()
	d = w.GetClipboardData(win32con.CF_UNICODETEXT)
	w.CloseClipboard()
	return d
	
	
def set_clipboard(aString):
	'''
		功能：设置剪贴板
		输入：
			aString:必须，string。需设置到剪贴板的字符串
		返回：
			无
	'''
	w.OpenClipboard()
	w.EmptyClipboard()
	w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
	w.CloseClipboard()