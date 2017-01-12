import logging
import numpy as np
import pypinyin
import re

from pypinyin import lazy_pinyin
from pypinyin import pinyin

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')

def get_pinyin(hans):
    """把汉字转换为对应的拼音, 声调用数字表示, 写在相应的韵母之后"""
    return ''.join(lazy_pinyin(hans, style=pypinyin.NORMAL))


def check_lang(token):
    """检查token是否为英语(包含阿拉伯数字)"""
    lang_pattern=r'^[A-Za-z0-9_]+$'
    return re.search(lang_pattern, token)


def levenshtein(str_1, str_2):
    """计算两个字符串之间的 Levenshtein距离"""
    if not check_lang(str_1):
        str_1 = get_pinyin(str_1)
    if not check_lang(str_2):
        str_2 = get_pinyin(str_2)

    len_1 = len(str_1) + 1
    len_2 = len(str_2) + 1
    tmp_mat= np.zeros((len_1, len_2), dtype=np.int)

    for i in range(1, len_1):
        tmp_mat[i, 0] = i
    for j in range(1, len_2):
        tmp_mat[0, j] = j

    for j in range(1, len_2):
        for i in range(1, len_1):
            if str_1[i-1] == str_2[j-1]:
                tmp_mat[i, j] = tmp_mat[i-1, j-1]
            else:
                tmp_mat[i, j] = min(
                   tmp_mat[i-1, j] + 1,
                   tmp_mat[i, j - 1] + 1,
                   tmp_mat[i-1, j-1] + 1,
                )

    return tmp_mat[-1, -1]

s_1 = '肺'
s_2 = '肺"'
print(get_pinyin('肺"'))
dis = levenshtein(s_1, s_2)
rate = dis/max(len(get_pinyin(s_1)), len(get_pinyin(s_2)))
print(rate)