from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import re
import json
import ast
import HTMLParser
from xml.sax.saxutils import unescape
from lxml import etree

# browser = webdriver.Chrome()  # Get local session of Chrome
# # browser.set_window_size(1000,30000)
# browser.get("https://www.toutiao.com/ch/news_car/")  # Load page
# time.sleep(5)
# # browser.execute_script("window.scrollBy(0,1000)")
# # js="window.scrollTo(0,document.body.scrollHeight)"
# # browser.execute_script(js)
# for i in range(10000):
#     ActionChains(browser).key_down(Keys.DOWN).perform()
#
# time.sleep(2)

url = 'https://www.toutiao.com/a6615079328390578702/'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'tt_webid=6628733243796178436; tt_webid=6628733243796178436; csrftoken=3a6f2dc0f315bd1fe957319a75bba4ed; uuid="w:2203d39caf3249c0bcda19ee5839b850"; UM_distinctid=1675827673a27a-0dd556679b3f63-3a3a5d0c-15f900-1675827673b22c; __tasessionId=qb2c0x9mb1543386267822; CNZZDATA1259612802=992935523-1543369669-%7C1543385869',
    'referer': 'https://www.toutiao.com/ch/news_car/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
response = requests.get(url, headers=headers)
data_all = response.content.decode()
print(data_all)
data = re.search(r"articleInfo: {([\s\S]*time: '\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", data_all).group(1)
data = '{' + data + "'}}"
print(data)
data = re.sub('\n', '', data)
data = unescape(data)
data = data.replace('&quot;', '"').replace('&#x3D;', '=')
content = re.search('content: ([\s\S]*)groupId',data).group(1).strip()[1:][:-2]
content = etree.HTML(content)
text = content.xpath('.//p//text()')
text_con = ''.join(text)
date, create_time = re.search('(\d{4}-\d{1,2}-\d{1,2}) (\d{1,2}:\d{1,2}:\d{1,2})', data).group(1, 2)
id_num = re.search("groupId: '(\d{1,50}).*itemId", data).group(1)
source = re.search("source: '(.*)time", data).group(1).strip()[:-2]
comment_count = re.search("commentCount: '(\d{0,10})[\s\S]*ban_comment", data_all).group(1)



