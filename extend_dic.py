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

def find_mod(path, dic):
    """用字典中的词发现文本模式"""
    dic =  open(dic, 'r', encoding= 'utf8')
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
        txt_fr.close()
        if len(txt_file) > 0:
            for word in word_list:
                inde = word.split('\t')[0]
                loc_list = [w.start() for w in re.finditer(inde, txt_file)]
                for loc in loc_list:
                    num += 1
                    for i in range(1, (p+1)):
                        for j in range(1,(q+1)):
                            ext_word = txt_file[max(0, loc - i): min(loc + len(word) + j, len(txt_file)-1)]
                            ext_wd = some_little_modify(ext_word)
                            local_ind = ext_wd.index(some_little_modify(inde))
                            try:
                                mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(inde)+ext_wd[local_ind+len(inde):])
                            except re.error:
                                print (inde + '\t\t' + ext_word + '\n')
                            if mod not in mod_list:
                                mod_list.append(mod)
                                word_count[mod] = 1
                            else:
                                word_count[mod] += 1
    dic.close()
    return mod_list, word_count


def find_word(path, mod_list):
    file_list = os.listdir(path)
    mod_dict = {}
    for mod in mod_list:
        wor_set = set()
        for file in file_list:
            with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
                txt_file = txt_fr.read()
                wor_set = wor_set.union(set(re.findall(mod, txt_file)))
        num_extract = len(wor_set)
        mod_dict[mod] = num_extract
    return mod_dict


def score_mod(mod, mod_dict, word_count):
    import math
    return float(mod_dict[mod])/float(word_count[mod])*math.log(float(mod_dict[mod]) + 1, 2)


path = 'E:/病例特点'
dic = 'C:/Users/yingying.zhu/Documents/dicts/disease.txt'
print (dic)
mod_list, count = find_mod(path, dic)
print (mod_list[:15])