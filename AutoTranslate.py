# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json
import os
import csv
import jsonpath
from csv import writer
import sys


# auto	自动检测
# zh	中文
# en	英语
# yue	粤语
# wyw	文言文
# jp	日语
# kor	韩语
# fra	法语
# spa	西班牙语
# th	泰语
# ara	阿拉伯语
# ru	俄语
# pt	葡萄牙语
# de	德语
# it	意大利语
# el	希腊语
# nl	荷兰语
# pl	波兰语
# bul	保加利亚语
# est	爱沙尼亚语
# dan	丹麦语
# fin	芬兰语
# cs	捷克语
# rom	罗马尼亚语
# slo	斯洛文尼亚语
# swe	瑞典语
# hu	匈牙利语
# cht	繁体中文
# vie	越南语


# Korean	                4
# English	                5
# Japanese	                6
# Chinese(Simplified)	    7
# Chinese(Traditional)	    8
# Russian	                9
# German                    10


original_language = 'en'
translate_language = 'fra'
target_row = 5

# Read from file
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

# Read .tsv file
read_from_path = 'your_file.tsv'
with open(read_from_path, 'rt', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    column = [row[target_row] for row in reader]

# Read .csv file
# read_from_path = 'your_file.csv'
# with open(read_from_path, 'rt', encoding='utf8') as f:
#     reader = csv.reader(f, quoting=csv.QUOTE_NONE)
#     column = [row[target_row] for row in reader]

# parse Json


def parse_json(json_data, key_name):
    key_value = jsonpath.jsonpath(
        json_data, '$..{key_name}'.format(key_name=key_name))
    return key_value

# baidu translate api


def baidu_translate_api(content):
    appid = '20200726000526612'  # 填写你的appid
    secretKey = 'rOm0F_8XELe0dbyNw3OY'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = original_language  # 原文语种
    toLang = translate_language  # 译文语种
    salt = random.randint(32768, 65536)
    q = content
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        print(parse_json(result, 'dst'))

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

    return parse_json(result, 'dst')


# Write to file
path = 'results/' + original_language + '_' + \
    translate_language + '_' + 'translation.tsv'

with open(path, 'w', newline="", encoding='utf8') as f:
    csv_write = csv.writer(f, delimiter='\t')
    count = 0
    for content in column:
        if content:
            csv_write.writerow(baidu_translate_api(content))
            count += 1
        else:
            csv_write.writerow('')
            count += 1
        print(str(count) + "/" + str(len(column)))

f.close()
