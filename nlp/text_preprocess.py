

'''
	本文档存储常用文本预处理的函数。
	by：Json Chen
	created：2018-10-23
	update record:
		2018-10-26	Json	修改cut_text_with_ps函数，新增without_stopwords、stop_words_filename字段用于判断是否去除停用词
		2019-02-18	Json	新增split_sentences函数
'''


import jieba.posseg as pseg
import jieba
import os
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# 停用词性
STOP_FLAG = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

def load_user_defined_words(file_name = None):
	"""
		功能：加载用户预定义好的中文词组，作为后续分词依据
		输入：
			file_name：可选，默认为'defined_words.txt'。预定义词组存储的文件名。
		返回：
			None
	"""
	if not file_name:
		current_abs_path = os.path.split(os.path.realpath(__file__))[0]
		file_name = os.path.join(current_abs_path, 'defined_words.txt')
	try:
		print('getting user defined words from {}'.format(file_name))
		user_defined_words = [line.strip() for line in open(file_name, 'r').readlines()]
		jieba.load_userdict(user_defined_words)
		print('user defined words loaded!')
	except Exception as e:
		print(e)

		
		
def get_stop_words(file_name = None):
	"""
		功能：加载用户预定义好的停用词
		输入：
			file_name：可选，默认为'stop_words.txt'。预定义词组存储的文件名。
		返回：
			stop_words:停用词列表
	"""
	if not file_name:
		current_abs_path = os.path.split(os.path.realpath(__file__))[0]
		file_name = os.path.join(current_abs_path, 'stop_words.txt')
	try:
		print('getting stop words from {}'.format(file_name))
		stop_words = [line.strip() for line in open(file_name, 'r').readlines()]
		print('stop words loaded!')
		return stop_words
	except Exception as e:
		print(e)
		return []
		
		

def cut_text_with_ps(contents, without_stopwords = True, stop_words_filename = None):	
	"""
		功能：对文本进行分词，并将分词后的词组按词性归类到dict中。
		输入：
			contents：必须，list or string。需进行分词的内容。
			without_stopwords：可选，bool，默认为True。分词后是否去除停用词。
			stop_words_filename：条件可选，string，在without_stopwords为True时有效，默认值为None。存放停用词的文件路径。
		返回：
			dic_word_count:分词结果。key值为词性缩写，value为对应的词组
		备注：各词性缩写说明如下。
			词性编码	词性名称	注 解
			Ag	形语素	形容词性语素。形容词代码为 a，语素代码ｇ前面置以A。
			a	形容词	取英语形容词 adjective的第1个字母。
			ad	副形词	直接作状语的形容词。形容词代码 a和副词代码d并在一起。
			an	名形词	具有名词功能的形容词。形容词代码 a和名词代码n并在一起。
			b	区别词	取汉字“别”的声母。
			c	连词	取英语连词 conjunction的第1个字母。
			dg	副语素	副词性语素。副词代码为 d，语素代码ｇ前面置以D。
			d	副词	取 adverb的第2个字母，因其第1个字母已用于形容词。
			e	叹词	取英语叹词 exclamation的第1个字母。
			f	方位词	取汉字“方”
			g	语素	绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母。
			h	前接成分	取英语 head的第1个字母。
			i	成语	取英语成语 idiom的第1个字母。
			j	简称略语	取汉字“简”的声母。
			k	后接成分	
			l	习用语	习用语尚未成为成语，有点“临时性”，取“临”的声母。
			m	数词	取英语 numeral的第3个字母，n，u已有他用。
			Ng	名语素	名词性语素。名词代码为 n，语素代码ｇ前面置以N。
			n	名词	取英语名词 noun的第1个字母。
			nr	人名	名词代码 n和“人(ren)”的声母并在一起。
			ns	地名	名词代码 n和处所词代码s并在一起。
			nt	机构团体	“团”的声母为 t，名词代码n和t并在一起。
			nz	其他专名	“专”的声母的第 1个字母为z，名词代码n和z并在一起。
			o	拟声词	取英语拟声词 onomatopoeia的第1个字母。
			p	介词	取英语介词 prepositional的第1个字母。
			q	量词	取英语 quantity的第1个字母。
			r	代词	取英语代词 pronoun的第2个字母,因p已用于介词。
			s	处所词	取英语 space的第1个字母。
			tg	时语素	时间词性语素。时间词代码为 t,在语素的代码g前面置以T。
			t	时间词	取英语 time的第1个字母。
			u	助词	取英语助词 auxiliary
			vg	动语素	动词性语素。动词代码为 v。在语素的代码g前面置以V。
			v	动词	取英语动词 verb的第一个字母。
			vd	副动词	直接作状语的动词。动词和副词的代码并在一起。
			vn	名动词	指具有名词功能的动词。动词和名词的代码并在一起。
			w	标点符号	
			x	非语素字	非语素字只是一个符号，字母 x通常用于代表未知数、符号。
			y	语气词	取汉字“语”的声母。
			z	状态词	取汉字“状”的声母的前一个字母。
			un	未知词	不可识别词及用户自定义词组。取英文Unkonwn首两个字母。(非北大标准，CSW分词中定义)
	"""

	if not isinstance(contents, list):
		contents = [contents]
	stop_words = get_stop_words(stop_words_filename) if without_stopwords else []
	dic_word_count = {}
	for content in contents:
		word_list = pseg.cut(content)
		for word in word_list:
			if word.word not in stop_words:
				if word.flag[0] in dic_word_count:
					dic_word_count[word.flag[0]].append(word.word)
				else:
					dic_word_count[word.flag[0]] = [word.word]
	return dic_word_count

	
	
