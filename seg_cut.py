def seg_cut(text, dicts, max_lenth=5):
    """正向最大匹配法"""
    start = 0
    result = ''
    while start < len(text):
        temp = text[start:]
        end = min(start + max_lenth, len(temp))
        while end > 0:
            sentence = temp[: end]
            print(sentence)
            if sentence not in dicts:
                end -= 1
            else:
                result += sentence + '/'
                start += len(sentence)
                break
    return result


def seg_cut_2(text, dicts, max_lenth=5):
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
