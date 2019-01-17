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

    def get_news_url(self, carts):
        """
        从百度搜索关键词，然后获取符合的新闻的url
        :param carts:
        :return:
        """
        # 时间
        get_time = time.time()
        str_time = str(get_time)[:-4]
        date = datetime.now() - timedelta(days=7)
        a = str(date)[:-7]
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeArray))
        end_time = str(timeStamp) + '.' + str_time.split('.')[1]
        print(str_time, end_time)
        url = 'https://www.baidu.com/s?q1={}&q2=&q3=&q4=&gpc=stf%3D{}%2C{}%7Cstftype%3D1&ft=&q5=&q6=xiaohongshu.com&tn=baiduadv'.format(str(carts), end_time, str_time)
        print(url)
        # ip = random.choice(self.proxies_list)
        response = requests.get(url, headers=self.headers_one, verify=False, timeout=30)  # , proxies={'https': ip}
        content = etree.HTML(response.content.decode())
        if content.xpath('.//h3[@class="t"]/a/@href'):
            url_list = content.xpath('.//h3[@class="t"]/a/@href')
            print(url_list)
            for url in url_list:
                news_url = url.replace('http', 'https')
                try:
                    self.get_news_page(news_url)
                except KeyError:
                    print('ip可能被封')
                except IndexError:
                    print('可能出现滑动验证')
                    if self.ip_count < 100:
                        print('更换ip中......')
                        self.ip = proxies.res_ip()
                        self.ip_count += 1
                        self.get_news_page(news_url)
                    else:
                        print('ip超过使用量')

                # time.sleep(2)
        elif content.xpath('.//div[@class="content_none"]/div/p//text()'):
            txt = content.xpath('.//div[@class="content_none"]/div/p//text()')
            print(txt)
        else:
            print('其他错误', url)
        print('------------------------------------------------')

    def get_news_page(self, url):
        """
        获取新闻详情页
        :param url:
        :return:
        """

        item = {}
        # 创建webdrive实例 这是chrom浏览器，有GUI界面
        # option = Options()
        # option.add_argument(r"--proxy-server=http://180.114.94.195:4263")
        # option.add_argument("--headless")
        # self_webdrive = webdriver.Chrome()
        logger.info('xiao_url:{}'.format(url))
        service_args = [
            '--proxy={}'.format(self.ip) ,  # 代理 IP：prot    （eg：192.168.0.28:808）
            '--proxy-type=http',            # 代理类型：http/https
            # '--load - images= no',  # 关闭图片加载（可选）
            # '--disk-cache=yes',          # 开启缓存（可选）
            # '--ignore-ssl-errors=true'    # 忽略https错误（可选）
        ]
        # 使用phantomjs无界面浏览器
        print(url, 11111)
        self_webdrive = webdriver.PhantomJS(executable_path='./../xiaohongshu/phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args=service_args)
        # self_webdrive = webdriver.PhantomJS(executable_path='./../xiaohongshu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self_webdrive.set_page_load_timeout(30)
        self_webdrive.get(url)
        print(self_webdrive.title)
        time.sleep(2)
        data = self_webdrive.page_source
        data = etree.HTML(data)
        if data.xpath('.//div[@class="placeholder"]/p/text()'):
            pass
        else:
            # if data.xpath('.//div/div[@class="content"]/p/text()'):
            content = data.xpath('.//div/div[@class="content"]/p/text()')
            # else:
            #     content = data.xpath('.//div/div[@class="content"]//text()')
            content = ''.join(content)
            print(content)
            try:
                title = data.xpath('.//div/div[@class="content"]/h1/text()')[0]
            except:
                title = data.xpath('.//h1[@class="title"]/text()')[0]
            print(title)

            date_all = data.xpath('.//span[@class="time"]/text()')[0]
            date = date_all.split(' ')[0]
            news_time = date_all.split(' ')[1]
            author = data.xpath('.//span[@class="name-detail"]/text()')[0]

            # if content:
            self_webdrive.quit()
            item['platform'] = '小红书'
            item['title'] = title
            item['date'] = date
            item['time'] = news_time
            item['source_author'] = author
            item['content'] = content
            item['url'] = url
            item['comments_count'] = ''
            item['clicks'] = ''
            item['likes'] = ''
            item['keyword'] = ''
            self.write_news_jsonfile(item)
            # print('文章类页面-------------------', url)
            # else:
            #     print('视频类页面+++++++++++++++++++', url)


    def get_at(self):
        url = 'https://anti-bot.baidu.com/abdr'
        data = 'eyIxIjoiMSIsIjMiOiI1ZTg1MThiY2RhOTlmNzczZWRmMDZmZTJmY2ZlYzVkNDc0ZmU3Njg1IiwiNCI6IjI0IiwiNSI6IjE2MDB4OTAwIiwiNiI6IjE2MDB4ODYwIiwiNyI6IiwiLCI4IjoiQ2hyb21lJTIwUERGJTIwUGx1Z2luLENocm9tZSUyMFBERiUyMFZpZXdlcixOYXRpdmUlMjBDbGllbnQiLCI5IjoiLFBvcnRhYmxlJTIwRG9jdW1lbnQlMjBGb3JtYXQsTmF0aXZlJTIwQ2xpZW50JTIwRXhlY3V0YWJsZSxQb3J0YWJsZSUyME5hdGl2ZSUyMENsaWVudCUyMEV4ZWN1dGFibGUiLCIxMSI6IjEiLCIxMiI6IjEiLCIxMyI6InRydWUiLCIxNCI6Ii00ODAiLCIxNSI6InpoLUNOIiwiMTYiOiIiLCIxNyI6IjEsMSwxLDEsMSwwIiwiMTgiOiIxIiwiMTkiOiIyIiwiMjAiOiIwIiwiMjEiOiIiLCIyMiI6IkdlY2tvLDIwMDMwMTA3LEdvb2dsZSBJbmMuLCxNb3ppbGxhLE5ldHNjYXBlLFdpbjMyLDMzLCIsIjIzIjoiMCwwLDAiLCIyNCI6IjEiLCIyNyI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzcwLjAuMzUzOC4xMTAgU2FmYXJpLzUzNy4zNiIsIjI4IjoiZmFsc2UsZmFsc2UiLCIyOSI6InRydWUsdHJ1ZSx0cnVlIiwiMzIiOiIzNCIsIjM0IjoiV2luMzIiLCIzNSI6ImZhbHNlLHRydWUiLCIxMDEiOiJhNTQ2Nzg4NGI4ZTg5YjlmMTE2MTJhNDExZThhYjdmNDgyYmNkY2JiIiwiMTAzIjoiMTU0Mzg5MTU0MzgyMCIsIjEwNCI6IiIsIjEwNiI6IjIwMDUiLCIxMDciOiIxMiIsIjEwOCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjMzNDIvY2hhbmNlL3R4Lmh0bWw/X2lqdD1oOWU5bDdpNDlsM2pjZjA2bDY2Y2ZjZWplMCIsIjEwOSI6IiIsIjExMCI6IjkxZTkzMDhjNGE2MmNkYTM2Y2EzNDdiN2RhNmQ4ZDFiYmY1YTEiLCIxMTIiOiIiLCIxMTMiOiIiLCIxMTQiOiIiLCIxMTUiOiIiLCIyMDAiOiIxIn0='
        response = requests.post(url, data=data)
        text = response.text
        return text

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../xiaohongshu/28_{}_xiaohongshu_news.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../xiaohongshu/42_{}_xiaohongshu_commnet.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        excelfile = xlrd.open_workbook(r'./../xiaohongshu/keywordV1.4.xlsx')
        print(excelfile.sheet_names())
        sheet1 = excelfile.sheet_by_name('Sheet1')
        cols = sheet1.col_values(0)
        cols = cols[1:]
        for cart in cols:
            # time.sleep(2)
            try:
             self.get_news_url(cart)
            except:
                logger.error(traceback.format_exc())


if __name__ == "__main__":
    xiaohongshu = XiaoHongShuSpider()
    xiaohongshu.run()