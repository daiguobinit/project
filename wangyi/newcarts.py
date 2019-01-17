import requests
from lxml import etree
import json
import re
import math
import time
import ast
import random
from datetime import datetime
from datetime import timedelta
import logging
import traceback

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../wangyi/wangyi-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class WangYiSpider(object):

    def __init__(self):

        self.headers_one = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Cookie':'Province=021;City=021; UM_distinctid=167167e03cf21d-06e10e6c7b740a-414f0120-15f900-167167e03d01bd; vjuids=-557de2078.167167e08f2.0.7347b06fe51a6; _ntes_nnid=6252d0d97812437a4b7ff6217cedcc48,1542270617849; _ntes_nuid=6252d0d97812437a4b7ff6217cedcc48; _antanalysis_s_id=1542270618187; __gads=ID=cc3983f5cdda3076:T=1542270617:S=ALNI_MagAFZ2moSoB4SrPD4W8Cnd9aa93Q; NNSSPID=71084a74668d496db04b9be5eaa98a1f; ne_analysis_trace_id=1542345088187; CNZZDATA1256336326=414109981-1542267111-%7C1542350651; vjlast=1542270618.1542335885.13; vinfo_n_f_l_n3=534cfd2536f3668a.1.6.1542270617858.1542350799174.1542352815563; s_n_f_l_n3=534cfd2536f3668a1542350884709',
            'Host':'auto.163.com',
            'Connection': 'close',
            'Referer':'http://auto.163.com/special/2016buy/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'','
        }
        self.headers_two = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection': 'close',
            'Cookie':'Province=021; City=021; UM_distinctid=167167e03cf21d-06e10e6c7b740a-414f0120-15f900-167167e03d01bd; vjuids=-557de2078.167167e08f2.0.7347b06fe51a6; _ntes_nnid=6252d0d97812437a4b7ff6217cedcc48,1542270617849; _ntes_nuid=6252d0d97812437a4b7ff6217cedcc48; _antanalysis_s_id=1542270618187; __gads=ID=cc3983f5cdda3076:T=1542270617:S=ALNI_MagAFZ2moSoB4SrPD4W8Cnd9aa93Q; NNSSPID=71084a74668d496db04b9be5eaa98a1f; ne_analysis_trace_id=1542345088187; pgr_n_f_l_n3=534cfd2536f3668a15423559003332052; vjlast=1542270618.1542335885.13; vinfo_n_f_l_n3=534cfd2536f3668a.1.9.1542270617858.1542357144579.1542357875424; s_n_f_l_n3=534cfd2536f3668a1542357867492',
            'Host':'comment.api.163.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        # 购车模块
        self.buy_url = 'http://auto.163.com/special/2016buy{}/'
        # 新车模块
        self.nauto_url = 'http://auto.163.com/special/2016nauto{}/'
        # 试驾模块
        self.drive_url = 'http://auto.163.com/special/2016drive{}/'
        # 导购模块
        self.guide_url = 'http://auto.163.com/special/2016buyers_guides{}/'
        # 新能源模块
        self.newenergy_url = 'http://auto.163.com/special/auto_newenergy{}/'
        # 行业模块
        self.news_url = 'http://auto.163.com/special/2016news{}/'
        # 表示评论页数
        self.comment_page_num = 0
        # 评论接口模板
        self.comment_port_url = 'http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?ibc=newspc&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&offset={}&callback=jsonp_1542355418897&_=1542355418898'
        # 代理ip
        self.proxies = {
            '180.118.247.30'
        }

        # 打卡json文件
        # self.news_jsonfile = open('./wangyi_news_jsonfile.json', 'wb')
        # self.comments_jsonfile = open('./wangyi_comments_jsonfile.json', 'wb')


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

        # # 定义开始时间 y-m-d
        # self.start_time = '2018-11-14'
        # # 定义结束时间 y-m-d
        # self.end_time = '2018-11-17'
        # 爬虫正常工作
        self.is_work = True

    # 获取新闻列表页
    def get_all_news_page(self, url):
        s = requests.session()
        s.keep_alive = False
        response = requests.get(url)
        data = response.content.decode('gbk')
        data = etree.HTML(data)
        news_list = data.xpath('.//div[@class="item-cont"]')
        for news in news_list:
            try:
                title = news.xpath('.//h3/a/text()')[0]
                news_url = news.xpath('.//h3/a/@href')[0]
                news_date = news.xpath('.//span[@class="item-time"]/text()')[0]
                comment_count = news.xpath('.//span[@class="item-comment"]/text()')[0]
                # 做时间判断部分---------------
                get_news_time = time.mktime(time.strptime(news_date, "%Y-%m-%d"))
                end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                if self.start_time != '':
                    start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                else:
                    start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                if float(get_news_time) < float(start_time):
                    self.is_work = False
                    return

                if float(start_time) <= float(get_news_time) <= float(end_time):
                    self.get_news_info_page(news_url, comment_count)
            except:
                continue

    # 获取新闻详情页
    def get_news_info_page(self, news_url, comment_count):
        item = {}
        s = requests.session()
        s.keep_alive = False
        response = requests.get(news_url, headers=self.headers_one)
        status_code = response.status_code
        if status_code == 200:
            data = response.content.decode('gbk')
            data = etree.HTML(data)
            news_id = news_url.split('/')[-1].split('.')[0]
            title = data.xpath('.//div[@id="epContentLeft"]/h1/text()')[0]
            date_all = data.xpath('.//div[@class="post_time_source"]/text()')[0]
            date_all = re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', date_all)[0]

            # 获取评论数
            try:
                s = requests.session()
                s.keep_alive = False
                comment_response = requests.get('http://comment.tie.163.com/' + str(news_id) + '.html')
                print('http://comment.tie.163.com/' + str(news_id) + '.html')
                comment_data = comment_response.content.decode()
                count = re.search('"tcount":\d{0,10}', comment_data).group(0)
                count = count.split(":")[1]
            except:
                count = ''

            # 网站
            item['platform'] = '网易新闻'
            # 日期date
            date = date_all.split(' ')[0]
            item['date'] = date
            news_time = date_all.split(' ')[1]
            item['time'] = news_time
            item['title'] = title
            # 来源
            source = data.xpath('.//div[@class="post_time_source"]/a/text()')[0]
            item['source_author'] = source
            # 正文内容
            content = data.xpath('.//div[@id="endText"]/p/text() | .//div[@id="endText"]/p/a/text()')
            content = ''.join(content)
            content = content.replace('\n', '')
            content = content.replace(' ', '')
            item['content'] = content
            item['keyword'] = ''
            item['url'] = news_url
            item['views'] = ''
            item['comments_count'] = count
            item['likes'] = ''
            item['clicks'] = ''

            self.write_news_jsonfile(item)

            # 调用爬取评论的函数
            # http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/E0IBEEA10008856S/comments/newList?ibc=newspc&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&offset=0&callback=jsonp_1542355418897&_=1542355418898

            self.get_comment_info(self.comment_port_url.format(news_id, "0"), news_id, date, news_time, title, news_url)

    # 获取评论信息
    def get_comment_info(self, url, news_id, source_date, source_time, source_title, source_url):
        # time.sleep(1)
        item = {}
        s = requests.session()
        s.keep_alive = False
        respnse = requests.get(url, headers=self.headers_two)
        status_code = respnse.status_code
        if status_code == 200:
            data = respnse.content.decode()
            try:
                data = re.findall(r'{"commentIds.*newListSize":\d{0,10}}', data)[0]
                data = json.loads(data)
                comment_data = data['comments']
                comment_id = data['commentIds']
                if comment_id:
                    for comment_info in comment_data.items():
                        comment_info = comment_info[1]
                        # 网站
                        item['platform'] = '网易新闻'
                        # 日期时间
                        date_all = comment_info['createTime']
                        date = date_all.split(' ')[0]
                        item['date'] = date
                        comment_time = date_all.split(' ')[1]
                        item['time'] = comment_time
                        # 发帖作者
                        try:
                            author = comment_info['user']['nickname']
                        except KeyError:
                            author = comment_info['user']['location'] + '网友'
                        item['author'] = author
                        # 内容
                        content = comment_info['content']
                        item['content'] = content
                        # 点赞数
                        item['likes'] = ''
                        # 原文发布日期时间
                        item['source_date'] = source_date
                        item['source_time'] = source_time
                        # 原文标题
                        item['title'] = source_title
                        # 原文url
                        item['source_url'] = source_url
                        item['keyword'] = ''
                        item['floor'] = ''
                        item['comment_url'] = 'http://comment.tie.163.com/' + str(news_id) + '.html'
                        item['comments_count'] = ''
                        item['views'] = ''
                        self.write_comment_jsonfile(item)

                    self.comment_page_num += 30
                    print(self.comment_page_num, '111111111111111111111111')

                    self.get_comment_info(self.comment_port_url.format(news_id, str(self.comment_page_num)), news_id, source_date, source_time, source_title, source_url)
                else:
                    print('评论爬取完毕')
                    self.comment_page_num = 30
            except:
                pass

    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../wangyi/15_{}_wangyi_news.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode('utf-8'))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../wangyi/29_{}_wangyi_commnet.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode('utf-8'))

    # # 关闭json文件
    # def close_jsonfile(self):
    #     self.news_jsonfile.close()
    #     self.comments_jsonfile.close()

    def run(self):
        '''
        # 购车模块 10
        self.buy_url = 'http://auto.163.com/special/2016buy{}/'
        # 新车模块 10
        self.nauto_url = 'http://auto.163.com/special/2016nauto{}/'
        # 试驾模块 10
        self.drive_url = 'http://auto.163.com/special/2016drive{}/'
        # 导购模块 10
        self.guide_url = 'http://auto.163.com/special/2016buyers_guides{}/'
        # 新能源模块 5
        self.newenergy_url = 'http://auto.163.com/special/auto_newenergy{}/'
        # 行业模块  10
        self.news_url = 'http://auto.163.com/special/2016news{}/'

        更换下面标记的url和循环次数，来爬取不同的模块，如上所示
        '''
        url_list = [{'url': 'http://auto.163.com/special/2016buy{}/', 'num': 11},
                    {'url': 'http://auto.163.com/special/2016nauto{}/', 'num': 11},
                    {'url': 'http://auto.163.com/special/2016drive{}/', 'num': 11},
                    {'url': 'http://auto.163.com/special/2016buyers_guides{}/', 'num': 11},
                    {'url': 'http://auto.163.com/special/auto_newenergy{}/', 'num': 6},
                    {'url': 'http://auto.163.com/special/2016news{}/', 'num': 11}]

        for data in url_list:
            print(data)
            self.is_work = True
            for i in range(1, data['num']):  # 循环次数
                if self.is_work:
                    if i == 1:
                        # ---------------------
                        url = data['url'].format('')
                        print('爬取' + url)
                        self.get_all_news_page(url)
                    elif i == data['num']-1:
                        # ---------------------
                        url = data['url'].format('_'+str(i))
                        print('爬取' + url)
                        self.get_all_news_page(url)
                    else:
                        # ---------------------
                        url = data['url'].format('_0'+str(i))
                        print('爬取' + url)
                        self.get_all_news_page(url)
                else:
                    break

        logger.info('爬取完毕......')

if __name__ == "__main__":
    wangyispider = WangYiSpider()
    wangyispider.run()
