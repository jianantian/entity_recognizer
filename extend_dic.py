# _*_ encoding: utf8 _*_

def some_little_modify(s):
    """ 在字符串中的(及)前面加上\, 方便转换成正则表达式 """
    to_be_removed = ['(', ')', '+', '*', '^', '.', '?', '$', '|']
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
        word_list = list(set([x.split()[0] for x in dic_fr.readlines()]))
    return word_list

def read_txt_file(path):
    """ 从整理好的文本中读取相应内容做成一个列表, 
        列表的每个元为一个句子. 该结果仅用于提取字典使用, 
        不能用于后面的任务, 因为所有病人的文本都混到了一起 """
    import os
    import json
    txt_file = []
    file_list = os.listdir(path)
    for file in file_list:
        with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
            txt_dic = json.load(txt_fr)
        for txt_date in txt_dic.keys():
            txt_list = [line.strip() for line in txt_dic[txt_date].split('。') if line.strip() !='']
            txt_file.extend(txt_list)
    return txt_file


def find_mod(txt_file, word_list):
    import re
    """ 用字典中的词发现文本模式 """
    word_count = {}
    # 用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
    mod_list = []
    # 文本模式以列表形式保存
    word_match = {}

    p = 5
    q = 5

    for line in txt_file:
        if len(line) > 0:
            for word in word_list:
                loc_list = [w.start() for w in re.finditer(word, line)]
                for loc in loc_list:
                    for i in range(1, (p+1)):
                        for j in range(1,(q+1)):
                            if loc - i >= 0 and loc + len(word) + j <len(line):
                                ext_word = line[loc - i: loc + len(word) + j]
                                ext_wd = some_little_modify(ext_word)
                                local_ind = ext_wd.index(some_little_modify(word))
                                try:
                                    mod = (ext_wd[:local_ind], ext_wd[local_ind+len(word):])
                                except re.error:
                                    print (word + '\t\t' + ext_word + '\n')
                                if mod not in mod_list:
                                    mod_list.append(mod)
                                    word_match[mod] = {word}
                                else:
                                    word_match[mod].add(word)
    for mod in mod_list:
        word_count[mod] = len(word_match[mod]) 
    return mod_list, word_count, word_match

# TODO: 优化find_word及find_mod函数的速度


def find_word(txt_file, mod_list, word_list):
    """ 用发现的模式去发现文本中的新词 """
    import re
    mod_count = {}
    # 键为发现的模式, 相应的值为匹配到的词的数目
    mod_match = {}
    # 键为发现的模式, 相应的值为匹配到的词的集合
    new_word = set()
    # 匹配到的新词的集合
    for mod in mod_list:
        word_set = set()
        for line in txt_file:         
            left_index = [w.end() for w in re.finditer(mod[0], line)]
            right_index = [w.start() for w in re.finditer(mod[1], line)]
            start = 0
            i, j = 0, 0
            for i in range(len(left_index)):
                if start < len(right_index):
                    for j in range(start, len(right_index)):
                        if right_index[j] > left_index[i] and (i == len(left_index)-1 or  right_index[j] <= left_index[i+1]):
                            word = line[left_index[i]: right_index[j]]
                            if len(word) < 15: 
                                word_set.add(word)
                                start += 1
                            break
                        elif i < len(left_index) - 1 and right_index[j] > left_index[i+1]:
                            break
                        else:
                            start += 1
        num_extract = len(word_set)
        mod_count[mod] = num_extract
        mod_match[mod] = word_set
        new_word = new_word.union(word_set)
    new_word = list(new_word.difference(set(word_list)))
    return new_word, mod_count, mod_match


def score_mod(mod, mod_count, word_count):
    """ 计算模式的评分, 这里的评分标准可能并不是很好 """
    import math
    return float(word_count[mod])/float(mod_count[mod])*math.log(float(mod_count[mod]) + 1, 2)

def score_word(word, mod_list, mod_count, mod_match):
    """ 计算新词的评分 """
    import math
    m_list = [mod for mod in mod_list if word in mod_match[mod]]
    return sum([math.log(float(word_count[mod]) + 1, 2) for mod in m_list])/(float(len(m_list))+1)


def main(path, text_type, iter_times=2):
    import os
    # global path
    #是否需要全局变量?????
    path = 'E:/病例特点_2'
    dic_path = 'C:/Users/yingying.zhu/Documents/dicts/'
    dic_name = text_type + '.txt'
    dic = os.path.join(dic_path, dic_name)
    txt_file = read_txt_file(path)

    mod_selected = []
    word_list = read_dict(dic)
    num = 0
    while num < iter_times:
        mod_list, word_count, word_match = find_mod(txt_file, word_list)
        new_word, mod_count, mod_match = find_word(txt_file,mod_list, word_list)


        mod_score_list = [score_mod(mod, mod_count, word_count) for mod in mod_list]
        mod_score = list(filter(lambda f: f[1] > 1, sorted(zip(mod_list, mod_score_list), key= lambda x: x[1], reverse=True)))[:20]
        #模式库是需要每一轮都增加的还是每次都取最好的??????? 
        mod_selected.extend([x[0] for x in mod_score])

        new_word, mod_count, mod_match = find_word(txt_file,mod_selected, word_list)
        word_score_list = [score_word(word, mod_selected, mod_count, mod_match) for word in new_word]
        word_score = list(filter(lambda f: f[1] > 0, sorted(zip(new_word, word_score_list), key= lambda x: x[1], reverse=True)))[:20]
        word_list.extend([x[0] for x in word_score])

        num += 1

if __name__ == '__main__':
    main()
