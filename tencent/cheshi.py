import requests
from lxml import etree
import json
import re
import math
import time
import ast
import random



headers_two = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'Province=021; City=021; UM_distinctid=167167e03cf21d-06e10e6c7b740a-414f0120-15f900-167167e03d01bd; vjuids=-557de2078.167167e08f2.0.7347b06fe51a6; _ntes_nnid=6252d0d97812437a4b7ff6217cedcc48,1542270617849; _ntes_nuid=6252d0d97812437a4b7ff6217cedcc48; _antanalysis_s_id=1542270618187; __gads=ID=cc3983f5cdda3076:T=1542270617:S=ALNI_MagAFZ2moSoB4SrPD4W8Cnd9aa93Q; NNSSPID=71084a74668d496db04b9be5eaa98a1f; ne_analysis_trace_id=1542345088187; pgr_n_f_l_n3=534cfd2536f3668a15423559003332052; vjlast=1542270618.1542335885.13; vinfo_n_f_l_n3=534cfd2536f3668a.1.9.1542270617858.1542357144579.1542357875424; s_n_f_l_n3=534cfd2536f3668a1542357867492',
    'Host': 'comment.api.163.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}

# url ='http://comment.tie.163.com/E0SORIJT0008856S.html'
#
#
# item = {}
# print(url)
# respnse = requests.get(url)
# data = respnse.content.decode()
# count = re.search('"tcount":\d{0,10}', data).group(0)
# print(count)


# url = 'http://www.yidianzixun.com/article/0Kdq538w'
# item = dict()
# response = requests.get(url)
# data = response.text
# print(data)
# data = re.findall(r'var url = "[\s\S]*vivobrowser', data)[0]
# data = data.split('"')[1]
# print(data)

from datetime import datetime, date, timedelta

yesterday = date.today() + timedelta()
print(yesterday)
