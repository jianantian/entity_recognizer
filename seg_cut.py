def seg_cut(text, dicts, max_lenth=5):
    """正向最大匹配法"""
    start = 0
    result = ''
    while start < len(text):
        temp = text[start:]
        end = min(start + max_lenth, len(temp))
        while end > 0:
            sentence = temp[: end]
            print (sentence)
            if sentence not in dicts:
                end -= 1
            else:
                result += sentence + '/'
                start += len(sentence)
                break
    return result



def seg_cut_2(text, dicts, max_lenth = 5):
    """逆向最大匹配法"""
    result = ''
    end = len(text)
    while end > 0:
        temp = text[:end]
        start = max(0, end - max_lenth)
        while start < end:
            sentence = temp[start:]
            if sentence in dicts:
                result = sentence + '/' + result
                end -= len(sentence)
                break
            else:
                start -= 1
    return result


def tagger(sentense, dict_path):
    n = len(sentense)
    bool_mark = [False] * n
    tag_list = []
    for i in range(n, 0, -1):
        for j in range(n-i+1):
            if bool_mark[j] == False and bool_mark[j+i-1]==False:
                temp = sentense[j: j+i]
                if temp in dict_path:
                    tag_list.append(temp)
                    for k in range(j, j+i):
                        bool_mark[k] = True
    return tag_list

