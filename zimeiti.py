import requests
import json
from lxml import etree
import time
import re
import json

import random
# 自定义爬取结束时间2018-10-30
END_TIME = '2018-9-1'
START_TIME = '2018-10-1'


# https://api.auto.ifeng.com/cms/api/amop?page=1&pageCount=10
page_num = 400
headers = {
        'Content-Encoding': 'gzip',
        'Content-Type': 'text/html',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=1643f2ba7392b6-030d9d8d1f840d-5b183a13-1fa400-1643f2ba73a3df; userid=1530068184693_q6fx2d508; vjuids=6be57a31a.1643f2cbf83.0.f86a88054c9c4; vjlast=1530068255.1530068255.30; prov=cn021; city=021; weather_city=sh; region_ip=58.246.74.194; region_ver=1.30; ifengRotator_iis3=6; ifengRotator_AP7057=0; ifengRotator_AP612=0; ifengRotator_Ap1528=0; ifengWindowCookieNameauto=1; auto_iploc=310000; auto_vlast=1541571206908; Hm_lvt_54fd6abfd2724514f20f3ead650f95b1=1541571207; Hm_lpvt_54fd6abfd2724514f20f3ead650f95b1=1541571207; _ga=GA1.2.1235343235.1541571207; _gid=GA1.2.1365747240.1541571207; user_module=%2Cgroup_buy%2Cdynamic%2Cindustry%2Ccomment%2Cparlor',
        'Host': 'auto.ifeng.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
start_url = 'https://auto.ifeng.com'


def get_html(url):
    html = requests.get(url, headers=headers)
    print(html.status_code)
    code = html.status_code
    new_data = etree.HTML(html.content.decode())
    return new_data, code

url_list = []
break_flag = False
while page_num < 1000:
    url = 'https://api.auto.ifeng.com/cms/api/amop?page=%s&pageCount=10' % page_num
    page_num += 1
    data = requests.get(url)
    try:
        data = json.loads(data.text)
        data_list = data['data']
        print(data_list)
        print(url)
        relist = []

        for alist in data_list:
            title = alist['title']
            createtime = alist['createtime']
            data = createtime.split(" ")[0]
            get_time = time.mktime(time.strptime(data, "%Y-%m-%d"))
            start_time = time.mktime(time.strptime(START_TIME, "%Y-%m-%d"))
            if END_TIME != '':
                end_time = time.mktime(time.strptime(END_TIME, "%Y-%m-%d"))
            else:
                end_time = time.mktime(time.strptime('2100-1-1', "%Y-%m-%d"))
            if float(get_time) < float(end_time):
                # self.crawler.engine.close_spider(self, '爬虫终止')
                print(data)
                # break_flag = True
                break
            if float(end_time) <= float(get_time) <= float(start_time):
                print(createtime)
                one_new_url = alist['url']
                url = start_url + one_new_url
                url_list.append(url)
    except:
        print("json数据错误")
    if break_flag:
        break
print(len(url_list),'数据数')
float_num = 100
click_num = 1
item = {}

filename = open('./zimeiti9yue.json', 'wb')

jishu = 1
for url in url_list:
    try:
        new_data, code = get_html(url)
        print(url)
        if code == 200:
            click_num += 1
            float_num += 1
            # url
            item['url'] = url
            # 标题
            item[u'title'] = new_data.xpath('.//div[1]/h3/span/text()')[0]
            # 网站
            item[u'platform'] = '凤凰网汽车'
            # 来源
            try:
                item[u'source'] = new_data.xpath('.//*[@id="source_baidu"]/a/text()')[0]
            except:
                item[u'source'] = ''
            # 作者
            # try:
            #     item[u'author'] = new_data.xpath('.//*[@id="author_baidu"]/text()')[0]
            # except:
            #     item[u'author'] = ''
            # 内容
            content = new_data.xpath('.//div[1]/div[@class="arl-c-txt"]/p/text()')
            item[u'content'] = ''.join(content)
            # 日期
            data_all = new_data.xpath('.//*[@id="pubtime_baidu"]/text()')[0]
            data = data_all.split(' ')[0]
            data = re.sub("年", '-', data)
            data = re.sub('月', '-', data)
            data = re.sub('日', '', data)
            item[u'data'] = data
            # 时间
            item[u'time'] = data_all.split(' ')[1]
            # 关键字
            item[u'keyword'] = ''
            # 评论数
            try:
                item[u'comments_count'] = new_data.xpath('.//*[@id="comments"]/div[1]/div[1]/div[2]/div[2]/text()')[0]
            except:
                item[u'comments_count'] = ''
            # 点赞数
            try:
                item[u'like'] = new_data.xpath('.//*[@id="comments"]/div[1]/div[1]/div[2]/div[1]/text()')[0]
            except:
                item[u'like'] = ''

            text = json.dumps(dict(item), ensure_ascii=False) + ',\n'
            print("正在写入第%s条数据" % jishu)
            jishu += 1
            filename.write(text.encode('utf-8'))
    except:
        print('爬取数据失败', url)

filename.close()
print('爬取完毕，成功爬取到%s条数据' % str(jishu))

