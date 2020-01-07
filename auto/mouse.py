
'''
	功能：该脚本实现鼠标、键盘自动化操作
	by：Json Chen
	created: 2018-10-30
'''


import aircv as ac
from PIL import ImageGrab
import pyautogui as ms
import os
import pdb
import win32con
import win32clipboard as w


def matchImg(imgobj, imgsrc=None, confidencevalue=0.5):#imgsrc=原始图像，imgobj=待查找的图片
	'''
		功能：在指定图片或当前桌面上定位目标图片所在位置
		输入：
			imgobj:必须，需定位目的图片路径。
			imgsrc：可选，默认为None。源图片路径，若为空，默认为当前桌面截屏
		返回：
			图片在给定图片中的位置以及可靠率
	'''
	imobj = ac.imread(imgobj)
	if not imgsrc:
		current_abs_path = os.path.split(os.path.realpath(__file__))[0]
		file_name = os.path.join(current_abs_path, 'total.png')
		im = ImageGrab.grab()
		im.save(file_name,'png')
		imsrc = ac.imread(file_name)
	else:
		imsrc = ac.imread(imgsrc)
 
	match_result = ac.find_template(imsrc,imobj,confidencevalue)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
	if match_result is not None:
		match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

	return match_result
	
	
def locateOnScreen(imgobj='to_det_1.png'):
	'''
		功能：在当前桌面上定位目标图片所在位置
		输入：
			imgobj:必须，需定位目的图片路径。
		返回：
			图片在当前桌面的位置
	'''
	if os.path.isfile(imgobj):
		return ms.locateOnScreen(imgobj)
	else:
		raise IOError('object img {} not found!'.format(imgobj))
	
	
def get_pixel(x,y):
	'''
		功能：获取x,y位置像素RGB颜色值
		输入：
			x：必须，float或int。x轴位置
			y：必须，float或int。y轴位置
		返回：
			rgb_color：tuple，RGB颜色值。
	'''
	assert type(x) == int or type(x) == float
	assert type(y) == int or type(y) == float
	return ms.pixel(x, y)
	
	
def match_color(x,y,rgb,tolerance=10):
	'''
		功能：匹配x,y位置像素RGB颜色值与给定颜色值的区别
		输入：
			x：必须，float或int。x轴位置
			y：必须，float或int。y轴位置
			rgb：必须，tuple。需匹配的rgb颜色值
			tolerance：可选，int，默认为10。容忍值，表示红、绿、蓝三种颜色分别可以容忍的差异程度。
		返回：
			rgb_color：tuple，RGB颜色值。
	'''
	assert type(x) == int or type(x) == float
	assert type(y) == int or type(y) == float
	assert type(rgb) == tuple
	assert type(tolerance) == int
	is_match = ms.pixelMatchesColor(x, y, rgb, tolerance=tolerance)
	return is_match
	
	
def move_mouse_abs(x,y,duration=0.25):
	'''
		功能：移动鼠标到绝对位置
		输入：
			x：必须，float或int。移动到的x轴位置
			y：必须，float或int。移动到的y轴位置
			duration：可选，float，默认为0.25。移动持续时长，单位s。
		返回：
			无
	'''
	assert type(x) == int or type(x) == float
	assert type(y) == int or type(y) == float
	ms.moveTo(x, y, duration=duration)
	return None

	
	
def move_mouse_rel(x,y,duration=0.25):
	'''
		功能：移动鼠标到相对于当前位置的偏移距离
		输入：
			x：必须，float或int。x轴方向的偏移距离
			y：必须，float或int。y轴方向的偏移距离
			duration：可选，float，默认为0.25。移动持续时长，单位s。
		返回：
			无
	'''
	assert type(x) == int or type(x) == float
	assert type(y) == int or type(y) == float
	ms.moveRel(x, y, duration=duration)
	return None
	
	
	
