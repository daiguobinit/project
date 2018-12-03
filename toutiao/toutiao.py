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
        # 打开json文件
        self.news_jsonfile = open('./toutiao_newsfile.json', 'wb')
        self.comment_jsonfile = open('./toutiao_commentfile.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-13'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-20'
        # 标记爬虫工作
        self.is_work = True
        # 评论页数
        self.comment_page_num = 1
        # 去重列表
        self.set_list = []
        # 代理ip
        self.proxies = [
           '58.218.92.128:18211'
        ]
        # 搜集问答类网页的列表
        self.questions_list = []

        # 读取url列表
        with open('./new_url_file.json', 'r') as f:
            self.url_list = f.readlines()

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

    def get_news_page(self, url):
        item = {}
        ip = random.choice(self.proxies)
        print(ip)
        response = requests.get(url, headers=self.headers_one, proxies={'https': ip})
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
                item['comment_count'] = comment_count
                item['clicks'] = ''
                item['likes'] = ''
                item['keyword'] = ''
                print(item)

                # # 做时间判断部分---------------
                # get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
                # end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                # if self.start_time != '':
                #     start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                # else:
                #     start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                # if float(get_news_time) < float(start_time):
                #     self.is_work = False
                #     return
                #
                # if float(start_time) <= float(get_news_time) <= float(end_time):
                self.write_news_jsonfile(item)
                self.get_comment_info(url, title, date, create_time)
            except AttributeError:
                print('问答类网页', url)
                self.questions_list.append(url)
                print(self.questions_list)

        else:
            print('网页404错误', url)

    # 获取评论
    # http://lf.snssdk.com/article/v1/tab_comments/?count=50&item_id=6629460454148145678&group_id=6629460454148145678&offset=0
    def get_comment_info(self, source_url, source_title, source_date, source_time, page_id="0"):
        item = dict()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'lf.snssdk.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        url_id = source_url.split('/')[-1][1:]
        comment_url = 'http://lf.snssdk.com/article/v1/tab_comments/?count=50&item_id={}&group_id={}&offset={}'.format(url_id, url_id, page_id)
        print('评论爬取中......')
        print(comment_url)
        response = requests.get(comment_url, headers=headers)
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
                item['url'] = comment_url
                item['floor'] = ''
                item['keyword'] = ''
                print('写入评论中......')
                self.write_comment_jsonfile(item)
            if len(data_list) == 50:
                page_id = int(page_id) + 50
                print('爬取评论翻页信息.....')
                self.get_comment_info(source_url, source_title, source_date, source_time, page_id=str(page_id))

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        # self.news_jsonfile.write(item.encode("utf-8"))
        with open('./toutiao_newsfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('./toutiao_commentfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))

    def close_file(self):
        self.news_jsonfile.close()
        self.comment_jsonfile.close()

    def run(self):
        for url in self.url_list:
            url = url.strip()
            print(url)
            try:
                self.get_news_page(url)
            except requests.exceptions.ProxyError:
                print('远程连接无响应，重试一次中.......', )
                try:
                    self.get_news_page(url)
                except requests.exceptions.ProxyError:
                    print('重试链接....远程连接无响应......')
            time.sleep(2.5)
        self.close_file()


if __name__ == "__main__":
    toutiao = TouTiaoSpider()
    toutiao.run()
