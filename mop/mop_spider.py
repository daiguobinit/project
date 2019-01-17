import requests
from lxml import etree
import json
import re
import math
import time
import ast
from datetime import datetime
from datetime import timedelta
import xlrd
import logging
import traceback
from urllib.request import quote
requests.adapters.DEFAULT_RETRIES = 5

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../mop/mop-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class MopSpider(object):
    def __init__(self):
        self.start_url = 'http://autoapi.dftoutiao.com/mopsearch_h5/searchnews?jsonpcallback=jQuery18309647992932972742_1541999181929&keywords={}&stkey_zixun=&lastcol_zixun={}&splitwordsarr=&stkey_video=&lastcol_video=&maintype=&domain=mopauto_pc&os=Win7&qid=&recgid=15417568671858769&_=1541999185686'
        # 获取数据接口的headers
        self.headers_one = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Host':'autoapi.dftoutiao.com',
            'Connection': 'close',
            'Referer':'http://auto.mop.com/search-models.html?query=%E5%AE%9D%E9%A9%AC',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        # 获取新闻详情页的headers
        self.headers_two = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection': 'close',
            # 'Cookie':'mopauto_uid=15417568671858769; _mc=m-1541756833719532435; BDTUJIAID=23ededdadee3798fd3cfff3b5345490d; localCity=%E4%B8%8A%E6%B5%B7; cityname=%E4%B8%8A%E6%B5%B7; _ms=1541998826147889031; Hm_lvt_471a5249a2db8e2ac0a5f23672636f92=1541756867,1541998826; Hm_lpvt_471a5249a2db8e2ac0a5f23672636f92=1542002510',
            'Host':'auto.mop.com',
            'If-Modified-Since':'Mon, 12 Nov 2018 05:34:13 GMT',
            'If-None-Match':"FiTD5v2cf3I2RtvdJb8DoWBQerYh",
            'Referer':'http://auto.mop.com/search-models.html?query=%E5%AE%9D%E9%A9%AC',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        self.next_port_parameter = ''
        # 表示爬虫是否继续爬取
        self.is_work = True
        date = datetime.now() - timedelta(days=3)
        news_start_time = str(date).split(' ')[0]
        yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
        yesterday = str(yesterday).split(' ')[0]
        print('爬取时间段：{}到{}'.format(news_start_time, yesterday))

        logging.info('爬取时间段：{}到{}'.format(news_start_time, yesterday))

        # 定义开始时间 y-m-d  离现在时间远  news_start_time
        self.start_time = news_start_time
        # 定义结束时间 y-m-d  离现在时间近  yesterday
        self.end_time = yesterday
        # 爬虫计数
        self.get_num = 1

    # 从借口中获取新闻列表信息
    def get_news_port_page(self, key_word, keyword_code,  next_port_parameter):
        s = requests.session()
        s.keep_alive = False
        response = requests.get(self.start_url.format(keyword_code, next_port_parameter), headers=self.headers_one)
        print(response.url)
        print(response.text)
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
                self.get_news_page('http://auto.mop.com/a/' + news_url, news_date, source, key_word)
            else:
                print(1111111)
                self.is_work = False
        # --------------------------------------------------------
        if self.is_work:
            self.get_news_port_page(key_word, keyword_code,  next_port_parameter)

    # 获取新闻详情页
    def get_news_page(self, url, news_date, source, key_word):
        item = {}
        try:
            s = requests.session()
            s.keep_alive = False
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
                item['clicks'] = ''
                # 阅读数
                item['views'] = ''
                # 评论数
                item['comments_count'] = ''
                # 点赞数
                item['likes'] = ''
                # 关键字
                item['keyword'] = key_word
                # url
                item['url'] = url
                self.write_news_info_into_jsonfile(item)
        except:
            logger.error(traceback.format_exc())

    # 获取新闻翻页数据
    def get_next_news_page(self, next_page_url):
        s = requests.session()
        s.keep_alive = False
        response = requests.get(next_page_url)
        data = etree.HTML(response.content.decode())
        text = data.xpath('.//div[@class="article"]/p/text()')
        text = ''.join(text)
        return text

    # 将数据写入json文件
    def write_news_info_into_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        print('正在写入第%s条数据' % str(self.get_num))
        with open('./../mop/21_{}_mop.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        self.get_num += 1

    def run(self):
        excelfile = xlrd.open_workbook(r'./../mop/keywordV1.4.xlsx')
        sheet1 = excelfile.sheet_by_name('Sheet1')
        cols = sheet1.col_values(0)
        cols = cols[1:]
        print(cols)
        for keyword in cols:
            print('爬取关键字：{}，  爬取进度{}/{}'.format(keyword, str(cols.index(keyword) + 1), str(len(cols))))

            keyword_code = quote(keyword, encoding="utf-8")

            keyword_code = quote(keyword_code, encoding="utf-8")
            try:
                self.get_news_port_page(keyword, keyword_code, self.next_port_parameter)
            except Exception as e:
                print('发生错误：', e)
                logger.info('搜索关键字无数据,关键字为：', keyword, traceback.format_exc())
                time.sleep(20)

            logger.info('数据爬取完毕.........')


if __name__ == "__main__":
    mopspider = MopSpider()
    mopspider.run()