def get_mouse_position():
	'''
		功能：获取鼠标所在位置
		输入：
			无
		返回：
			x：鼠标x轴位置。
			y：鼠标y轴位置。
	'''
	x, y = ms.position()
	return x,y
	
	
	
def click_mouse(x=None, y=None, button='left'):
	'''
		功能：模拟鼠标单击
		输入：
			x,y：可选，默认为None。鼠标点击的位置，默认是当前位置
			button：可选，默认为lefet。要点击的按键，有三个可选值：‘left’, ‘middle’,  ‘right’。
		返回：
			x：鼠标x轴位置。
			y：鼠标y轴位置。
	'''
	if x:
		ms.click(x=cur_x, y=cur_y, button='left')
	else:
		ms.click(button=button)
	return None
	
	
	
def scroll_mouse(span):
	'''
		功能：模拟鼠标滚轮滚动
		输入：
			span：必须，int或float类型。滚动距离，值为正往上滚，值为负往下滚。
		返回：
			无
	'''
	assert type(span) == int or type(span) == float
	ms.scroll(span)
	return None
	
	
	
def type_key(type_list, duration=0.25):
	'''
		功能：模拟键盘打字
		输入：
			type_list：必须，string或string list类型。键盘输入的内容。type_list为string类型时，输入字符串；为list类型时，会识别特殊键值。
			duration：可选，float，默认为0.25。移动持续时长，单位s。
		返回：
			无
		备注：一些特殊的键值如下：
			‘enter’(或‘return’ 或 ‘\n’)	回车
			‘esc’	ESC键
			‘shiftleft’, ‘shiftright’	左右SHIFT键
			‘altleft’, ‘altright’	左右ALT键
			‘ctrlleft’, ‘ctrlright’	左右CTRL键
			‘tab’ (‘\t’)	TAB键
			‘backspace’, ‘delete’	BACKSPACE 、DELETE键
			‘pageup’, ‘pagedown’	PAGE UP 和 PAGE DOWN键
			‘home’, ‘end’	HOME 和 END键
			‘up’, ‘down’, ‘left’, ‘right’	箭头键
			‘f1’, ‘f2’, ‘f3’….	F1…….F12键
			‘volumemute’, ‘volumedown’, ‘volumeup’	有些键盘没有
			‘pause’	PAUSE键
			‘capslock’, ‘numlock’, ‘scrolllock’	CAPS LOCK, NUM LOCK, 和 SCROLLLOCK 键
			‘insert’	INS或INSERT键
			‘printscreen’	PRTSC 或 PRINT SCREEN键
			‘winleft’, ‘winright’	Win键
			‘command’	Mac OS X command键
	'''
	
	ms.typewrite(type_list, duration)
	
	

def hot_key(*args):
	'''
		功能：模拟热键
		输入：
			args:必须，热键标识，string类型。
		返回：
			无
		备注：一些热键值如下：
			['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
			')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
			'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
			'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
			'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
			'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
			'browserback', 'browserfavorites', 'browserforward', 'browserhome',
			'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
			'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
			'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
			'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
			'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
			'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
			'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
			'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
			'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
			'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
			'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
			'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
			'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
			'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
			'command', 'option', 'optionleft', 'optionright']
	'''
	ms.hotkey(*args)
	
	
	
def key_down(key_string):
	'''
		功能：按下按键（不放开）
		输入：
			key_string:必须，热键标识，string类型。
		返回：
			无
	'''
	ms.keyDown(*args)
	
	
	
def key_up(key_string):
	'''
		功能：放开按键
		输入：
			key_string:必须，热键标识，string类型。
		返回：
			无
	'''
	ms.keyUp(*args)



	

	
	
if __name__ == '__main__':
	result = matchImg('to_det_1.png')
	print(result)
	print(ms.locateOnScreen('to_det_1.png'))  # 该方法也可用于定位
	x = (result['rectangle'][0][0] + result['rectangle'][2][0])/2
	y = (result['rectangle'][0][1] + result['rectangle'][1][1])/2
	ms.moveTo(x,y)