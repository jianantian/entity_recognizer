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
    ch_num_list.extend(['今', '本', '当', '上', '去', '昨', '次', '同'])
    ch_num_list = [ord(x) for x in ch_num_list]
    nums = [str(x) for x in [0, 0, 0, -1, -1, -1, 1, 0]]
    num_list.extend(nums)
    trans_table = dict(zip(ch_num_list, num_list))
    return ch_num.translate(trans_table)


def str2int(word):
    """注意这个辅助函数是用于把一个分组中的日期里的数值转换成整型数, 默认word种植含有一个数值"""
    try:
        content = re.search(r'\d+', word).group()
        return int(content)
    except TypeError:
        return 1


def triple2date(triple):
    """ 把(year, month, day)的三元组转换为时间
        某个信息不存在时用 None 表示"""
    try:
        res = datetime.date(*map(str2int, triple))
    except ValueError:
        print('illegal date format!')
    return res


def exact_date_trans(s):
    """准确时间点的处理, 把时间词表示成元祖, 分别为年月日, 然后转换为 date """
    """对一些汉字表示的时间进行转化, 如上旬, 下旬, 月初, 上半年等"""
    ch_date_list = ['上半年', '下半年', '上旬', '中旬', '下旬', '年初', '年中', '年末', '年尾', '月初', '月中', '月末', '月尾']
    concrete_date_list = ['3月', '9月', '5日', '15日', '25日', '1月', '6月', '12月', '12月', '月1日', '月15日', '月28日', '月28日']
    for k,v in zip(ch_date_list, concrete_date_list):
        s = s.replace(k, v)
    s = s.replace('月月', '月')
    format_re = r'(\d{4})[-年](\d{1,2})?[-月]?(\d{1,2})?[日号]?'
    s_triple = re.search(format_re, s).groups()
    return triple2date(s_triple)


def duration_trans(s):

    """ 转换时间段, 结果为timedelata对象, 单位为天
        这里做了简化, 每年默认为365天, 每月默认为30天
        s 的格式为 xx 年/月/日/周等 """

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
                res = timedelta(days = 7 * int(w))
    return res


def han_time_trans(word, basetime):
    """ 这里的basetime为病历时间
        把形如 '今年3月' 的时间转换为正常时间对象"""
    y_m_d_re = r'([今本去当])年([0-9]\d?|[一二两三四五六七八九十半]{1,2})?月?([1-9]\d?|[一二两三四五六七八九十半]{1,2})?(?:日|号)?'
    m_d_re = r'([本当上])月((?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})?(?:日|号)?'
    d_re = r'([今昨本当])[日天]'
    w_re = r'([本当上])周(?!期)''
    try:
        y_m_d = re.search(y_m_d_re, word).groups()
        year = basetime.year + int(num_trans(y_m_d[0]))
        y_m_d = (year, ) + y_m_d[1:]
        event_date = triple2date(y_m_d)
    except AttributeError:
        try:
            m_d = re.search(m_d_re, word).groups()
            month = basetime.month + int(num_trans(m_d[0]))
            event_date = triple2date((basetime.year, month, m_d[-1]))
        except AttributeError:
            try:
                d = re.search(d_re, word).groups()
                day = basetime.day + int(num_trans(d[0]))
                event_date = (basetime.year, basetime.month, day)
            except AttributeError:
                w = re.search(w_re, word).groups()
                delta  = timedelta(days = int(num_trans(w[0])) * 7)
                event_date = basetime + delta
    return event_date


def date_without_year_trans(s, basetime):
    """ s 为字符串, 时间点, 不包含年份信息, 如 3月2日 """
    s = num_trans(s)
    format_re = r'(\d{1,2}[月-])?份?(\d{1,2})?[日号]?'
    s_pair = tuple(map(str2int, re.search(s).groups()))
    s_triple = (basetime.year,) + s_pair
    return triple2date(s_triple)


