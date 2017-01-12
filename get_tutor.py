import json
import math
import os
import re
import string

from pprint import pprint

def modify_for_re(word):
    """在字符串中的(及)前面加上\, 方便转换成正则表达式"""
    to_be_removed = ['(', ')', '+', '*', '^', '.', '?', '$', '|']
    for signal in to_be_removed:
        word = word.replace(signal, '\\' + signal)
    return word


def trans_punctuation(word):
    # 去掉字符串中的\xa0, 以免报错
    # 文档中中文标点与英文混用, 把句子中的标点替换为半角, 句号不转换, 便于和小数点区分, 用于断句
    word = word.replace('\xa0', '')
    trans_table= str.maketrans('，：“”（）',',:\"\"()')
    word = word.translate(trans_table)
    return word.replace('\xa0', '')


def remove_punctuation(word):
    punctuation = string.punctuation
    punc_list = [ord(s) for s in punctuation]
    trans_table = dict().fromkeys(punc_list, '')
    return word.translate(trans_table)


def get_ordinary_word(ord_path):
    """常用词词典"""
    ord_dic = []
    with open(ord_path, 'r', encoding='utf8') as fr:
        for line in fr.readlines():
            ord_dic.append(line.split()[0])
    return ord_dic


def get_seed(dic_path, dic_type):
    dic_name = dic_type + '.txt'
    dic = os.path.join(dic_path, dic_name)
    with open(dic, 'r', encoding='utf8') as dic_fr:
        word_list = [trans_punctuation(x.split()[0]) for x in dic_fr.readlines()]
    return word_list


def get_neg_list(dic_path, ord_path, dic_type): 
    neg_list = get_ordinary_word(ord_path)
    dic_list = os.listdir(dic_path)
    for dic_name in dic_list:
        if ('txt' in dic_name) and (dic_type not in dic_name) and ('total' not in dic_name):
            neg_path = os.path.join(dic_path, dic_name)
            with open(neg_path, 'r', encoding='utf8') as dic_fr:
                w_list = [trans_punctuation(x.split()[0]) for x in dic_fr.readlines() if len(x.strip()) > 0]
                print 
                neg_list.extend(w_list)
    return neg_list


def manual_filtration(word, neg_list):
    """作用在 word 上, 若该词为负例则返回 True, 否则返回 False"""
    pattern_1 = r',|\.|:|;'
    pattern_2 = r'行|示|为|较'
    pattern_3 = r'切除|标本'
    remove_word_list = neg_list + ['病理', '癌', '炎']
    tnm_pattern = r'[Tt]\S{1,2}[Nn][xX0123][Mm][01]'
    word_no_punc = remove_punctuation(word)
    if ((not re.search(pattern_1, word)) and (not re.search(pattern_2, word)) and (not re.search(pattern_3, word)) 
        and len(word_no_punc) > 1 and (word_no_punc not in remove_word_list)):
        if (not re.search(tnm_pattern, word)) and re.search(r'\d', word):
            return True
        else:
            return False
    else:
        return True


def get_txt_file(txt_path):
    """ 从整理好的文本中读取相应内容做成一个列表, 
        列表的每个元为一个句子. 该结果仅用于提取字典使用, 
        不能用于后面的任务, 因为所有病人的文本都混到了一起 """
    txt_file = []
    file_list = os.listdir(txt_path)
    for file in file_list:
        if os.path.splitext(file)[-1] == '.json':
            with open(os.path.join(txt_path, file), 'r', encoding='utf8') as txt_fr:
                txt_dic = json.load(txt_fr)
            for txt_date in txt_dic.keys():
                line_list = [line.strip() for line in txt_dic[txt_date].split('。') if line.strip() !='']
                txt_file.extend(line_list)
    return txt_file


# 利用生成器, 每次使用的时候都要生成, 不知道和上面的列表哪一种方式更快
# def get_txt_file(path):
#     """ 从整理好的文本中读取相应内容做成一个列表, 
#         列表的每个元为一个句子. 该结果仅用于提取字典使用, 
#         不能用于后面的任务, 因为所有病人的文本都混到了一起 """
#     file_list = os.listdir(path)
#     for file in file_list:
#         if os.path.splitext(file)[-1] == '.json':
#             with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
#                 txt_dic = json.load(txt_fr)
#             for txt_date in txt_dic.keys():
#                 for line in (line.strip() for line in txt_dic[txt_date].split('。') if line.strip() !=''):
#                     yield txt_file