def fuzz_ratio(text_a, text_b):
	'''
		功能：字符串模糊匹配，对位置敏感，全匹配
		输入：
			text_a：必选，string，待匹配字符串1。
			text_b：必选，string，待匹配字符串2。
		返回：
			匹配概率
		例子：
			>>fuzz.ratio("this is a test", "this is a test!")
				97
	'''
	return fuzz.ratio(text_a, text_b)
	
	
	
def fuzz_partial_ratio(text_a, text_b):
	'''
		功能：字符串模糊匹配，对位置敏感，搜索匹配
		输入：
			text_a：必选，string，待匹配字符串1。
			text_b：必选，string，待匹配字符串2。
		返回：
			匹配概率
		例子：
			>>fuzz.partial_ratio("this is a test", "this is a test!")
				100
	'''
	return fuzz.partial_ratio(text_a, text_b)
	
	
	
def fuzz_token_sort_ratio(text_a, text_b):
	'''
		功能：字符串模糊匹配，对位置不敏感，全匹配
		输入：
			text_a：必选，string，待匹配字符串1。
			text_b：必选，string，待匹配字符串2。
		返回：
			匹配概率
		例子：
			>>> fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
				91
			>>> fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
				100
	'''
	return fuzz.token_sort_ratio(text_a, text_b)

	
def fuzz_token_set_ratio(text_a, text_b):
	'''
		功能：字符串模糊匹配，对位置不敏感，去重
		输入：
			text_a：必选，string，待匹配字符串1。
			text_b：必选，string，待匹配字符串2。
		返回：
			匹配概率
		例子：
			>>> fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
				84
			>>> fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
				100
	'''
	return fuzz.token_set_ratio(text_a, text_b)
	

	
	
def split_sentences(text,p='[。.，,？：]',filter_p='\s+'):
	'''
		功能：输入整段文本，去除掉文本中的空白部分，并按照标点符号分裂成list
		输入：
			text：必选，string，待处理的整段文本。
			p：可选，string list，用于分割文本的标点符号，默认为中文的逗号、句号、问号及冒号。
			filter_p，可选，正则表达式，用于替换原始文本的内容，默认为替换空白字符部分。
		返回：
			list格式，分割后的句子列表。
	'''
	f_p = re.compile(filter_p)
	text = re.sub(f_p,'',text)
	pattern = re.compile(p)
	split = re.split(pattern,text)
	return split



	
	
	
	