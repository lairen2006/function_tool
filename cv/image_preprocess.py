

'''
	本文档存储常用图片预处理的函数。
	by：Json Chen
	created：2018-10-23
'''



from PIL import Image
import os
import pdb
import struct

def vertical(img, threshold = 0):
	"""
		功能：将传入二值化后的图片进行垂直投影，并按threshold门限划分切割范围
		输入：
			img：必须，传入Image库打开且二值化后的图片对象
			threshold：可选，默认为0。垂直方向上的黑点数超过threshold才进行切割
		返回：
			cuts：图片垂直方向上的切割。list类型，包含两个元素的tuple值，表示垂直方向切割的上下界。
	"""
	pixdata = img.load()
	w,h = img.size
	ver_list = []
	# 开始投影
	for x in range(w):
		black = 0
		for y in range(h):
			if pixdata[x,y] == 0:
				black += 1
		ver_list.append(black)
	print(ver_list)
	# 判断边界
	l,r = 0,0
	flag = False
	cuts = []
	for i,count in enumerate(ver_list):
		# 阈值这里为0
		if flag is False and count > threshold:
			l = i
			flag = True
		if flag and count <= threshold:
			r = i-1
			flag = False
			cuts.append((l,r))
	return cuts
	
	
	
def binarizing(img,threshold = 122):
	"""
		功能：传入image对象进行灰度、二值处理
		输入：
			img：必须，传入Image库打开的图片对象
			threshold：可选，默认为122。二值化分割门限
		返回：
			img：二值化后的图片对象
	"""
	img = img.convert("L") # 转灰度
	pixdata = img.load()
	w, h = img.size
	# 遍历所有像素，大于阈值的为黑色
	for y in range(h):
		for x in range(w):
			if pixdata[x, y] < threshold:
				pixdata[x, y] = 0
			else:
				pixdata[x, y] = 255
	return img
	
	
	
def depoint(img, depoint_type='four'):
	"""
		功能：传入二值化后的图片进行降噪
		输入：
			img：必须，传入Image库打开的二值化后的图片对象
			depoint_type：可选，默认为'four'。降噪方式选择，值为'four'时，采用上/下/左/右四向模糊化，否则采用八向模糊
		返回：
			img：降噪后的图片对象
	"""
	pixdata = img.load()
	w,h = img.size
	for y in range(1,h-1):
		for x in range(1,w-1):
			count = 0
			if pixdata[x,y-1] > 245:#上
				count = count + 1
			if pixdata[x,y+1] > 245:#下
				count = count + 1
			if pixdata[x-1,y] > 245:#左
				count = count + 1
			if pixdata[x+1,y] > 245:#右
				count = count + 1
			if depoint_type != 'four':
				if pixdata[x-1,y-1] > 245:#左上
					count = count + 1
				if pixdata[x-1,y+1] > 245:#左下
					count = count + 1
				if pixdata[x+1,y-1] > 245:#右上
					count = count + 1
				if pixdata[x+1,y+1] > 245:#右下
					count = count + 1
				if count > 4:
					pixdata[x,y] = 255
			else:
				if count > 2:
					pixdata[x,y] = 255
	return img

	
	
def rgb_to_hex(rgb):
	"""
		功能：将RGB颜色转换为十六进制格式
		输入：
			rgb：必须，tuple。需转换的RGB颜色值，颜色取值范围为0~255
		返回：
			转换后的string格式十六进制颜色值
	"""
    return '#%02x%02x%02x' % rgb
	
	
	
def hex_to_rgb(hex_str):
	"""
		功能：将十六进制格式颜色转换为RGB
		输入：
			hex_str：必须，string。需转换的十六进制颜色值
		返回：
			转换后的tuple格式RGB颜色值，颜色取值范围为0~255
	"""
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))    
    return tuple([val for val in int_tuple])  
	
	
	
	
	
if __name__ == '__main__':
	i = 443
	train_data_set = {}
	already_get_traindata_img = []
	f2 = open('already_get_train_img.txt','r')
	already_get_traindata_img = f2.read().split('\n')
	f2.close()
	f = open('train_record.txt','a')
	f2 = open('already_get_train_img.txt','a')
	for original_im_name in os.listdir("data\\temp"):
		if original_im_name not in already_get_traindata_img:
			original_im = Image.open("data\\temp\\%s"%original_im_name)
			original_im = original_im.convert('L')
			c_img = binarizing(original_im,200)
			c_img = depoint(c_img,'eight')
			x = vertical(c_img,3)

			w,h = original_im.size
			cuts = []
			for ele in x[1:-1]:
				if ele[1] - ele[0] > 1:
					cuts.append((ele[0],0,ele[1],h))

			for n in cuts[:3]:
				i += 1
				temp = original_im.crop(n) # 调用crop函数进行切割
				temp.save("data\\train\\%d.png" % i)
				# temp.show()
				y_data = input()
				train_data_set["%d.png" % i] = y_data
				f.write("%d.png\t%s\n" %(i,y_data))
			f2.write(original_im_name+'\n')
			already_get_traindata_img.append(original_im_name)
	f.close()
	f2.close()