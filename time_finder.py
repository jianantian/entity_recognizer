import os
import re
import json
import datetime
from datetime import timedelta

def str_sum(iterable):
    res = ''
    for x in iterable:
        res += str(x)
    return res


def num_trans(ch_num):
    """把汉字表示的数字转换成阿拉伯数字"""
    ch_num_list = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '半', '两']
    num_list = [str(num) for num in range(1, 11)]
    num_list.extend(['0.5', '2'])
    trans_table = dict(zip(ch_num_list, num_list))
    return ch_num.translate(trans_table)


def exact_time_trans(s):
    """准确时间点的处理, 把时间词表示成元祖, 分别为年月日"""
    y_re = r'(\d{2,4})年$'
    y_m_re = r'(?<!-|年)(\d{2,4})[年-](\d{1,2})(?:[月-]$|$)'
    y_m_d_re = r'(\d{2,4})[年-](\d{1,2})[月-](\d{1,2})'
    try:
        res = re.search(y_re, s).groups()
        # print('year')
    except AttributeError:
        try:
            res = re.search(y_m_re, s).groups()
            # print('year-month')
        except AttributeError:
            res = re.search(y_m_d_re, s).groups()
            # print('year-month-day')
    return res

def duration_trans(s):

    """ 转换时间段, 结果为timedelata对象, 单位为天
        这里做了简化, 每年默认为365天, 每月默认为30天 """

    y_re = r'((?:\d{1,2})?\.?\d{1,2})\S?年'
    m_re = r'((?:\d{1,2})?\.?\d{1,2})\S?月'
    d_re = r'((?:\d{1,2})?\.?\d{1,2})[天日]'
    w_re = r'(\d{1,2})\S?[周星]'
    s = num_trans(s)
    try:
        y = re.search(y_re, s).group(1)
        res = timedelta(days = 365 * float(y))
    except AttributeError:
        try:
            m = re.search(m_re, s).group(1)
            res = timedelta(days = 30 * float(m))
        except AttributeError:
            try:
                d = re.search(d_re, s).group(1)
                res = timedelta(days = float(d))
            except AttributeError:
                w = re.search(w_re, s).group(1)
                res = timedelta(days = 7 * int(d))
    return res


def find_time(text, date_type):
    import re

    # 提取时间也要以句子为单位, 这样才能比较方便, 只有最后那种某个时间点之后的时间需要用到前一个句子

    #匹配具体时间点, 如2012-09-03, 2014-07-, 2014-07, 2015年08月下旬, 2015年08月, 2015年9月17日, 03年, 2009年
    time_re_1 = r'(?:\d{2,4}[-年])(?:\d{1,2})?[-月]?(?:\d{1,2})?(?:日|号|下旬|上旬|上旬|初|末|中)?(?![前后内余间来])'

    #匹配以病历时间为基准的时间段: 病程 14月余, 病史 30余年, 半个月前, 1个月前, 20年前, 病程一年半
    # 这里的时间与对应的实体都在同一个句子中
    time_re_2 = r'(?<=病(?:史|程))?(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])[前余内来间]?'

    #匹配以病历时间为基准的时间段, 但不是用数字表示: 今, 当日
    time_re_3 = r'[前今昨明次同本去当上][天日月周年]?'

    # 这部分的关键词是 "后"
    #匹配以该文字之前最近的时间点(通常是上一个句子中最晚的时间?)为基准的时间段, 这个时间的作用域到 min(所在句子结束, 下一个时间点)
    # 3天后, 注意这里紧挨着时间之前的词不能是手术以及出院, 入院
    time_re_4 = r'(?<!入院|出院)(?<!术)(?:(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[天日月周年])后'
    patt_7 = r'(?<=手术|入院|出院)后?(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天][内|后]?'
    patt_8 = r'(?<=术)后?(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天][内|后]?'
    pattern_list = [time_re_1, time_re_2, time_re_3, time_re_4]

    pattern = pattern_list[int(date_type) - 1]

    return re.finditer(pattern, text)



# 实体与时间在同一个句子中, 若该句子中不存在任何实体, 则假定对应的实体为症断结果中的疾病, 通常情况下这种类型的时间都是病程xx时间或诊断明确xx时间
# 以 & 相连的实体(原文中为顿号)视作一个实体组合, 一起处理
# 以下都是时间段名次


# 病史类时间在实体之后, 在该时间之前最近的实体或实体组合对应改时间, 时间点为病历时间减去该时间段
# eg: 病史30年
patt_1 = r'(?<=病(?:史|程))近?(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])'

# 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
# eg: 3年来, 近4月前
patt_2 = r'(?<!病(?:史|程))近?(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])以?[前内中来间]'

# 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
# eg: 近3周(之后不是逗号)
patt_3 = r'(?<!病(?:史|程))近(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])以?(?![前内中来间,])'


# 该类型的时间对应的实体在时间之前, 紧挨着, 时间点为病历时间减去该时间段
# eg: 左侧肢体乏力10天
patt_4 = r'(?<!手术|入院|出院)(?<!病(?:史|程))(?<!近|后)(?<![\d年月周日-])(?<!上|下)(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])以?(?![中前后内来间])'

# 该类型的时间对应的实体在时间之前, 紧挨着, 时间点为病历时间减去该时间段
# eg: 左侧胸背部疼痛不适近3月,(后面是标点, 前面不是标点)
patt_5 = r'(?<=\w)(?<!病(?:史|程))近(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d]),'


# 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
# eg: ；近2日,(前后都是标点)
patt_6 = r'(?<!病(?:史|程))近(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d]),'


def get__time(doc_path):
    res = {}
    file_list = os.listdir(doc_path)
    for file in file_list:
        if file.endswith('json'):
            patiend_id = file[:-5] # 病人ID
            res[patient_id] = []
            with open(os.path.join(path, file), 'r', encoding='utf8') as fr:
                doc_dic = json.load(fr)
            for doc_date in doc_dic.keys():
                base_time = datetime.datetime.strptime(doc_date, '%Y%m%d') # 病历时间

                time_list_1 = list(find_time(txt_dic[doc_date], 1))
                for x in time_list_1:
                    event_date_triple = exact_time_trans(x.group())
                    if len(event_date_triple) == 3:
                        event_date = datetime.datetime.strptime(str_sum(event_date_triple), '%Y%m%d')
                    if len(event_date_triple) == 2:
                        event_date = datetime.datetime.strptime(str_sum(event_date_triple), '%Y%m')
                    if len(event_date_triple) == 1:
                        event_date = datetime.datetime.strptime(str_sum(event_date_triple), '%Y')
                    res[patient_id].append((event_date, x.start(), x.end()))
                 # 以上提取文档中所有准确时间点

                time_list_2 = list(find_time(txt_dic[txt_date], 2))
                for x in time_list_2:
                    past_stamp = base_time - duration_trans(x.group(0))
                    resres[patient_id].append((past_stamp, x.start(), x.end()))
                # 以上提取以文档时间为标准的时间段名词, 并计算出相应的时间点
