# -*- encoding: utf-8 -*-
import locale
import re
from datetime import datetime
from collections import defaultdict


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
        new_list=[item[1][0] for item in d_sorted_by_value[:5]]

    if slow_queries:
        for m in dict_log.keys():
            dict_log[m][2]=dict_log[m][1]//dict_log[m][0]
        d_sorted_by_value = sorted(dict_log.items(), key=lambda x: x[1][2],reverse=True)
        new_list=[]
        if dict_log:
            new_list=[item[1][2] for item in d_sorted_by_value[:5]]
            return new_list

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

    dict_log= defaultdict(lambda:[0,0,0])
    f = open('log.log')
    for line in f:
        date_time = re.findall(r'(\d{2}/\b\w{3}\b/\d{4} \d{2}:\d{2}:\d{2})',line)
        date_time_str=str(date_time)
        if date_time:
            date_inline=datetime.strptime(date_time_str[2:22], '%d/%b/%Y %H:%M:%S')
            if start_at:
                start_date=datetime.strptime(start_at, '%d/%b/%Y %H:%M:%S')
                if date_inline<start_date:continue
            if stop_at:
                stop_date=datetime.strptime(stop_at, '%d/%b/%Y %H:%M:%S')
                if date_inline>stop_date:continue
            
            result_first = re.split(r'["]', line)
            result_second = re.split(r'[\s]', result_first[1])
            if request_type and not result_second[0]==str(request_type):continue
            result_line_one = re.split(r'//', result_second[1])
            result_line=result_line_one[1]
            
            if '?' in result_line:
               result_line_two = re.split(r'\?.*', result_line)
               result_line=result_line_two[0]

            word = re.findall(r'\w+$', line)
            
            if ignore_files:
                str_split = re.split(r'[.]', result_line)
                result_third=str_split.pop()
                if 0<len(result_third)<4:continue

            if ignore_www and result_line[0:4]=='www.':
                result_forth = re.search(r'www.', result_line)
                if result_forth:
                    result_line_three = re.split(r'www.', result_line)
                    result_line=result_line_three[1]
               
            if ignore_urls:
                for j in range(len(ignore_urls)):
                    if '?' in ignore_urls:
                        line_url = re.split(r'\?.*', ignore_urls)
                        result_line_url=line_url[0]
                    if result_line_url[-1]=='/':
                        result_line_url=result_line_url[:-1]
                    if result_line==result_line_url:continue

            if result_line[-1]=='/':
                result_line=result_line[:-1]

            if result_line:
                    dict_log[result_line][0]+=1
                    dict_log[result_line][1]+=int(word[0])

    f.close()
    
    return dict_log

