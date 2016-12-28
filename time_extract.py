
def find_exact_time(text):
    """从文本中发现确切表述的时间, 如2012-09-03   2014-07-  2014-07 2015年08月下旬  2015年08月    2015年9月17日, 并不提取表示时间段的词语, 如三月前等"""
    import re
    #匹配具体时间点, 如2012-09-03, 2014-07-, 2014-07, 2015年08月下旬, 2015年08月, 2015年9月17日, 03年, 2009年
    time_re_1 = r'\d{2,4}[-年](?:\d{1,2})?[-月]?(?:\d{1,2})?(?:日|号|下旬|上旬|上旬|初|末|中)?'

    #匹配以病历时间为基准的时间段: 病程 14月余, 病史 30余年, 半个月前, 1个月前, 20年前, 病程一年半
    #这里的时间可能并不全是以病历时间为基准, 如手术后6日
    #可能需要分一分类
    time_re_2 = r'(?:病(?:史|程))?(?<![\d年月周日-])(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[年月周日天](?![-期年月周日\d])[前余内]?'

    #匹配以病历时间为基准的时间段, 但不是用数字表示: 今, 当日
    time_re_3 = r'[前今昨明次同本去当上][天日月周年]?'

    #匹配以该文字之前最近的时间点为基准的时间段: 3天后
    tmie_re_4 = r'(?:(?:[1-9]\d?|[一二两三四五六七八九十半])(?:十)?[余多几]?[个]?[天日月周年])后'
    
    return re.findall(time_re, text)
    