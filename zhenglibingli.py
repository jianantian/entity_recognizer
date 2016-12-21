import os
import shutil
import json
import re

path = 'E:/nanzong_json'

for file in os.listdir(path):
    filename = os.path.join(path, file)
    with open(filename, 'r', encoding='utf8') as fr:
        data = json.load(fr)
    patient_id = data['ID']
    #print (str(type(patient_id)) + filename)
    try:
        dir_name = os.path.join('E:/huizong',patient_id)
        #print (dir_name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        shutil.move(filename,dir_name)
    except TypeError:
        doc_name = data['Doc']
        get_id = r'(\w+)_(\S+)'
        patient_id = re.match(get_id, doc_name).group(1)
        dir_name = os.path.join('E:/huizong',patient_id)
        #print (dir_name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        shutil.move(filename,dir_name)
