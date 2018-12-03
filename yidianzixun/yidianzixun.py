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


class YiDianSpider(object):

    def __init__(self):
        self.headers_one = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%2216730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201542776168%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201542776168%7D%7D; UM_distinctid=16730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461; JSESSIONID=208cee9fea61049d61e7d18f9e9c275ecf530a9e308a94dde36658adc01a0594; wuid=154945905891357; wuid_createAt=2018-11-21 12:56:9',
            'Host':'www.yidianzixun.com',
            'Referer':'http://www.yidianzixun.com/channel/c11',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
        self.proxies = ['115.223.195.15:9000']
        # 打开json文件
        self.news_jsonfile = open('./yidian_newsfile.json', 'wb')
        self.comment_jsonfile = open('./yidian_commentfile.json', 'wb')
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
        self.tool_list = [
            {
                'channel_id': '11976187579',
                'cookies': 'JSESSIONID=183ead48983c4d295722fc172f1415f63e90dda8a8f2bbf3663fcef3e74e2d78; wuid=291715094685181; wuid_createAt=2018-11-23 9:04:22; weather_auth=2; captcha=s%3A020e96978e400d130be11b25bb1c6631.lc2FPVtjQrZeLZuB%2BTRXzjyR%2FHZ1km%2F3hP7IRvK9Ntw; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1542935063; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1542935063; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%2216730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201542935061%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201542935061%7D%7D; UM_distinctid=16730471952668-0ecf0ba7ae41cb-414f0120-15f900-16730471953461; CNZZDATA1255169715=1281590818-1542931366-%7C1542931366'
            },
        ]

    def get_channel_id(self, url):
        response = requests.get(url)
        data = response.content.decode()
        data = re.search('channel_id(.*?)汽车', data).group(0)
        channel_id = re.search('\d{8,15}', data).group(0)
        return channel_id

    def get_news_list_port(self, url, params, cookie, ip):
        self.headers_one['Cookie'] = cookie
        response = requests.get(url, params=params, headers=self.headers_one, proxies={'https': ip})
        print(response.url)
        data = response.content.decode()
        data = json.loads(data)
        data = data['result']
        for news in data:
            item = {}
            title = news['title']
            item['title'] = title
            itemid = news['itemid']
            url = 'http://www.yidianzixun.com/article/' + itemid
            news_date = news['date']
            get_date = re.search('\d{4}-\d{2}-\d{2}', news_date).group(0)
            print(get_date)
            if 'V_' not in itemid:
                if url not in self.set_list:
                    # self.write_news_jsonfile(item)
                    try:
                        print(url)
                        self.get_news_page_info(url)
                        self.set_list.append(url)
                    except IndexError:
                        print('网页解析错误', url)
                        self.error_url_list.append(url)

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

        try:
            date_all = data.xpath('.//div[@class="meta"]/span[2]/text()')
            if date_all == '昨天':
                yesterday = date.today() + timedelta(days=-1)
                item['date'] = yesterday
        except:
            today = date.today() + timedelta()
            item['date'] = today
        item['time'] = ''
        item['likes'] = ''
        item['clicks'] = ''
        item['views'] = ''
        item['keyword'] = ''
        item['commnets_count'] = ''
        self.write_news_jsonfile(item)
        news_id = url.split('/')[-1]
        self.get_commnet_info(news_id, title, url)

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
                content = comment['comment']
                item['content'] = content
                author = comment['nickname']
                item['author'] = author
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
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        print('正在写入评论数据......')
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.comment_jsonfile.write(item.encode("utf-8"))

    def close_file(self):
        self.news_jsonfile.close()
        self.comment_jsonfile.close()

    def run(self):

        url = 'http://www.yidianzixun.com/home/q/news_list_for_channel'
        # 1542 7036 63.23 22059
        get_time = time.time()
        get_time = ''.join(str(get_time).split('.'))
        get_time = get_time[:-2]
        # first_url = 'http://www.yidianzixun.com/channel/c11'
        # channel_id = self.get_channel_id(first_url)

        # channel_id = 11810267522
        t = 0
        for tool in self.tool_list:
            channel_id = tool['channel_id']
            cookie = tool['cookies']
            ip = self.proxies[t]
            t += 1
            for j in range(1, 30):
                for i in range(1, 10):
                    # try:
                    start = 0
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
                    # except:
                    #     pass
        self.close_file()
        print(list(set(self.error_url_list)))


if __name__ == "__main__":
    yidian = YiDianSpider()
    yidian.run()
