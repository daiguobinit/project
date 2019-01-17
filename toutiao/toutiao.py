import requests
from lxml import etree
import json
import re
import math
import time
import ast
import random
from as_cp import get_as_cp
from xml.sax.saxutils import unescape
# from ippro.proxies import res_ip
import proxies
from datetime import datetime
from datetime import timedelta
import logging
import traceback

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../toutiao/toutiao-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class TouTiaoSpider(object):
    """
    今日头条的爬虫，主要采集和汽车有关的新闻
    """
    def __init__(self):

        # 'cookie':'uuid="w:d0214807f672416fb7d3ee0431aa13a3"; UM_distinctid=1674ef3a9800-0bce565d4c8dc4-414f0120-15f900-1674ef3a981290; _ga=GA1.2.823209007.1543222670; _gid=GA1.2.547615301.1543222670; CNZZDATA1259612802=603836554-1543213069-%7C1543218469; __tasessionId=tpisw88851543281460530; csrftoken=d9a6dad7de6c1fbbf3ddd1a3de811481; tt_webid=6628070185327625741',
        # ':authority':'www.toutiao.com',
        # ':method':'GET',
        # ':path':'/api/pc/feed/?category=news_car&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1E56B7F8CD9B35&cp=5BFC39BB43B5DE1&_signature=pMmtcAAA.0TvpJ9rFvhWIKTJrW',
        # ':scheme':'https',
        # 'cache-control': 'max-age=0',
        # 'cookie': 'tt_webid=6628733243796178436; tt_webid=6628733243796178436; csrftoken=3a6f2dc0f315bd1fe957319a75bba4ed; uuid="w:2203d39caf3249c0bcda19ee5839b850"; UM_distinctid=1675827673a27a-0dd556679b3f63-3a3a5d0c-15f900-1675827673b22c; __tasessionId=qb2c0x9mb1543386267822; CNZZDATA1259612802=992935523-1543369669-%7C1543385869',
        # 'referer': 'https://www.toutiao.com/ch/news_car/',
        self.headers_one = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.start_url = 'https://www.toutiao.com/api/pc/feed/'
        # 评论接口模板
        self.commnet_port_url = ''

        date = datetime.now() - timedelta(days=3)
        news_start_time = str(date).split(' ')[0]
        yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
        yesterday = str(yesterday).split(' ')[0]
        print('爬取时间段：{}到{}'.format(news_start_time, yesterday))

        logging.info('爬取时间段：{}到{}'.format(news_start_time, yesterday))
        # 定义开始时间 y-m-d  离现在时间远
        news_start_time = news_start_time
        # 定义结束时间 y-m-d  离现在时间近
        new_end_time = yesterday

        # 定义开始时间 y-m-d
        self.start_time = news_start_time
        # 定义结束时间 y-m-d
        self.end_time = new_end_time

        # 标记爬虫工作
        self.is_work = True
        # 评论页数
        self.comment_page_num = 1
        # 去重列表
        self.set_list = []
        # 代理ip
        self.proxies = [
            '112.245.235.249:4243',
            # '59.53.47.4:4249'
        ]
        # 搜集问答类网页的列表
        self.questions_list = []

        # 读取url列表
        with open('./../toutiao/new_url_file.json', 'r') as f:
            self.url_list = f.readlines()

        # 获取ip
        self.ip = proxies.res_ip()

        # ip计数
        self.ip_count = 0

    # # 从接口获取数据
    # def get_news_list_port(self, url, ip, next=0):
    #     as_cp = get_as_cp()
    #     print(as_cp)
    #     params = {
    #         'category': 'news_car',
    #         'utm_source': 'toutiao',
    #         'widen': 1,
    #         'max_behot_time': next,
    #         'max_behot_time_tmp': next,
    #         'tadrequire': 'true',
    #         'as': as_cp['as'],
    #         'cp': as_cp['cp'],
    #         '_signature': 'DTdIWAAAVtBGWnpD5b1pLA03SE'
    #     }
    #     response = requests.get(url, headers=self.headers_one, params=params)
    #     data = response.content.decode()
    #     data = data.encode('utf-8').decode('unicode_escape')
    #     print(response.url)
    #     data = json.loads(data)
    #     print(data)
    #     next_id = data['next']['max_behot_time']
    #     print(next_id)
    #     time.sleep(3)
    #     self.get_news_list_port(url, ip, next=next_id)

    def get_news_page(self, url, ip):
        user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
        ]
        headers_one = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': '{}'.format(random.choice(user_agent))
        }

        item = {}
        # ip = random.choice(self.proxies)
        print(ip)
        response = requests.get(url, headers=headers_one, proxies={'https': ip}, timeout=20)  #, proxies={'https': ip}
        stutus_code = response.status_code
        if str(stutus_code) == '200':
            data_all = response.content.decode()
            try:
                data = re.search(r"articleInfo: {([\s\S]*time: '\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", data_all).group(1)
                data = '{' + data + "'}}"
                data = re.sub('\n', '', data)
                data = unescape(data)
                data = data.replace('&quot;', '"').replace('&#x3D;', '=')
                content = re.search('content: ([\s\S]*)groupId', data).group(1).strip()[1:][:-2]
                content = etree.HTML(content)
                text = content.xpath('.//p//text()')
                text_con = ''.join(text)
                date, create_time = re.search('(\d{4}-\d{1,2}-\d{1,2}) (\d{1,2}:\d{1,2}:\d{1,2})', data).group(1, 2)
                id_num = re.search("groupId: '(\d{1,50}).*itemId", data).group(1)  # 新闻的标识id
                source = re.search("source: '(.*)time", data).group(1).strip()[:-2]  # 来源
                comment_count = re.search("commentCount: '(\d{0,10})[\s\S]*ban_comment", data_all).group(1)
                title = re.search("title: '([\s\S])*content", data).group(0).split("'")[1]
                item['platform'] = '今日头条'
                item['date'] = date
                item['time'] = create_time
                item['title'] = title
                item['source_author'] = source
                item['url'] = url
                item['content'] = text_con
                item['comments_count'] = comment_count
                item['clicks'] = ''
                item['views'] = ''
                item['likes'] = ''
                item['keyword'] = ''


                # 做时间判断部分---------------
                get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
                end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                if self.start_time != '':
                    start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                else:
                    start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                # if float(get_news_time) < float(start_time):
                #     # self.is_work = False
                #     # return
                #     pass

                if float(start_time) <= float(get_news_time) <= float(end_time):  # 符合时间段的内容
                    print(item)
                    self.write_news_jsonfile(item)
                    self.get_comment_info(url, title, date, create_time, ip)
                else:
                    print(item)
                    print('不符合抓取时间段的文章 URL:{}'.format(url))
                if float(get_news_time) > float(end_time):
                    with open('{}_url.txt'.format(now_time), 'a') as f:
                        f.write(url + '\n')
            except AttributeError:
                print('问答类网页', url)
                self.questions_list.append(url)
                print(self.questions_list)

        else:
            print('网页404错误', url)

    # 获取评论
    # http://lf.snssdk.com/article/v1/tab_comments/?count=50&item_id=6629460454148145678&group_id=6629460454148145678&offset=0
    def get_comment_info(self, source_url, source_title, source_date, source_time, ip, page_id="0"):
        item = dict()
        user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
        ]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            'Host': 'lf.snssdk.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': '{}'.format(random.choice(user_agent))
        }

        url_id = source_url.split('/')[-1][1:]
        comment_url = 'http://lf.snssdk.com/article/v1/tab_comments/?count=50&item_id={}&group_id={}&offset={}'.format(url_id, url_id, page_id)
        print('评论爬取中......')
        print(comment_url)
        # ip = random.choice(self.proxies)
        try:
            response = requests.get(comment_url, headers=headers, proxies={'https': ip})  # , proxies={'https': ip}
            datas = json.loads(response.content)
            print(datas)
            data_list = datas['data']
            if data_list:
                for comment in data_list:
                    item['platform'] = '今日头条'
                    item['source_date'] = source_date
                    item['source_time'] = source_time

                    content = comment['comment']['text']
                    date_all = comment['comment']['create_time']
                    # #转换成localtime
                    time_local = time.localtime(float(str(date_all)))
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    date = dt.split(' ')[0]
                    comment_time = dt.split(' ')[1]
                    item['date'] = date
                    item['time'] = comment_time
                    item['title'] = source_title
                    author = comment['comment']['user_name']
                    item['author'] = author
                    item['content'] = content
                    item['source_url'] = source_url
                    item['comment_url'] = comment_url
                    item['floor'] = ''
                    item['views'] = ''
                    item['comments_count'] = ''
                    item['keyword'] = ''
                    item['likes'] = ''
                    print('写入评论中......')
                    self.write_comment_jsonfile(item)
                if len(data_list) == 50:
                    page_id = int(page_id) + 50
                    print('爬取评论翻页信息.....')
                    time.sleep(2)
                    self.get_comment_info(source_url, source_title, source_date, source_time, ip, page_id=str(page_id))
        except requests.exceptions.ConnectionError:
            print('获取评论时发生链接错误,程序暂停100s后爬取')
            time.sleep(100)
            self.get_comment_info(source_url, source_title, source_date, source_time, ip, page_id=str(page_id))
            logging.error('获取评论时发生链接错误,程序暂停100s后爬取，get_comment error:{}'.format(traceback.format_exc()))


    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../toutiao/history_toutiao_newsfile.json', 'ab') as f:  # 将新闻数据写入一个总的历史数据文件
            f.write(item.encode("utf-8"))

        with open('./../toutiao/24_{}_toutiao_news.json'.format(str(now_time)), 'ab') as f:  # 新的数据文件
            f.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../toutiao/history_toutiao_commentfile.json', 'ab') as f:  # 将评论数据写入一个总的历史数据文件
            f.write(item.encode("utf-8"))

        with open('./../toutiao/38_{}_toutiao_comment.json'.format(str(now_time)), 'ab') as f:  # 新的数据文件
            f.write(item.encode("utf-8"))

    def run(self):

        for url in open('./../toutiao/new_url_file.json'):
            if self.ip_count < 150:
                url = url.strip()
                print('一个爬虫正在爬取网址{}'.format(url))
                logger.info('一个爬虫正在爬取网址{}'.format(url))
                try:
                    self.get_news_page(url, self.ip)
                except requests.exceptions.ProxyError:
                    print('远程连接无响应，重试一次中.......', )
                    try:
                        if self.ip_count < 150:
                            print('更换ip中......')
                            self.ip = proxies.res_ip()
                            self.ip_count += 1
                            self.get_news_page(url, self.ip)
                        else:
                            self.get_news_page(url, self.ip)
                    except requests.exceptions.ProxyError:
                        print('重试链接....远程连接无响应......')
                except Exception as e:
                    print('发生其他异常{}'.format(e))
                    print('更换ip中......')
                    time.sleep(10)
                    self.ip = proxies.res_ip()
                    self.ip_count += 1
                    try:
                        self.get_news_page(url, self.ip)
                    except:
                        pass
                time.sleep(1)
                print('一个网址爬虫结束.....')
            else:
                print('使用ip已达到{}个'.format(str(self.ip_count)) + ',爬虫停止运行......')
                break
        logger.info('爬取完毕......')

if __name__ == "__main__":
    toutiao = TouTiaoSpider()
    toutiao.run()
