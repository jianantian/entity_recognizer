import json
import os
import shutil

#类型可以选测试, 训练或调参
data_type = '测试'

text_type = '病例特点'

if data_type = '测试':
    path = 'E:/new/test_100'
elif data_type = '训练':
    path = 'E:/new/train_2157'
elif data_type = '调参':
    path = 'E:/new/para_50'

dise_path = os.path.join(path, text_type)
if not os.path.exists(dise_path):
    os.mkdir(dise_path)

patient_list = os.listdir(path)

for patient in patient_list:
    if patient != text_type:
        filename = os.path.join(dise_path, patient + '.txt')
        dise_char = open(filename, 'a+', encoding='utf8')
        dise[patient] = []
        dir_name = os.path.join(path, patient)
        file_list = os.listdir(dir_name)
        for filename in file_list:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                with open(os.path.join(dir_name, filename), 'r', encoding='utf8') as fr:
                    print(os.path.join(dir_name, filename))
                    doc = json.load(fr)
                for content in doc['Data']:
                    if text_type in content.keys():
                        if content[text_type] not in dise_char.read():
                            dise_char.write(content[text_type])
            else:
                pass
        dise_char.close()