def check(filename):
	"""检查并删除词典中的重复词"""
	import os
	import shutil
	mark = 0
	new = ''
	fr = open(filename, 'r', encoding='utf8')
	for word in fr.readlines():
		if '，' in word:
			print ('逗号GET!')
			new_word = word.rstrip().split('，')
			print (new_word)
			for s in new_word:
				if s not in new:
					new += (s + '\n')
				else:
					print (s)
					mark += 1
		elif word not in new:
			new += word
		else:
			mark += 1
	fr.close()
	if mark != 0:
		name = os.path.split(filename)[1]
		shutil.move(filename, os.path.join('e:/词典备份', filename))
		new_file = open(filename, 'w', encoding='utf8')
		new_file.write(new)
		new_file.close()
		print('Bingo!')
	else:
		print('没有重复!')


def re_modified(filename):
	"""删除词典中的标签"""
	fr = open(filename, 'r', encoding='utf8')
	new_fr = open(path, 'w', encoding='utf8')

	#to_match = r'(\S+)\t\w+'

	for word in fr.readlines():
		if '\t' in word.strip():
			new_word = word.strip().split('\t')[0]
			new_fr.write(new_word)
			new_fr.write('\n')
	fr.close()
	new_fr.close()

def total_dic(dirname):
	"""把各个词典中的词汇总在一起, 去掉标签"""
	import os
	word_list = []
	for filename in os.listdir(dirname):
		fr = open(os.path.join(dirname, filename), 'r', encoding='utf8')
		for word in fr.readlines():
			if len(word.split()) > 0:
				word_list.append(word.split('\t')[0]+'\n')
		fr.close()
	new = open(os.path.join(dirname, 'total.txt'), 'w', encoding='utf8')
	new.writelines(word_list)
	new.close()



def modified(filename):
	'''调整词典, 为其中的词添加标签'''
	import os
	import shutil

	name = os.path.split(filename)[1]
	mark_dict = {'bodypart.txt': 'B', 'disease.txt': 'Di', \
	'drugs.txt': 'Dr', 'procedure.txt': 'P', 'symptoms.txt': 'S', 'test.txt': 'T'} 
	mark = mark_dict[name]

	fr = open(filename, 'r', encoding='utf8')
	word_list= []
	i = 0
	for word in fr.readlines():
		if len(word.strip()) != 0 and '\t' not in word.strip():
			word_list.append(word[:-1] + '\t' + mark + '\n')
			i += 1
	fr.close()

	if i != 0:
		print('Add Some Marks for %s'%name)
		shutil.move(filename, os.path.join('e:/词典备份', name))
		new_file = open(filename, 'w', encoding='utf8')
		new_file.writelines(word_list)
		new_file.close()

import os
#path = 'C:/Users/yingying.zhu/Documents/dictsdisease.txt'
# for file in os.listdir(path):
# 	modified(os.path.join(path, file))
#total_dic(path)

check('C:/Users/yingying.zhu/Documents/dicts/disease.txt')

