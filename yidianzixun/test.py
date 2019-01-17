import requests
from lxml import etree
import json
import re
import math
import time
import ast
import xlrd
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
import xlrd
import logging
import traceback
import proxies
from datetime import date

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../xiaohongshu/xiaohongshu-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class XiaoHongShuSpider(object):
    """
    小红书网站的爬虫
    这是一个爬虫模板
    """
    def __init__(self):

        self.headers_one = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.baidu.com',
            # 'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.headers_two = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        self.headers_three = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Connection': 'keep-alive',
            'Host': 'www.xiaohongshu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.start_url = ''
        # 评论接口模板
        self.commnet_port_url = ''
        # # 打开json文件
        # self.news_jsonfile = open('./sina_newsfile.json', 'wb')
        # self.comment_jsonfile = open('./sina_commentfile.json', 'wb')
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
        # 标记爬虫工作
        self.is_work = True
        # ip代理
        self.proxies_list = [
            '121.231.226.210:4252',
        ]

        self.ip = proxies.res_ip()

        self.ip_count = 0

        # url去重list
        self.set_list = []

    def get_news_url(self, num):
        """
        从百度搜索关键词，然后获取符合的新闻的url
        :param carts:
        :return:
        """
        # 时间
        get_time = time.time()
        str_time = str(get_time)[:-4]
        date = datetime.now() - timedelta(days=3)
        a = str(date)[:-7]
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeArray))
        end_time = str(timeStamp) + '.' + str_time.split('.')[1]
        print(str_time, end_time)
        # url = 'https://www.baidu.com/s?q1=汽车&q2=&q3=&q4=&gpc=stf%3D{}%2C{}%7Cstftype%3D1&ft=&q5=&q6=www.yidianzixun.com&tn=baiduadv&pn={}'.format(end_time, str_time, num)
        url = 'https://www.baidu.com/s?wd=site%3A(www.yidianzixun.com)%20%E6%B1%BD%E8%BD%A6&pn={}&oq=site%3A(www.yidianzixun.com)%20%E6%B1%BD%E8%BD%A6&ct=2097152&tn=baiduadv&ie=utf-8&si=(www.yidianzixun.com)&rsv_pq=e948db9e00097fcd&rsv_t=1273sdRx9rzb35pYERweuGf1mV6RO2BZZUthjhhdYlSidhjyUjzN%2FuD2LYJ1%2Fso&gpc=stf%3D{}%2C{}%7Cstftype%3D2&tfflag=1'.format(num, end_time, str_time)
        print(url)
        # ip = random.choice(self.proxies_list)
        response = requests.get(url, headers=self.headers_one, verify=False, timeout=30)  # , proxies={'https': ip}
        content = etree.HTML(response.content.decode())
        if content.xpath('.//h3[@class="t"]/a/@href'):
            url_list = content.xpath('.//h3[@class="t"]/a/@href')
            print(url_list)
            print(len(url_list))
            for url_ch in url_list:
                response = requests.get(url_ch, headers=self.headers_two, allow_redirects=False)
                print(response.status_code)
                news_url = response.headers['Location']
                print(news_url)
                if news_url not in self.set_list:
                    try:
                        self.get_news_page_info(news_url)
                    except Exception as e:
                        print(e)
                        time.sleep(15)
                    self.set_list.append(news_url)


    def get_news_page_info(self, url):
        item = {}
        response = requests.get(url)
        print(response.url)
        data = etree.HTML(response.content.decode())
        title = data.xpath('.//h2/text()')[0]
        if data.xpath('.//a[@class="doc-source"]/text()'):
            source = data.xpath('.//a[@class="doc-source"]/text()')[0]
        else:
            source = data.xpath('.//div[@class="meta"]/span[1]/text()')[0]
        # date_time = data.xpath('.//div[@class="meta"]/span[2]/text()')[0]
        if data.xpath('.//div[@id="imedia-article"]//text()'):
            content = data.xpath('.//div[@id="imedia-article"]//text()')
        elif data.xpath('.//div[@id="imedia-article"]/article/p//text()'):
            content = data.xpath('.//div[@id="imedia-article"]/article/p//text()')
        elif data.xpath('.//div[@id="imedia-article"]/section/section//text()'):
            content = data.xpath('.//div[@id="imedia-article"]/section/section//text()')
        elif data.xpath('.//div[@class="content-bd"]/div/div//text()'):
            content = data.xpath('.//div[@class="content-bd"]/div/div//text()')
        elif data.xpath('.//div[@class="content-bd"]/p//text()'):
            content = data.xpath('.//div[@class="content-bd"]/p//text()')
        elif data.xpath('.//div[@class="content-bd"]/div/div/text()'):
            content = data.xpath('.//div[@class="content-bd"]/div/div//text()')
        elif data.xpath('.//div[@class="content-bd"]/section//text()'):
            content = data.xpath('.//div[@class="content-bd"]/section//text()')
        elif data.xpath('.//div[@class="content-bd"]/section/text()'):
            content = data.xpath('.//div[@class="content-bd"]/section/text()')
        elif data.xpath('.//div[@class="content-bd"]//text()'):
            content = data.xpath('.//div[@class="content-bd"]//text()')
        else:
            content = data.xpath('.//div[@id="imedia-article"]/section/section/section/p//text()')
        content = ''.join(content)

        # get_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['platform'] = '一点资讯'
        item['title'] = title
        item['source'] = source
        item['content'] = content
        item['url'] = url
        if data.xpath('.//div[@class="meta"]/span[2]/text()'):
            date_all = data.xpath('.//div[@class="meta"]/span[2]/text()')[0]
        else:
            date_all = data.xpath('.//div[@class="meta"]/span/text()')[0]
        try:
            if date_all == '昨天':
                yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
                yesterday = str(yesterday).split(' ')[0]
                item['date'] = yesterday
            elif date_all == '2天前':
                yesterday = datetime.now() - timedelta(days=2)  # 前天时间
                yesterday = str(yesterday).split(' ')[0]
                item['date'] = yesterday
            else:
                item['date'] = date_all
        except:
            today = date.today() + timedelta()
            item['date'] = today
        item['time'] = ''
        item['likes'] = ''
        item['clicks'] = ''
        item['views'] = ''
        item['keyword'] = ''
        item['commnets_count'] = ''

        # 做时间判断部分---------------  这个部分区分于另外一个部分
        if date_all == '昨天' or date_all == '2天前' or date_all == '3天前':
            print(date_all, '时间符合')
            print(item)
            self.write_news_jsonfile(item)
            news_id = url.split('/')[-1]
            self.get_commnet_info(news_id, title, url)
        else:
            print(date_all, '时间不符合')

    # 获取评论信息
    def get_commnet_info(self, news_id, title, source_url, last_comment_id=''):
        item = {}
        url = 'http://www.yidianzixun.com/home/q/getcomments?_=1542864983174&docid={}&s=&count=30&last_comment_id={}&appid=web_yidian'.format(
            str(news_id), last_comment_id)
        response = requests.get(url)
        data = json.loads(response.content.decode())
        comments = data['comments']
        if comments:
            for comment in comments:
                print('爬取评论中')
                item['platform'] = '一点资讯'
                item['title'] = title
                content = comment['comment']
                item['content'] = content
                author = comment['nickname']
                item['source_author'] = author
                date_all = comment['createAt']
                comment_date = date_all.split(' ')[0]
                comment_time = date_all.split(' ')[1]
                item['date'] = comment_date
                item['time'] = comment_time
                item['source_date'] = ''
                item['source_time'] = ''
                item['source_url'] = source_url
                item['floor'] = ''
                item['keyword'] = ''
                item['comment_url'] = url
                item['views'] = ''
                item['comments_count'] = ''
                item['likes'] = ''
                self.write_comment_jsonfile(item)

            if len(comments) == 30:
                last_comment_id = comments[-1]['comment_id']
                print('评论翻页')
                self.get_commnet_info(news_id, title, source_url, last_comment_id=last_comment_id)

    def get_at(self):
        url = 'https://anti-bot.baidu.com/abdr'
        data = 'eyIxIjoiMSIsIjMiOiI1ZTg1MThiY2RhOTlmNzczZWRmMDZmZTJmY2ZlYzVkNDc0ZmU3Njg1IiwiNCI6IjI0IiwiNSI6IjE2MDB4OTAwIiwiNiI6IjE2MDB4ODYwIiwiNyI6IiwiLCI4IjoiQ2hyb21lJTIwUERGJTIwUGx1Z2luLENocm9tZSUyMFBERiUyMFZpZXdlcixOYXRpdmUlMjBDbGllbnQiLCI5IjoiLFBvcnRhYmxlJTIwRG9jdW1lbnQlMjBGb3JtYXQsTmF0aXZlJTIwQ2xpZW50JTIwRXhlY3V0YWJsZSxQb3J0YWJsZSUyME5hdGl2ZSUyMENsaWVudCUyMEV4ZWN1dGFibGUiLCIxMSI6IjEiLCIxMiI6IjEiLCIxMyI6InRydWUiLCIxNCI6Ii00ODAiLCIxNSI6InpoLUNOIiwiMTYiOiIiLCIxNyI6IjEsMSwxLDEsMSwwIiwiMTgiOiIxIiwiMTkiOiIyIiwiMjAiOiIwIiwiMjEiOiIiLCIyMiI6IkdlY2tvLDIwMDMwMTA3LEdvb2dsZSBJbmMuLCxNb3ppbGxhLE5ldHNjYXBlLFdpbjMyLDMzLCIsIjIzIjoiMCwwLDAiLCIyNCI6IjEiLCIyNyI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzcwLjAuMzUzOC4xMTAgU2FmYXJpLzUzNy4zNiIsIjI4IjoiZmFsc2UsZmFsc2UiLCIyOSI6InRydWUsdHJ1ZSx0cnVlIiwiMzIiOiIzNCIsIjM0IjoiV2luMzIiLCIzNSI6ImZhbHNlLHRydWUiLCIxMDEiOiJhNTQ2Nzg4NGI4ZTg5YjlmMTE2MTJhNDExZThhYjdmNDgyYmNkY2JiIiwiMTAzIjoiMTU0Mzg5MTU0MzgyMCIsIjEwNCI6IiIsIjEwNiI6IjIwMDUiLCIxMDciOiIxMiIsIjEwOCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjMzNDIvY2hhbmNlL3R4Lmh0bWw/X2lqdD1oOWU5bDdpNDlsM2pjZjA2bDY2Y2ZjZWplMCIsIjEwOSI6IiIsIjExMCI6IjkxZTkzMDhjNGE2MmNkYTM2Y2EzNDdiN2RhNmQ4ZDFiYmY1YTEiLCIxMTIiOiIiLCIxMTMiOiIiLCIxMTQiOiIiLCIxMTUiOiIiLCIyMDAiOiIxIn0='
        response = requests.post(url, data=data)
        text = response.text
        return text

    def write_news_jsonfile(self, item):
        print('正在写入新闻数据......')
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../yidianzixun/26_{}_yidianzixun_news.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode('utf-8'))

    def write_comment_jsonfile(self, item):
        print('正在写入评论数据......')
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../yidianzixun/40_{}_yidianzixun_commnet.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode('utf-8'))

    def run(self):
        for i in range(0, 25):
            i = i*10
            self.get_news_url(str(i))

if __name__ == "__main__":
    xiaohongshu = XiaoHongShuSpider()
    xiaohongshu.run()