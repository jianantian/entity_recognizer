def find_mod(path, dic):
    """用字典中的词发现文本模式"""
    file_list = os.listdir(path)
    word_list = read_dict(dic)
    word_count = {}
    #用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
    mod_list = []
    #文本模式以列表形式保存
    word_match = {}
    p = 5
    q = 5
    for file in file_list:
        with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
            txt_file = txt_fr.readlines()       
            #txt_file = modified(txt_fr.read())
        for line in txt_file:
            line = modified(line)
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
                                        #mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(word)+ext_wd[local_ind+len(word):])
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




def find_word(path, mod_list, dic):
    """用发现的模式去发现文本中的新词"""
    file_list = os.listdir(path)
    word_list = read_dict(dic)
    mod_count = {}
    #键为发现的模式, 相应的值为匹配到的词的数目
    mod_match = {}
    #键为发现的模式, 相应的值为匹配到的词的集合
    new_word = set()
    #匹配到的新词的集合
    for mod in mod_list:
        word_set = set()
        for file in file_list:
            with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
                #txt_file = modified(txt_fr.read())
                txt_list = txt_fr.readlines()
            for line in txt_list:
                line = modified(line)         
                left_index = [w.end() for w in re.finditer(mod[0], line)]
                right_index = [w.start() for w in re.finditer(mod[1], line)]
                start = 0
                i, j = 0, 0
                for i in range(len(left_index)):
                    if start < len(right_index):
                        for j in range(start, len(right_index)):
                            if right_index[j] > left_index[i] and (i == len(left_index)-1 or  right_index[j] <= left_index[i+1]):
                                word = line[left_index[i]: right_index[j]]
                                if len(word) < 10:
                                    print (word)
                                    print (file)
                                    word_set.add(word)
                                    start += 1
                                break
                            elif i < len(left_index) - 1 and right_index[j] > left_index[i+1]:
                                break
                            else:
                                start += 1

        #wor_set = wor_set.difference(set(word_list))
        num_extract = len(word_set)
        mod_count[mod] = num_extract
        mod_match[mod] = word_set
        new_word = new_word.union(word_set)
    new_word = new_word.difference(set(word_list))
    return new_word, mod_count, mod_match






    # def find_word(path, mod_list, dic):
#     """用发现的模式去发现文本中的新词"""
#     file_list = os.listdir(path)
#     word_list = read_dict(dic)
#     mod_count = {}
#     #键为发现的模式, 相应的值为匹配到的词的数目
#     mod_match = {}
#     #键为发现的模式, 相应的值为匹配到的词的集合
#     new_word = set()
#     #匹配到的新词的集合
#     for mod in mod_list:
#         wor_set = set()
#         for file in file_list:
#             with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
#                 txt_file = txt_fr.read()
#                 wor_set = wor_set.union(set(re.findall(mod, txt_file)))
#         #wor_set = wor_set.difference(set(word_list))
#         num_extract = len(wor_set)
#         mod_count[mod] = num_extract
#         mod_match[mod] = wor_set
#         new_word = new_word.union(wor_set)
#         new_word = new_word.difference(set(word_list))
#     return  new_word, mod_count, mod_match




# def find_mod(path, dic):
#     """用字典中的词发现文本模式"""
#     file_list = os.listdir(path)
#     word_list = read_dict(dic)
#     word_count = {}
#     #用一个字典保存, key为发现的文本模式, 键值为匹配该模式的词典中的词的数目
#     mod_list = []
#     #文本模式以列表形式保存
#     word_match = {}
#     for file in file_list:
#         with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:          
#             p = 5
#             q = 5
#             txt_file = modified(txt_fr.read())
#             if len(txt_file) > 0:
#                 for word in word_list:
#                     loc_list = [w.start() for w in re.finditer(word, txt_file)]
#                     for loc in loc_list:
#                         for i in range(1, (p+1)):
#                             for j in range(1,(q+1)):
#                                 if loc - i >= 0 and loc + len(word) + j <len(txt_file):
#                                     ext_word = txt_file[loc - i: loc + len(word) + j]
#                                     ext_wd = some_little_modify(ext_word)
#                                     local_ind = ext_wd.index(some_little_modify(word))
#                                     try:
#                                         #mod = re.compile(ext_wd[:local_ind]+'(\S{%d})'%len(word)+ext_wd[local_ind+len(word):])
#                                         mod = (ext_wd[:local_ind], ext_wd[local_ind+len(word):])
#                                     except re.error:
#                                         print (word + '\t\t' + ext_word + '\n')
#                                     if mod not in mod_list:
#                                         mod_list.append(mod)
#                                         word_match[mod] = {word}
#                                     else:
#                                         word_match[mod].add(word)
#     for mod in mod_list:
#         word_count[mod] = len(word_match[mod]) 
#     return mod_list, word_count, word_match


# def find_word(path, mod_list, dic):
#     """用发现的模式去发现文本中的新词"""
#     file_list = os.listdir(path)
#     word_list = read_dict(dic)
#     mod_count = {}
#     #键为发现的模式, 相应的值为匹配到的词的数目
#     mod_match = {}
#     #键为发现的模式, 相应的值为匹配到的词的集合
#     new_word = set()
#     #匹配到的新词的集合
#     for mod in mod_list:
#         wor_set = set()
#         for file in file_list:
#             with open(os.path.join(path, file), 'r', encoding='utf8') as txt_fr:
#                 txt_file = modified(txt_fr.read())

#             left_index = [w.start() for w in re.finditer(mod[0], txt_file)]
#             right_index = [w.start() for w in re.finditer(mod[1], txt_file)]
#             start = 0
#             for i in range(len(left_index)):

#                 for j in range(start, len(right_index)):
#                     if right_index[j] > left_index[i] and right_index[j] <= left_index[i+1]:
#                         word = text_file[left_index[i], right_index[j]]
#                         wor_set.add(word)
#                         start += 1
#                         break
#                     elif right_index[j] > left_index[i+1]:
#                         break
#                     else:
#                         start += 1

#         #wor_set = wor_set.difference(set(word_list))
#         num_extract = len(wor_set)
#         mod_count[mod] = num_extract
#         mod_match[mod] = wor_set
#         new_word = new_word.union(wor_set)
#         new_word = new_word.difference(set(word_list))
#     return new_word, mod_count, mod_match



