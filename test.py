import pypinyin
from pypinyin import pinyin, lazy_pinyin
import numpy as np
import re
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')

def get_pinyin(hans):
    """把汉字转换为对应的拼音, 声调用数字表示, 写在相应的韵母之后"""
    return ' '.join(lazy_pinyin(hans, style=pypinyin.TONE2))

print(get_pinyin('中心'))

def check_lang(token):
    """检查token是否为英语(包含阿拉伯数字)"""
    num = len(token)
    lang_pattern=r"\w{%d}"%num
    return re.search(lang_pattern, token)


def levenshtein(str_1, str_2):
    """计算两个字符串之间的Levenshtein距离"""

    if not check_lang(str_1):
        str_1 = get_pinyin(str_1)
    if not check_lang(str_2):
        str_2 = get_pinyin(str_2)

    print(str_1)
    print(str_2)


    len_1 = len(str_1) + 1
    len_2 = len(str_2) + 1
    tmp_mat= np.zeros((len_1, len_2), dtype=np.int)

    print(tmp_mat.shape)

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

s_1 = '中国'
s_2 = '国家'
dis = levenshtein(s_1, s_2)
print(dis)
print(check_lang(s_1))