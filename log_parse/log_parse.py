# -*- encoding: utf-8 -*-
import locale
import re
from datetime import datetime

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    dict_log=parse_file(ignore_files,
                        ignore_urls,
                        start_at,
                        stop_at,
                        request_type,
                        ignore_www,
                        slow_queries)
    new_list=[]
    if dict_log:
        d_sorted_by_value = sorted(dict_log.items(), key=lambda x: x[1][0],reverse=True)
        for k in range(5):
            new_list.append(d_sorted_by_value[k][1][0])

    if slow_queries:
        for m in dict_log.keys():
            dict_log[m][2]=dict_log[m][1]//dict_log[m][0]
        d_sorted_by_value = sorted(dict_log.items(), key=lambda x: x[1][2],reverse=True)
        new_list=[]
        if dict_log:
            for k in range(5):
                new_list.append(d_sorted_by_value[k][1][2])
            list_time=new_list
            return list_time

    return new_list

def parse_file(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    dict_log={}
    f = open('log.log')
    for line in f:
        date_time = re.findall(r'(\d{2}/\b\w{3}\b/\d{4}) \d{2}:\d{2}:\d{2}',line)
        date_time_str=str(date_time)
        if date_time:
            date_inline=datetime.strptime(date_time_str[2:13], '%d/%b/%Y').date()
            if start_at:
                start_date=datetime.strptime(start_at, '%d/%b/%Y').date()
                if date_inline<start_date:continue
            if stop_at:
                stop_date=datetime.strptime(stop_at, '%d/%b/%Y').date()
                if date_inline>stop_date:continue
            
            result_first = re.split(r'["]', line)
            result_second = re.split(r'[\s]', result_first[1])
            if request_type and not result_second[0]==str(request_type):continue
            result_line = re.split(r'//', result_second[1])
            
            if ignore_urls:
                for j in range(len(ignore_urls)):
                    if result_line[1]==ignore_urls:continue
        
            word= re.findall(r'\w+$', line)
            
            if ignore_files:
                str_split = re.split(r'[.]', result_line[1])
                result_third=str_split.pop()
                if result_third=='jpg' or result_third=='png' or result_third=='gif' or result_third=='js':continue

            if ignore_www and result_line[1][0:4]=='www.':
                result_forth = re.search(r'www.', result_line[1])
                if result_forth:
                    result_line = re.split(r'www.', result_line[1])
            
            if result_second[1]:
                if dict_log.setdefault(result_line[1]):
                    dict_log[result_line[1]][0]=dict_log[result_line[1]][0]+1
                    dict_log[result_line[1]][1]=dict_log[result_line[1]][1]+int(word[0])
                else:dict_log[result_line[1]]=[1,int(word[0]),0]
    f.close()

    return dict_log