def find_time_expression(text, date_type):
    import re

    # 提取时间也要以句子为单位, 这样才能比较方便, 只有最后那种某个时间点之后的时间需要用到前一个句子

    #匹配具体时间点, 如2012-09-03, 2014-07-, 2014-07, 2015年08月下旬, 2015年08月, 2015年9月17日, 03年, 2009年
    time_re_1 = r'(?<![较年-\d])(\d{4})[-年](\d{1,2})?[-月]?(\d{1,2})?(?:日|号|下旬|上旬|上旬|初|末|中)?(?![前组后内余间])'

    # 实体与时间在同一个句子中, 若该句子中不存在任何实体, 则假定对应的实体为症断结果中的疾病, 通常情况下这种类型的时间都是病程xx时间或诊断明确xx时间
    # 以 & 相连的实体(原文中为顿号)视作一个实体组合, 一起处理
    # 以下都是时间段名次
    #匹配以病历时间为基准的时间段: 病程 14月余, 病史 30余年, 半个月前, 1个月前, 20年前, 病程一年半




    # 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
    # eg: 3年来, 近4月前
    patt_1 = r'(?<!病(?:史|程))(近)?(?<![\d年月周日较-])((?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?(?(1)[年月周日天]|[年月周天])(?![-期年月周日\d]))余?[之以]?[前内中来间]'
    # 需要排除24日来我院呼吸科门诊就诊这种
    # 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
    # eg: 近3周(之后不是逗号)
    patt_2 = r'(?<!病(?:史|程))近(?<![\d年月周日-])((?:\d{1,2}|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[年月周日天])(?![-期年月周日\d])以?(?![前内中来间,])'
    # 该种时间对应的实体在时间之后, 紧挨着, 时间点为病历时间减去该时间段
    # eg: ；近2日,(前后都是标点)
    patt_3 = r'(?:^近|[;,]近)((?:\d{1,2}|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[年月周日天])(?![-期年月周日\d]),'
    duration_patt_1 = [patt_1, patt_2, patt_3]
    time_re_2 = '|'.join(duration_patt_1)

    # 该类型的时间对应的实体在时间之前, 紧挨着, 时间点为病历时间减去该时间段
    # 病史类实体在时间词之前, 在该时间之前最近的实体或实体组合对应该时间, 时间点为病历时间减去该时间段
    # eg: 病史30年
    patt_4 = r'(?<=病(?:史|程))近?(?<![\d年月周日-])((?:\d{1,2}|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[年月周日天])(?![-期年月周日\d])'
    # eg: 左侧肢体乏力10天
    patt_5 = r'(?<=\w|")(?<!手术|入院|出院)(?<!病(?:史|程))(?<![\d年月周日-])(?<![近后上下于在])约?((?:\d{1,2}|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[年月天日周])(?![-期年月周日\d])(?![之中来份前后内间])(?!余前|以来)(?!余之前)'
    # eg: 左侧胸背部疼痛不适近3月,(后面是标点, 前面不是标点)
    patt_6 = r'(?<=\w|")(?<!病(?:史|程))近(?<![\d年月周日-])((?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[年月周日天]),'
    duration_patt_2 = [patt_4, patt_5, patt_6]
    time_re_3 = '|'.join(duration_patt_2)

    #匹配以病历时间为基准的时间段, 但不是用数字表示: 今, 当日
    time_re_4 = r'[今本去当上昨][天日月周年](?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})?[月日号]?(?:[1-9]\d?|[一二两三四五六七八九十半]{1,2})?(?:日|号)?'


    # 时间点, 但是没有年份信息, 对应的实体在时间名词之后, 年份信息应该从该词之前最近的时间获得
    # 9月30日
    patt_7 = r'(?<![a-zA-Z第较年\d-])(?:\d{1,2}|[一二两三四五六七八九十半]{1,2})[月-](?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})[日号-]?(?![\d点组口次时分秒])'
    # 4月份
    patt_8 = r'(?<![年\d近程史-])([0-9]\d?|[一二两三四五六七八九十半]{1,2})月份'
    # 患者于2月无明显诱因下出现咳嗽&咳痰
    patt_9= r'(?<=于|在)([1-9]\d?|[一二两三四五六七八九十半]{1,2})[月日号](?![\d前份中间后余])'
    # 25日患者面部浮肿
    patt_10= r'(?:(?<=^)|(?<=,|;))([0-9]\d?|[一二两三四五六七八九十半]{1,2})[月日号](?!以来)(?![\d近中前间份后余])'
    uncomplete_date = [patt_7, patt_8, patt_9, patt_10]
    time_re_5 = '|'.join(uncomplete_date)


    # 这部分的关键词是 "后", 得到具体时间的方法都是基准时间加上该时间词表示的时间
    # 匹配以该文字之前最近的时间点(通常是上一个句子到本句子该词出现之前这一段中最晚的时间?)为基准的时间段, 这个时间的作用域到 min(所在句子结束, 下一个时间点)
    # 3天后, 注意这里紧挨着时间之前的词不能是手术以及出院, 入院
    patt_11 = r'(?<!入院|出院)(?<!术)(?:(?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[天日月周年])[后内]'
    patt_12 = r'(?<!入院|出院)(?<!术)后(?:(?:[0-9]\d?|[一二两三四五六七八九十半]{1,2})(?:十)?[余多几]?[个]?[天日月周年])'
    after_patt_1 = [patt_11, patt_12]
    time_re_6 = '|'.join(after_patt_1)



    # 时间的基准点为手术, 入院, 出院时间, 加上这里的时间段, 该时间先从表里查, 要注意病例周期
    patt_13 = r'(?<=手术|入院|出院)后?(?:[0-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天][内|后]?'
    # 时间的基准点为相应手术时间, 加上这里的时间段
    patt_14 = r'(?<=术)[以之]?后?(?:[0-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天][之以]?[内后]?'

    pattern_list = [time_re_1, time_re_2, time_re_3, time_re_4, time_re_5, time_re_6]

    pattern = pattern_list[int(date_type) - 1]

    return re.finditer(pattern, text)