def find_mod(txt_file, word_list):
    """用字典中的词发现文本模式"""
    word_count = {}
    # 用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
    mod_list = []
    # 文本模式以列表形式保存
    word_match = {}
    p = 5
    q = 5
    for line in txt_file:
        line = trans_punctuation(line)
        if len(line) > 0:
            for word in word_list:
                word = modify_for_re(word)
                loc_list = [w.start() for w in re.finditer(word, line)]
                for loc in loc_list:
                    for i in range(1, (p + 1)):
                        for j in range(1, (q + 1)):
                            if loc - i >= 0 and loc + len(word) + j < len(line):
                                ext_word = line[loc - i: loc + len(word) + j]
                                ext_wd = modify_for_re(ext_word)
                                local_ind = ext_wd.index(word)
                                try:
                                    # mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(word)+ext_wd[local_ind+len(word):])
                                    mod = (ext_wd[:local_ind], ext_wd[local_ind + len(word):])
                                except re.error:
                                    print(word + '\t\t' + ext_word + '\n')
                                if mod not in mod_list:
                                    mod_list.append(mod)
                                    word_match[mod] = {word}
                                else:
                                    word_match[mod].add(word)
    for mod in mod_list:
        word_count[mod] = len(word_match[mod])
    return mod_list, word_count, word_match


def find_word(txt_file, mod_list, word_list, neg_list):
    """用发现的模式去发现文本中的新词"""

    mod_count = {}
    # 键为发现的模式, 相应的值为匹配到的词的数目
    mod_match = {}
    # 键为发现的模式, 相应的值为匹配到的词的集合
    mod_match_neg = {}
    mod_match_unlabeled = {}
    
    new_word = set()
    # 匹配到的新词的集合
    for mod in mod_list:
        word_set = set()
        for line in txt_file:
            line = trans_punctuation(line)        
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
                                # print (word)
                                # print (file)
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
        
        unlabeled_word = word_set.difference(set(word_list))
        #neg_word_type1 = unlabeled_word.intersection(set(neg_list))       
        #unlabeled_word = unlabeled_word.difference(neg_word_type1)
        neg_word = set([word for word in unlabeled_word if manual_filtration(word, neg_list)])
        
        #neg_word = neg_word_type1.union(neg_word_type2)
        unlabeled_word = unlabeled_word.difference(neg_word)       
        
        mod_match_neg[mod] = neg_word
        mod_match_unlabeled[mod] = unlabeled_word
        
        new_word = new_word.union(unlabeled_word)
        
    # new_word = new_word.difference(set(word_list))
    return new_word, mod_count, mod_match, mod_match_neg, mod_match_unlabeled


def score_mod(mod, word_count, mod_count, mod_match_unlabel):
    """计算模式的评分"""
    p = word_count[mod]
    u = len(mod_match_unlabel[mod])
    t = mod_count[mod]
    return (p / t) * math.log(u + 1, 2) * math.log(p + 1, 2)


def score_word(word, mod_list, word_count, mod_match):
    import math
    m_list = [mod for mod in mod_list if word in mod_match[mod]]
    return sum([math.log(word_count[mod] + 1, 2) for mod in m_list]) / (len(m_list) + 1)


def get_user_dict(txt_path, dic_path, ord_path, dic_type, iter_times=3, inital_lenth_mod=80, 
    lenth_word=50, extend_rate=10, mod_threshold=0.5, word_threshold=1.0):
   
    word_list = get_seed(dic_path, dic_type)
    neg_list = get_neg_list(dic_path, ord_path, dic_type)
    txt_file = get_txt_file(txt_path)

    res = []

    num = 0
    while num < iter_times:
        mod_list, word_count, word_match = find_mod(txt_file, word_list)
        new_word, mod_count, mod_match, mod_match_neg, mod_match_unlabel = find_word(txt_file, mod_list, word_list, neg_list)

        mod_score_list = [score_mod(mod, word_count, mod_count, mod_match_unlabel) for mod in mod_list]

        mod_selected = []
        lenth_mod = inital_lenth_mod + num * extend_rate
        mod_score = list(filter(lambda f: f[1] > mod_threshold, sorted(zip(mod_list, mod_score_list), key=lambda x: x[1], reverse=True)))[:lenth_mod]
        # 模式库是需要每一轮都增加的还是每次都取最好的???????
        mod_selected.extend([x[0] for x in mod_score])
        new_word, mod_count, mod_match, mod_match_neg, mod_match_unlabel = find_word(txt_file, mod_selected, word_list, neg_list)
        word_score_list = [score_word(word, mod_selected, word_count, mod_match) for word in new_word]
        word_score = list(filter(lambda f: f[1] > word_threshold, sorted(zip(new_word, word_score_list), key=lambda x: x[1], reverse=True)))[:lenth_word]
        add_word = [x[0] for x in word_score]
        word_list.extend(add_word)
        res.extend(add_word)

        num += 1

        print("Run time: NO. %d"%num + "\t\tAdd %d words to dictionary"%len(res))

    return res


if __name__ == '__main__':

    txt_path = 'e:/test/病例特点/'
    dic_path = 'C:/Users/yingying.zhu/Documents/dicts'
    ord_path = 'C:/Users/yingying.zhu/Documents/现代汉语常用词表.txt'
    dic_type = 'tutor'
    res = get_user_dict(txt_path, dic_path, ord_path, dic_type)
    with open('C:/Users/yingying.zhu/Desktop/user_dic.txt', 'w', encoding='utf8') as fr:
        fr.write('\n'.join(res))

