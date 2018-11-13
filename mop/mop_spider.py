import requests
from lxml import etree
import json
import re
import math
import time
import ast

class MopSpider(object):
    def __init__(self):
        self.start_url = 'http://autoapi.dftoutiao.com/mopsearch_h5/searchnews?jsonpcallback=jQuery18309647992932972742_1541999181929&keywords=%25E5%25AE%259D%25E9%25A9%25AC&stkey_zixun=&lastcol_zixun={}&splitwordsarr=&stkey_video=&lastcol_video=&maintype=&domain=mopauto_pc&os=Win7&qid=&recgid=15417568671858769&_=1541999185686'
        # 获取数据接口的headers
        self.headers_one = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'autoapi.dftoutiao.com',
            'Referer':'http://auto.mop.com/search-models.html?query=%E5%AE%9D%E9%A9%AC',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        # 获取新闻详情页的headers
        self.headers_two = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'mopauto_uid=15417568671858769; _mc=m-1541756833719532435; BDTUJIAID=23ededdadee3798fd3cfff3b5345490d; localCity=%E4%B8%8A%E6%B5%B7; cityname=%E4%B8%8A%E6%B5%B7; _ms=1541998826147889031; Hm_lvt_471a5249a2db8e2ac0a5f23672636f92=1541756867,1541998826; Hm_lpvt_471a5249a2db8e2ac0a5f23672636f92=1542002510',
            'Host':'auto.mop.com',
            'If-Modified-Since':'Mon, 12 Nov 2018 05:34:13 GMT',
            'If-None-Match':"FiTD5v2cf3I2RtvdJb8DoWBQerYh",
            'Referer':'http://auto.mop.com/search-models.html?query=%E5%AE%9D%E9%A9%AC',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        self.next_port_parameter = ''
        self.mopfile = open('./mop_json_file.json', 'wb')
        # 表示爬虫是否继续爬取
        self.is_work = True
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-1'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-13'
        # 爬虫计数
        self.get_num = 1

    # 从借口中获取新闻列表信息
    def get_news_port_page(self, next_port_parameter):
        response = requests.get(self.start_url.format(next_port_parameter), headers=self.headers_one)
        response = response.text
        response_dict = response.split('({')[1].split('})')[0]
        response_dict = '{' + response_dict + "}"
        response_dict = ast.literal_eval(response_dict)
        next_port_parameter = response_dict['lastcol_zixun']

        datas = response_dict['data']
        for data in datas:
            # 获取的新的url的参数
            news_url = data['url']
            print(news_url)
            # 日期
            news_date = data['date']
            print(news_date)
            # 来源
            source = data['source']

            # 做时间判断-----------------------------------------------
            get_news_time = news_date.split(' ')[0]
            get_news_time = time.mktime(time.strptime(get_news_time, "%Y-%m-%d"))
            end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
            if self.start_time != '':
                start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
            else:
                start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
            if float(get_news_time) > float(end_time):
                continue
            if float(start_time) <= float(get_news_time) <= float(end_time):
                self.get_news_page('http://auto.mop.com/a/' + news_url, news_date, source)
            else:
                print(1111111)
                self.is_work = False
        # --------------------------------------------------------
        if self.is_work:
            self.get_news_port_page(next_port_parameter)

    # 获取新闻详情页
    def get_news_page(self, url, news_date, source):
        item = {}
        response = requests.get(url)
        print(url)
        data = etree.HTML(response.content.decode())

        if data:
            title = data.xpath('.//h1[@class="artice-title"]/text()')[0]
            page_num_list = data.xpath('.//div[@class="mp-auto-list-paging tc mt30"]/a/text()')
            text = data.xpath('.//div[@class="article"]/p/text()')
            text = ''.join(text)
            page_num_list = data.xpath('.//div[@class="mp-auto-list-paging tc mt30"]/a/text()')
            if page_num_list:
                num = int(page_num_list[-1]) + 1
                print(num)
                for i in range(2, num):
                    next_page_url = url.split('.html')[0] + '-' + str(i) + '.html'
                    print(next_page_url)
                    text2 = self.get_next_news_page(next_page_url)
                    text = text + text2
            # 生成信息字典
            # 网站
            item['platform'] = '猫扑新闻'
            # 发布日期
            item['date'] = news_date.split(' ')[0]
            # 发布时间
            item['time'] = news_date.split(' ')[1]
            # 标题title
            item['title'] = title
            # 正文
            item['content'] = text
            # 来源
            item['source'] = source
            # 点击数
            item['click'] = ''
            # 阅读数
            item['views'] = ''
            # 评论数
            item['comments_count'] = ''
            # 点赞数
            item['likes'] = ''
            # 关键字
            item['keyword'] = ''
            # url
            item['url'] = url
            self.write_news_info_into_jsonfile(item)

    # 获取新闻翻页数据
    def get_next_news_page(self, next_page_url):
        response = requests.get(next_page_url)
        data = etree.HTML(response.content.decode())
        text = data.xpath('.//div[@class="article"]/p/text()')
        text = ''.join(text)
        return text

    # 将数据写入json文件
    def write_news_info_into_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        print('正在写入第%s条数据' % str(self.get_num))
        self.mopfile.write(item.encode('utf-8'))
        self.get_num += 1

    # 关闭json文件
    def close_news_jsonfile(self):
        self.mopfile.close()

    def run(self):
        self.get_news_port_page(self.next_port_parameter)
        self.close_news_jsonfile()


if __name__ == "__main__":
    mopspider = MopSpider()
    mopspider.run()
