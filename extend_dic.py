import os
import re

def some_little_modify(s):
    """在字符串中的(及)前面加上\, 方便转换成正则表达式"""
    to_be_removed = ['(', ')', '+', '*']
    for signal in to_be_removed:
        s = s.replace(signal, '\\'+signal)
    return s

def find_all(substring, string):
    start = 0
    while True:
        start  = string.find(substring, start)
        if start == -1:
            return -1
        yield start
        start += len(substring)


def read_dict(dic):
    with open(dic, 'r', encoding= 'utf8') as dic_fr:
        word_list = [x.split()[0] for x in dic_fr.readlines()]
    return word_list

def find_mod(path, dic):
    """用字典中的词发现文本模式"""
    file_list = os.listdir(path)
    word_list = read_dict(dic)
    word_count = {}
    #用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
    mod_list = []
    #文本模式以列表形式保存
    word_match = {}
    for file in file_list:
        with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:          
            p = 5
            q = 5
            txt_file = txt_fr.read()
            if len(txt_file) > 0:
                for word in word_list:
                    loc_list = [w.start() for w in re.finditer(word, txt_file)]
                    for loc in loc_list:
                        for i in range(1, (p+1)):
                            for j in range(1,(q+1)):
                                ext_word = txt_file[max(0, loc - i): min(loc + len(word) + j, len(txt_file)-1)]
                                ext_wd = some_little_modify(ext_word)
                                local_ind = ext_wd.index(some_little_modify(word))
                                try:
                                    mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(word)+ext_wd[local_ind+len(word):])
                                except re.error:
                                    print (word + '\t\t' + ext_word + '\n')
                                if mod not in mod_list:
                                    mod_list.append(mod)
                                    word_match[mod] = {word}
                                else:
                                    word_match[mod] = word_match[mod].union(word)
    for mod in mod_list:
        word_count[mod] = len(word_match[mod]) 
    return mod_list, word_count


def find_word(path, mod_list, dic):
    """用发现的模式去发现文本中的新词"""
    file_list = os.listdir(path)
    word_list = read_dict(dic)
    mod_count = {}
    #键为发现的模式, 相应的值为匹配到的词的数目
    mod_match = {}
    #键为发现的模式, 相应的值为匹配到的词的集合
    new_word = set()
    #匹配到的新词的集合
    for mod in mod_list:
        wor_set = set()
        for file in file_list:
            with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
                txt_file = txt_fr.read()
                wor_set = wor_set.union(set(re.findall(mod, txt_file)))
        #wor_set = wor_set.difference(set(word_list))
        num_extract = len(wor_set)
        mod_count[mod] = num_extract
        mod_match[mod] = wor_set
        new_word = new_word.union(wor_set)
        new_word = new_word.difference(set(word_list))
    return mod_count, mod_match, new_word


def score_mod(mod, mod_count, word_count):
    """计算模式的评分"""
    import math
    return float(word_count[mod])/float(mod_count[mod])*math.log(float(mod_count[mod]) + 1, 2)

def score_word(word, mod_list, mod_count, mod_match):
    import math
    m_list = [mod for mod in mod_list if word in mod_match[mod]]
    return sum([math.log(float(word_count[mod]) + 1, 2) for mod in m_list])/float(len(m_list))


path = 'E:/病例特点'
dic = 'C:/Users/yingying.zhu/Documents/dicts/disease.txt'
print (dic)
mod_list, count = find_mod(path, dic)
print (mod_list[:15])