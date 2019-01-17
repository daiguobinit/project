import requests
from lxml import etree
import json
import re
import math
import time
import ast
from datetime import datetime
from datetime import timedelta
import logging
import traceback

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../tencent/tencent-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


# 新车模块爬虫
class NewCartsSpider(object):

    def __init__(self):
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'close',
            'Host':'auto.qq.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        self.comment_headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'close',
            'Host':'coral.qq.com',
            'Referer':'http://page.coral.qq.com/coralpage/comment/news.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        }

        # 评论回帖的headers
        self.reply_comment_headers = {
            ''
        }

        """
        新车模块：http://auto.qq.com/newcar.htm
        导购模块：http://auto.qq.com/guide.htm
        评测模块：http://auto.qq.com/evaluat.htm
        科技模块：http://auto.qq.com/tech.htm
        行业模块：http://auto.qq.com/news.htm
        """
        self.start_url = 'http://auto.qq.com/news.htm'
        self.newcart_port_url = 'http://coral.qq.com/article/3119727602/comment/v2?callback=_article3119727602commentv2&orinum=10&oriorder=o&pageflag=1&cursor=6448911923942977637&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1542093441225'
        self.some_url_list = []
        self.some_url_list_two = []

        # 评论数据接口url模板
        self.comment_port = 'http://coral.qq.com/article/{}/comment/v2?callback=_article{}commentv2&orinum=10&oriorder=o&pageflag=1&cursor={}&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1542161324292'
        # 标记评论数量的id
        self.cursor_comment = '0'
        # 标记评论回复的节点id
        self.comment_reply = '0'

        # 标记重复的url
        self.all_url_list = []
        # 通过系统时间自动计算时间间隔
        date = datetime.now() - timedelta(days=3)  # 七天前的时间，不包括今天
        str_time = str(date).split(' ')[0]

        yesterday = datetime.now() - timedelta(days=1)  # 昨天时间

        now_time = str(yesterday).split(' ')[0]
        print('爬取时间段：{}到{}'.format(str_time, now_time))

        logging.info('爬取时间段：{}到{}'.format(str_time, now_time))
        # 定义开始时间 y-m-d  离现在时间远
        self.start_time = str_time
        # 定义结束时间 y-m-d  离现在时间近
        self.end_time = now_time
        # 爬虫工作
        self.is_work = True



    # 新车模块的起始页面的数据
    def get_first_page(self, url):
        response = requests.get(url)
        data = etree.HTML(response.content)
        news_list = data.xpath('//*[@id="LIST_LM"]/li')
        for news in news_list:
            title = news.xpath('.//div[1]/h3/a/text()')[0]
            url = "http://auto.qq.com" + news.xpath('.//div[1]/h3/a/@href')[0]
            date_all = news.xpath('.//div[1]/div/h5/text()')[0]
            if self.is_work:
                self.get_news_page(url, title)
            else:
                break

    # 获取新闻详情页
    def get_news_page(self, url, title):
        if title not in self.all_url_list:
            self.all_url_list.append(title)
            item = {}
            response = requests.get(url, headers=self.headers)
            data = etree.HTML(response.content)
            text = response.text
            # print(text)
            id = re.findall(r'\d{10};', text)
            # 来源
            try:
                source_author = data.xpath('.//span[@class="a_source"]/a/text()')[0]
            except IndexError:
                if data.xpath('.//span[@class="a_source"]/text()'):
                    source_author = data.xpath('.//span[@class="a_source"]/text()')[0]
                elif data.xpath('.//span[@bosszone="jgname"]/a/text()'):
                    source_author = data.xpath('.//span[@bosszone="jgname"]/a/text()')[0]
                else:
                    source_author = data.xpath('.//span[@bosszone="jgname"]/text()')[0]

            # 日期时间
            if data.xpath('.//span[@class="a_time"]/text()'):
                date_all = data.xpath('.//span[@class="a_time"]/text()')[0]
            else:
                date_all = data.xpath('.//span[@class="article-time"]/text()')[0]
            date = date_all.split(' ')[0]

            # 做时间判断部分---------------
            get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
            end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
            if self.start_time != '':
                start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
            else:
                start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
            if float(get_news_time) < float(start_time):
                self.is_work = False
                return

            if float(start_time) <= float(get_news_time) <= float(end_time):

                item['date'] = date
                news_time = date_all.split(' ')[1]
                item['time'] = news_time
                item['source_author'] = source_author
                # 网站
                item['platform'] = '腾讯新闻'
                # 标题
                item['title'] = title

                # 正文
                if data.xpath('.//div[@bosszone="content"]/p/text()'):
                    content = data.xpath('.//div[@bosszone="content"]/p/text()')
                else:
                    content = data.xpath('.//div[@bosszone="content"]/p/text()')
                content = ''.join(content)
                item['content'] = content
                # print(item)
                # 获取评论信息---------------------------------
                if id == []:
                    comment_count = ''
                else:
                    comment_count = self.get_comment_info(id[0], url, date, news_time, title)
                print('*********************************')
                item['comments_count'] = comment_count
                item['clicks'] = ''
                item['views'] = ''
                item['likes'] = ''
                item['keyword'] = ''
                item['url'] = url
                print('一个新闻抓取完成', '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                self.write_news_jsonfile(item)

    # 获取接口处的新闻数据, 几口的历史数据
    def get_news_from_port(self):
        url = 'http://cgi.data.auto.qq.com/php/index.php?mod=carnews&act=carsdaily&year=2018&sort=1&callback=jQuery110202152556609837435_1542256112458&_=1542256112460'
        response = requests.get(url)
        data = response.content.decode()
        data = re.findall(r'{"status[\s\S]*"total":\d{3}}', data)[0]
        data = json.loads(data)
        data = data['data']
        for news in data:
            title = news['FTitle']
            news_url = news['FUrl']
            if self.is_work:
                self.get_news_page(news_url, title)
            else:
                break


    # 获取评论信息
    def get_comment_info(self, comment_id, source_url, source_date, cource_time, source_title):
        comment_id = comment_id.split(';')[0]
        comment_count = self.get_comment_from_port(comment_id,  source_url, source_date, cource_time, source_title)
        return comment_count

    # 从数据接口获取评论  主评论
    def get_comment_from_port(self, comment_id, source_url, source_date, cource_time, source_title, cursor='0'):
        item = {}
        # self.comment_port = 'http://coral.qq.com/article/{}/comment/v2?callback=_article{}commentv2&orinum=10&oriorder=o&pageflag=1&cursor={}&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1542161324292'
        url = self.comment_port.format(comment_id, comment_id, cursor)
        print(url, '主评论--------------------')
        response = requests.get(url, headers=self.comment_headers)
        data = response.content.decode()
        data = re.findall(r'{"errCode[\s\S]*{"time":\d{10}}}', data)[0]
        data = json.loads(data)
        if str(data['errCode']) == '100':
            print(data, '错误----------------------')
            comment_count = ''
            return comment_count
        else:
            comment_count = data['data']['targetInfo']['commentnum']
            print(comment_count)
            if int(comment_count) != 0:
                # 获取接口数据中的评论信息列表
                comment_list = data['data']['oriCommList']
                user_list = data['data']['userList']
                has_next = data['data']['hasnext']
                for comment in comment_list:
                    # 评论的回帖数量
                    orireplynum = comment['orireplynum']
                    # 评论时间
                    comment_time = comment['time']
                    date_all = time.localtime(int(comment_time))
                    date_all = time.strftime("%Y-%m-%d %H:%M:%S",date_all)
                    # 网站
                    item['platform'] = '腾讯新闻'
                    item['date'] = date_all.split(' ')[0]
                    item['time'] = date_all.split(' ')[1]
                    # 评论内容
                    content = comment['content']
                    item['content'] = content
                    item['keyword'] = ''
                    item['floor'] = ''
                    item['views'] = ''
                    item['comments_count'] = ''

                    # 作者author
                    user_id = comment['userid']
                    user_info = user_list[user_id]
                    user_name = user_info['nick']
                    item['author'] = user_name

                    # 点赞数
                    likes = comment['up']
                    item['likes'] = likes
                    # 原文发布日期时间
                    item['source_date'] = source_date
                    item['source_time'] = cource_time
                    # 原文标题
                    item['title'] = source_title
                    # 原文url
                    item['source_url'] = source_url
                    # 评论url
                    item['comment_url'] = 'http://coral.qq.com/'+comment_id


                    print(item, '1111111111111111111111111111111111')
                    self.write_comment_jsonfile(item)


                    # 获取子评论信息模块代码， 即评论的评论
                    # 用户评论标记ID
                    # get_comment_id = comment['id']
                    # if int(orireplynum) != 0:
                    #     comment_reply_url = 'http://coral.qq.com/comment/{}/reply/v2?callback=_comment{}replyv2&targetid={}&reqnum=10&pageflag=2&source=1{}&_=1542183535325'.format(get_comment_id, get_comment_id, comment_id, '')
                    #     print(comment_reply_url, '############################################')
                    #     # 获取子评论数据
                    #     self.get_comment_reply(comment_reply_url, get_comment_id, comment_id, source_url, source_date, cource_time, source_title)

                self.cursor_comment = cursor
                # 获取剩下评论的指针信息
                if has_next:
                    get_cursor = data['data']['last']
                    print(get_cursor)
                    self.get_comment_from_port(comment_id, source_url, source_date, cource_time, source_title, cursor=get_cursor)
            return comment_count


    # 获取评论的回帖信息    子评论
    def get_comment_reply(self, url, get_comment_id, comment_id, source_url, source_date, cource_time, source_title, cursor=''):
        print(url, '============================')
        item = {}
        response = requests.get(url, headers=self.comment_headers)
        data = response.content.decode()
        data = re.findall(r'{"errCode[\s\S]*{"time":\d{10}}}', data)[0]
        data = json.loads(data)
        rep_comment_list = data['data']['repCommList']
        user_list = data['data']['userList']
        last_id = data['data']['last']
        has_next = data['data']['hasnext']
        if rep_comment_list:
            for rep_comment in rep_comment_list:
                # 评论的回帖数量
                # orireplynum = rep_comment['orireplynum']
                # 评论时间
                comment_time = rep_comment['time']
                date_all = time.localtime(int(comment_time))
                date_all = time.strftime("%Y-%m-%d %H:%M:%S", date_all)
                item['platform'] = '腾讯新闻'
                item['date'] = date_all.split(' ')[0]
                item['time'] = date_all.split(' ')[1]
                # 评论内容
                content = rep_comment['content']
                item['content'] = content
                item['keyword'] = ''
                item['floor'] = ''
                item['views'] = ''
                item['comments_count'] = ''

                # 作者author
                user_id = rep_comment['userid']
                user_info = user_list[user_id]
                user_name = user_info['nick']
                item['author'] = user_name

                # 点赞数
                likes = rep_comment['up']
                item['likes'] = likes
                # 原文发布日期时间
                item['source_date'] = source_date
                item['cource_time'] = cource_time
                # 原文标题
                item['title'] = source_title
                # 原文url
                item['source_url'] = source_url
                # 评论url
                item['comment_url'] = 'http://coral.qq.com/' + comment_id
                print(item, 22222222222222222222222222222222222222)
                self.write_comment_jsonfile(item)
        if has_next:
            url = 'http://coral.qq.com/comment/{}/reply/v2?callback=_comment{}replyv2&targetid={}&reqnum=10&pageflag=2&source=1{}&_=1542183535325'.format(get_comment_id, get_comment_id, comment_id, '&cursor=' + last_id)
            self.get_comment_reply(url, get_comment_id, comment_id, source_url, source_date, cource_time, source_title,)

    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../tencent/18_{}_tencent_news.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../tencent/32_{}_tencent_commnet.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))


    def run(self):
        # 新车模块
        url_list = ['http://auto.qq.com/newcar.htm',
        'http://auto.qq.com/guide.htm',
        'http://auto.qq.com/evaluat.htm',
        'http://auto.qq.com/tech.htm',
        'http://auto.qq.com/news.htm'
                    ]
        for url in url_list:
            print(url)
            self.is_work = True
            self.get_first_page(url)
        # self.get_news_from_port()
        logger.info('爬取完毕......')


if __name__ == "__main__":
    newcarts = NewCartsSpider()
    newcarts.run()