def get_time(doc_path):
    res = {}
    file_list = os.listdir(doc_path)
    for file in file_list:
        if file.endswith('json'):
            patiend_id = file[:-5] # 病人ID
            res[patient_id] = {}
            with open(os.path.join(path, file), 'r', encoding='utf8') as fr:
                doc_dic = json.load(fr)
            for doc_date in doc_dic.keys():
                res[patient_id][doc_date] = []
                doc_time = datetime.datetime.strptime(doc_date, '%Y%m%d') # 病历时间
                doc_file = txt_dic[txt_date]

                time_list_1 = find_time_expression(doc_file, 1)
                for x in time_list_1:
                    event_date = exact_date_trans(x.group())
                    res[patient_id][doc_date].append((event_date, x.start(), x.end()))
                 # 以上提取文档中所有准确时间点, 即包含完整年份的信息, 作用域在时间词之后, 为 x.end() 到下一个时间词的开始位置, 即 x.next().start()

                time_list_2 = find_time_expression(doc_file, 2)
                for x in time_list_2:
                    past_stamp = doc_time - duration_trans(x.group())
                    res[patient_id][doc_date].append((past_stamp, x.start(), x.end()))
                # 以上提取以文档时间为标准的时间段,并计算出相应的时间点 , 作用域在时间词之后, 为 x.end() 到下一个时间词的开始位置, 即 x.next().start()

                time_list_3 = find_time_expression(doc_file, 3)
                for x in time_list_3:
                    after_stamp = doc_time - duration_trans(x.group())
                    res[patient_id][doc_date].append((after_stamp, x.start(), x.end()))
                # 以上提取以文档时间为标准的时间段,并计算出相应的时间点 , 作用域在时间词之前, 为上一个时间词的结束位置, 即 x.pre().end(), 到本词的开始位置x.start()

                time_list_4 = find_time_expression(doc_file, 4)
                for x in time_list_4:
                    event_date = han_time_trans(x.group(), doc_time)
                    res[patient_id][doc_date].append((event_date, x.start(), x.end()))
                # 以上提取以文档时间为基准, 时间以汉字表示, 如今年, 作用域在时间词之后, 为 x.end() 到下一个时间词的开始位置, 即 x.next().start()

                time_list_5 = list(find_time_expression(doc_file, 5))
                for x in time_list_5:
                    pre_time_list = filter(lambda f: f[-1] < x.end(), res[patient_id][doc_date])
                    pre_time_list = sorted(pre_time_list, key=lambda f: f[-1])
                    basetime = pre_time_list[-1]
                    event_date = date_without_year_trans(x.group(), basetime)
                    res[patiend_id][doc_date].append((event_date, x.start(), x.end()))
                # 以上提取没有年份信息的时间点, 如3月19日, 作用域在时间词之后, 为 x.end() 到下一个时间词的开始位置, 即 x.next().start()

                time_list_6 = list(find_time_expression(doc_file, 6))
                for x in time_list_6:
                    pre_time_list = filter(lambda f: f[-1] < x.end(), res[patient_id][doc_date])
                    pre_time_list = sorted(pre_time_list, key=lambda f: f[-1])
                    basetime = pre_time_list[-1]
                    event_date = basetime + duration_trans(x.group())
                    res[patiend_id][doc_date].append((event_date, x.start(), x.end()))
                # 以上提取 3月后 这一类的时间信息, 作用域在时间词之后, 为 x.end() 到下一个时间词的开始位置, 即 x.next().start()
