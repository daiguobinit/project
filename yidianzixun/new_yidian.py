import requests
from lxml import etree
import json
import re
import math
import time
import ast
import execjs
import random
from datetime import datetime, date, timedelta
import logging
import proxies
import traceback


# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../yidianzixun/yidianzixun-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class YiDianSpider(object):

    def __init__(self):
        self.headers_one = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            # 'Connection':'keep-alive',
            'Cookie':'cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%2216730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201542776168%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201542776168%7D%7D; UM_distinctid=16730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461; JSESSIONID=208cee9fea61049d61e7d18f9e9c275ecf530a9e308a94dde36658adc01a0594; wuid=154945905891357; wuid_createAt=2018-11-21 12:56:9',
            'Host':'www.yidianzixun.com',
            'Referer':'http://www.yidianzixun.com/channel/c11',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        self.proxies = ['218.95.55.154:4243']

        # 去重列表
        self.set_list = []
        #
        self.error_url_list = []

        # cookies池和id池
        '''
            {
                'channel_id': '',
                'cookies': ''
            },
        '''

        # 通过系统时间自动计算时间间隔
        date = datetime.now() - timedelta(days=3)  # 七天前的时间，不包括今天，
        str_time = str(date).split(' ')[0]

        yesterday = datetime.now() - timedelta(days=1)  # 昨天时间

        now_time = str(yesterday).split(' ')[0]
        print('爬取时间段：{}到{}'.format(str_time, now_time))

        logging.info('爬取时间段：{}到{}'.format(str_time, now_time))
        # 定义开始时间 y-m-d  离现在时间远
        self.start_time = str_time
        # 定义结束时间 y-m-d  离现在时间近
        self.end_time = now_time
        try:
            self.page_ip = proxies.res_ip()
            # self.page_ip = '115.219.77.241:2316'
        except:
            time.sleep(3)
            print('调用ip时发生错误：{}'.format(traceback.format_exc()))
            logger.error('调用ip时发生错误：{}'.format(traceback.format_exc()))
            self.page_ip = proxies.res_ip()
        self.ip_count = 0

    def get_channel_id(self):
        url = 'http://www.yidianzixun.com/channel/c11'
        try:
            response = requests.get(url, proxies={'http': self.page_ip})
            data = response.content.decode()
            data = re.search('channel_id(.*?)汽车', data).group(0)
            channel_id = re.search('\d{8,15}', data).group(0)
            cokies = response.headers['Set-Cookie']
            print(cokies)
            id = re.search('JSESSIONID=([a-z0-9]{30,80});', cokies).group(1)

            return channel_id, id
        except:
            if self.ip_count < 100:
                self.page_ip = proxies.res_ip()
                self.ip_count += 1
                self.get_channel_id()
            else:
                raise IndexError

    def get_news_list_port(self, url, params, cookie, ip):
        self.headers_one['Cookie'] = cookie
        response = requests.get(url, params=params, headers=self.headers_one, proxies={'https': ip})
        print(response.url)
        data = response.content.decode()
        data = json.loads(data)
        data = data['result']
        print(data)
        if data:
            for news in data:
                item = {}
                title = news['title']
                item['title'] = title
                itemid = news['itemid']
                url = 'http://www.yidianzixun.com/article/' + itemid
                news_date = news['date']
                get_date = re.search('\d{4}-\d{2}-\d{2}', news_date).group(0)
                if 'V_' not in itemid:
                    if url not in self.set_list:
                        # self.write_news_jsonfile(item)
                        try:
                            print(url)
                            self.get_news_page_info(url)
                            self.set_list.append(url)
                        except IndexError:
                            print('网页解析错误', url, 111111)
                            self.error_url_list.append(url)
                            self.page_ip = proxies.res_ip()
                            time.sleep(10)
                            print('更换ip：', self.page_ip)
        else:
            time.sleep(10)
            print('重试中......')
            self.page_ip = proxies.res_ip()

            self.get_news_list_port(url, params, cookie, ip)

    # 获取通过js生成的spt的值
    def get_spt(self, start, channel_id):
        # start = 10
        end = start + 10
        n = "/home/q/news_list_for_channel?channel_id=11756176923&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5"
        e = str(channel_id)
        ctx = execjs.compile(
            '''
            function good (n,e,i,t){
                for (var o = "sptoken", a = "", c = 1; c < arguments.length; c++){
                    o += arguments[c];
                }
                for (var c = 0; c < o.length; c++) {
                    var r = 10 ^ o.charCodeAt(c);
                    a += String.fromCharCode(r)
                }
                return a
            }
            '''
        )
        spt = ctx.call('good', n, e, start, end)
        return spt

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
        if date_all == '昨天' or date_all == '2天前':
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
        url = 'http://www.yidianzixun.com/home/q/getcomments?_=1542864983174&docid={}&s=&count=30&last_comment_id={}&appid=web_yidian'.format(str(news_id), last_comment_id)
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

        url = 'http://www.yidianzixun.com/home/q/news_list_for_channel'
        # 1542 7036 63.23 22059
        get_time = time.time()
        get_time = ''.join(str(get_time).split('.'))
        get_time = get_time[:-2]


        # channel_id = 11810267522
        # for tool in self.tool_list:
        # channel_id = tool['channel_id']
        # cookie = tool['cookies']
        # ip = self.proxies[0]
        start = 0
        for i in range(1, 60):
            time.sleep(60)
            try:
                # channel_id, jession_id = self.get_channel_id()
                # print(channel_id)
                for j in range(20):
                    channel_id, jession_id = self.get_channel_id()
                    print(channel_id)
                    # tool = random.choice(self.tool_list)
                    cookie = 'JSESSIONID={}; wuid=955594968988162; wuid_createAt=2018-12-28 9:23:51; weather_auth=2; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1545960232; UM_distinctid=167f26914dc782-0cf8055a8c462f-5d1e331c-15f900-167f26914dd486; CNZZDATA1255169715=841120563-1545955593-null%7C1545955593; captcha=s%3A6cb2d7fd90216ee034e5063e173e8bd8.ytEeuzpbuzDpjq0fMjQB99MS3QYW4tagEAy6RClglQc; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1545960241; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%22167f26914dc782-0cf8055a8c462f-5d1e331c-15f900-167f26914dd486%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201545960240%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201545960240%7D%7D'.format(jession_id)
                    ip = self.page_ip
                    # try:

                    spt = self.get_spt(start, channel_id)
                    print(spt)
                    end = start + 10
                    params = {
                        'channel_id': channel_id,
                        'cstart': start,
                        'cend': end,
                        'infinite': 'true',
                        'refresh': '1',
                        '__from__': 'pc',
                        'multi': '5',
                        '_spt': spt,
                        'appid': 'web_yidian',
                        '_': get_time
                    }
                    self.get_news_list_port(url, params, cookie, ip)
                    start += 10
                    # except:
                    #     pass
            except TypeError:
                time.sleep(10)
                logger.error('内容解析错误',traceback.format_exc(), 222222)
            except:
                logger.error('其他错误', traceback.format_exc())
        print(list(set(self.error_url_list)))
        logger.info('爬虫爬取完毕......')

if __name__ == "__main__":
    yidian = YiDianSpider()
    try:
        yidian.run()
    except:
        logger.error(traceback.format_exc())
