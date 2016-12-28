import json
import os
import shutil


def extrac_part(data_type, text_type):
    """从病例中提取特定类型的文本, 如病例特点, 病史等"""
    if data_type == '测试':
        path = 'E:/new/test_100'
    elif data_type == '训练':
        path = 'E:/new/train_2157'
    elif data_type == '调参':
        path = 'E:/new/para_50'

    dise_path = os.path.join('e:/', text_type)
    if not os.path.exists(dise_path):
        os.mkdir(dise_path)

    patient_list = os.listdir(path)

    for patient in patient_list:
        if patient != text_type:
            filename = os.path.join(dise_path, patient + '.txt')
            dise_char = open(filename, 'a+', encoding='utf8')
            #dise[patient] = []
            dir_name = os.path.join(path, patient)
            file_list = os.listdir(dir_name)
            for filename in file_list:
                ext = os.path.splitext(filename)[-1]
                if ext == '.json':
                    with open(os.path.join(dir_name, filename), 'r', encoding='utf8') as fr:
                        #print(os.path.join(dir_name, filename))
                        doc = json.load(fr)
                    for content in doc['Data']:
                        if text_type in content.keys():
                            if content[text_type] not in dise_char.read():
                                dise_char.write(content[text_type])
                else:
                    pass
            dise_char.close()


def split_doc(path):
    """把相应的文本分割成句子, 每句一行"""
    import os
    path_name = os.path.split(path)[1] + '_split'
    path_split = os.path.join(os.path.split(path)[0], path_name)
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf8') as txt_fr:
            txt_list = [line.strip() for line in txt_fr.read().split('。') if line.strip() !='']
        with open(os.path.join(path_split,filename), 'w+', encoding='utf8') as fr:
            for line in txt_list:
                fr.write(line + '\n')


def check_empty(path):
    """检查相应位置的空文档, 计数, 并输出空文档名, 便于调整"""
    empty_list = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r', encoding='utf8') as txt_fr:
            txt_file = txt_fr.read()
        if len(txt_file) == 0:
            empty_list.append(filename)
    return len(empty_list), empty_list


#类型可以选测试, 训练或调参
data_type = '训练'

text_type = '病例特点' 
#有两个文件这一部分的名字是'病史特点'


#extrac_part(data_type, text_type)

path = 'e:/train/病例特点'
num, l = check_empty(path)
print (l)