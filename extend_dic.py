import os
import re

def some_little_modify(s):
	"""在字符串中的(及)前面加上\, 方便转换成正则表达式"""
	s_1 = s.replace('(', '\(')
	s_2 = s_1.replace(')', '\)')
	return s_2







def find_mod(path):
	"""用字典中的词发现文本模式"""
	dic =  open('C:/Users/yingying.zhu/Documents/dicts/total.txt', 'r', encoding= 'utf8')
	word_list = dic.readlines()
	file_list = os.listdir(path)

	word_count = {}
	#用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
	mod_list = []
	#文本模式以列表形式保存
	
	num = 0
	for file in file_list:
		txt_fr = open(os.path.join(path, file), 'r', encoding='utf8')
		p = 5
		q = 5
		txt_file = txt_fr.read()
		for word in word_list:
			inde = word.split('\t')[0]
			if inde in txt_file:
				num += 1
				loc = txt_file.index(inde)
				for i in range(1, (p+1)):
					for j in range(1,(q+1)):
						ext_word = txt_file[loc - i:loc + len(inde) + j]
						ext_wd = some_little_modify(ext_word)
						local_ind = ext_wd.index(inde)
						mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(inde)+ext_wd[local_ind+len(inde):])
						if mod not in mod_list:
							mod_list.append(mod)
							word_count[mod] = 1
						else:
							word_count[mod] += 1
	dic.close()
	txt_fr.close()
	return mod_list, word_count


def find_word(path)
	file_list = os.listdir(path)
	mod_dict = {}
	for mod in m_list:
    	wor_set = set()
    	for file in file_list:
        	with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
            	txt_file = txt_fr.read()
            	wor_set = wor_set.union(set(re.findall(mod, txt_file)))
    	num_extract = len(wor_set)
    	mod_dict[mod] = num_extract
    return mod_dict



path = 'E:/病例特点'
mod_list, count = find_mod(path)
print (mod_list[:15])