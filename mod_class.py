import math
import os
import re

def frequence(word, path):
    """计算 word 在 path 处的文档库中出现的频数"""
    res = 0
    file_list = os.listdir(path)
    for file in file_list:
        with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
            txt_file = some_little_modify(modified(txt_fr.read()))
        res += txt_file.count(word)
    return res


class Mod(object):

	def __init__(self, mod_name, mod_match=None, word_match=None, mod_match_neg=None, mod_match_unlabel=None):
		
		self.name = mod_name
		self.match = mod_match
		self.match_positive = word_match
		self.match_negtive = mod_match_neg
		self.match_unlabel = mod_match_unlabel

		self.counts = len(self.match)
		self.counts_positive = len(self.match_positive)
		self.counts_negtive = len(mod_match_neg)
		self.counts_unlabel = len(mod_match_unlabel)

	def get_score(self):
		precision = self.counts_positive/self.count    #准确率
		capacity = math.log(1 + self.counts_unlabel, 2)    #发现新词的能力
		recall = math.log(1 + self.counts_positive, 2)    #被词典中的词汇匹配的程度
		score = precision * recall * capacity
		self.__score = score
		return score

	def __str__(self):
		return self.name


class Word(object):

	def __init__(self, word_name, match_list=None, frequence=None):
		
		self.name = word_name
		self.match = match_list    #匹配 word 的模式列表
		self.counts = len(self.match)
		self.frequence = frequence

	def get_match(self, mod_list):
		self.match = [mod for mod in mod_list if self.name in mod.match]
		return self.match

	def get_frequence(self, doc_path):
		self.frequence = frequence(self.name, doc_path)
		return self.frequence

	def get_score(self):
		self.score = sum([math.log(mod.counts_positive + 1, 2) for mod in self.match])/self.counts
		return self.score

	
class Entity(object):

	def __init__(self, start=None, end=None, time=None, patient=None):
		self.start = start
		self.end = end
		self.time = time
		self.patient = patient

	







