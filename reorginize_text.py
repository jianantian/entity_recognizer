import os
import json
import re
from functools import reduce


def trans_punctuation(word):
    # 去掉字符串中的\xa0, 以免报错
    # 文档中中文标点与英文混用, 把句子中的标点替换为半角, 句号不转换, 便于和小数点区分, 用于断句
    word = word.replace('\xa0', '')
    trans_table= str.maketrans('，：“”（）；、',',:""();&')
    word = word.translate(trans_table)
    return word


def extrac_part(data_type, text_type):
    """从病例中提取特定类型的文本, 如病例特点, 病史等
        每一个病人的资料保存在一个json文件中, key值为相应的病历时间"""

    date_match = r'\d+_\d+-\d+_(\d{8})\d+_\d+\.html'

    if data_type == '测试':
        path = 'E:/new/test_100'
        rel_dir = 'test'
    elif data_type == '训练':
        path = 'E:/new/train_2157'
        rel_dir = 'train'
    elif data_type == '调参':
        path = 'E:/new/para_50'
        rel_dir = 'para'

    out_path = os.path.join('e:/', rel_dir+'/'+text_type)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    patient_list = os.listdir(path)

    for patient in patient_list:
        text_dir = {}
        dir_name = os.path.join(path, patient)
        file_list = os.listdir(dir_name)
        for filename in file_list:
            ext = os.path.splitext(filename)[-1]
            with open(os.path.join(dir_name, filename), 'r', encoding='utf8') as fr:
                doc = json.load(fr)                    
            for content in doc['Data']:
                if text_type in content.keys():
                    raw_date = doc['Doc']
                    text_date = re.search(date_match, raw_date).group(1)
                    text_dir[text_date] = trans_punctuation(content[text_type])
        text_to_write = json.dumps(text_dir, ensure_ascii=False, indent=4, sort_keys = True)
        out_name = os.path.join(out_path, patient + '.json')
        with open(out_name, 'w', encoding='utf8') as out_text:
            out_text.write(text_to_write)


def check_empty(path):
    """检查相应位置的空文档, 计数, 并输出空文档名, 便于调整"""
    empty_list = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf8') as txt_fr:
            txt_file = txt_fr.read()
        if len(txt_file) == 0:
            empty_list.append(filename)
    return len(empty_list), empty_list

def main():
    data_type = '测试'
    text_type = '病例特点' 
    #某些病历这部分的命名为病史特点
    extrac_part(data_type, text_type)

if __name__ == '__main__':
    main()
    