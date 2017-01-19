import os
import re

def reconstruct_bodypart(path):
    """对身体部位名词进行重组, 前面加上适当的方位词"""
    direction = r'[左右]?[上下前后]?[半侧]?(\S+)'
    direc_type_1 = ['侧', '半', '']
    direc_type_2 = ['上', '下', '前', '后', '']
    direc_type_3 = ['左', '右', '']
    direc_list = []
    for a in direc_type_3:
        for b in direc_type_2:
            for c in direc_type_1:
                direc_list.append(a + b + c)
    direc_list.extend(['两', '双', '两侧', '双侧'])

    with open(path, 'r', encoding='utf8') as fr:
        word_list = fr.readlines()
    root_word_list = [re.search(direction, word.split('\t')[0]).group(1) for word in word_list if not re.search(r'^两|双', word)]

    with open(os.path.join(os.path.split(path)[0], 'new_bodypart.txt'), 'w', encoding='utf8') as new_fr:
        for direc in direc_list:
            for word in root_word_list:
                new_fr.write(direc + word + '\n')
    print('Finish writing!')


def check(filename):
    """检查并删除词典中的重复词"""
    import os
    import shutil
    mark = 0
    new = []
    with open(filename, 'r', encoding='utf8') as fr:
        for word in fr.readlines():
            if word not in new:
                new.append(word)
            else:
                mark += 1
    if mark != 0:
        name = os.path.split(filename)[1]
        shutil.move(filename, os.path.join('e:/词典备份', filename))
        new_file = open(filename, 'w', encoding='utf8')
        new_file.write(''.join(new))
        new_file.close()
        print('Bingo!')
    else:
        print('没有重复!')


path = 'C:/Users/yingying.zhu/Documents/dicts/bodypart.txt'
reconstruct_bodypart(path)
check(os.path.join(os.path.split(path)[0], 'new_bodypart.txt'))