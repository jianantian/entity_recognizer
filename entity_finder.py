import get_tutor
""""""
from pprint import pprint


def tagger(sentense, dic):
    """用 dic 中的词来匹配文本中的实体"""
    n = len(sentense)
    bool_mark = [False] * n
    tag_list = []
    for i in range(n, 0, -1):
        for j in range(n - i + 1):
            if bool_mark[j] is False and bool_mark[j + i - 1] is False:
                temp = sentense[j: j + i]
                if temp in dic:
                    tag_list.append((temp, j, j + i - 1))
                    for k in range(j, j + i):
                        bool_mark[k] = True
    return tag_list


if __name__ == "__main__":
    txt_path = 'e:/test/病例特点/'
    dic_path = 'C:/Users/yingying.zhu/Documents/dicts'
    dic_type = 'tutor'
    dic = get_tutor.get_seed(dic_path, dic_type)
    txt_file = get_tutor.get_txt_file(txt_path)
    x = []
    for sent in txt_file:
        x.extend(tagger(sent, dic))
    pprint(x)
