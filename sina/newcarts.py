import requests
from lxml import etree
import json
import re
import time
from datetime import datetime
from datetime import timedelta
import xlrd
import logging
import traceback

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../sina/sina-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class SinaSpider(object):
    def __init__(self):

        self.headers_one = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Cookie':'lxlrttp=1541383354; SUB=_2AkMsr_iof8NxqwJRmfkQzmLlaop3wg3EieKa8wlzJRMyHRl-yD8Xqk4YtRB6By_WR3ecEuiI3NBWzuzCv5vtVnmGKtsn; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFVyZLoounDZRKve7mPA8Ho',
            'Host':'auto.sina.com.cn',
            'Connection': 'close',
            'Referer':'http://auto.sina.com.cn/newcar/?page=1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        self.start_url = 'http://auto.sina.com.cn/newcar/?page={}'
        # 评论接口模板
        self.commnet_port_url = 'http://comment.sina.com.cn/page/info?version=1&format=json&channel=qc&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page={}&page_size=10&t_size=3&h_size=3&thread=1&callback=jsonp_1542676393124&_=1542676393124'
        # 评论页数
        self.page_num = 1
        # 新闻接口url模板78593
        self.news_url_port = 'http://interface.sina.cn/auto/inner/getAutoSubpageInfo.d.json?cid={}&pageSize=15&page={}&callback=jQuery172017229859039201645_1542683078100&_=1542683078171'
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

        # 新能源模块新闻数据接口的url模板
        self.energy_url = 'http://interface.sina.cn/auto/inner/getEstationHot.d.json?page={}&callback=jQuery1720805668580888633_1542692800702&_=1542692901640'

    # 获取新闻的url
    def get_news_url(self, url):
        response = requests.get(url)
        data = response.content.decode()
        data = data[42:][:-1]
        data = json.loads(data)
        data = data['data']
        data = etree.HTML(data)
        url_list = data.xpath('.//h3/a/@href')
        # print(url_list)
        # data = etree.HTML(response.content)
        # url_list = data.xpath('.//a[@class="more"]/@href')
        # url_list = url_list[1:]
        for news_url in url_list:
            if self.is_work:
                self.get_news_info(news_url)
            else:
                break

    # 获取新闻详情页
    def get_news_info(self, url):
        print(url)
        item = dict()
        response = requests.get(url, headers=self.headers_one)
        try:
            data = etree.HTML(response.content)
            # 网站
            item['platform'] = '新浪新闻'
            # 标题
            title = data.xpath('.//h1[@class="main-title"]/text()')[0]
            item['title'] = title
            date_all = data.xpath('.//div[@class="date-source"]/span/text()')[0]
            date = date_all.split(' ')[0]
            news_time = date_all.split(' ')[1]
            item['date'] = date
            item['time'] = news_time
            # 来源作者
            source_author = data.xpath('.//div[@class="date-source"]/a/text()')[0]
            item['source_author'] = source_author
            # 内容
            content = data.xpath('.//div[@id="article_content"]/div[1]/div/p/text()')
            content = ''.join(content)
            # 翻页数据
            next_page = data.xpath('.//div[@data-sudaclick="content_pagination_p"]/a/@href')
            if len(next_page) > 3:
                next_page = next_page[1:][:-2]
                for page_url in next_page:
                    print('获取翻页数据')
                    next_content = self.get_next_page(page_url)
                    content = content + next_content

            item['content'] = content

            # 从接口处获取评论数
            news_id = re.search('(\w{7}\d{7})', url).group(0)
            try:
                comment_count = self.get_commnet_count(news_id)
            except AttributeError:
                comment_count = '0'
            item['comments_count'] = comment_count
            item['clicks'] = ''
            item['views'] = ''
            item['likes'] = ''
            item['keyword'] = ''
            item['url'] = url

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

                self.write_news_jsonfile(item)
                if int(comment_count) > 0:
                    self.get_comments_info(news_id, title, date, news_time, url)
        except IndexError:
            print('网页请求404')

    # 获取翻页数据
    def get_next_page(self, url):
        response = requests.get(url, headers=self.headers_one)
        try:
            data = etree.HTML(response.content)
            # 内容
            content = data.xpath('.//div[@id="article_content"]/div[1]/div/p/text()')
            content = ''.join(content)
            return content
        except:
            content = ''
            return content

    # 获取评论数
    def get_commnet_count(self, news_id):
        response = requests.get(self.commnet_port_url.format(news_id, str(1)))
        data = response.content.decode()
        print(data)
        data = re.search('"qreply": \d{0,9}', data).group(0)
        comment_count = data.split(':')[1]
        return comment_count

    # 获取评论信息
    def get_comments_info(self, news_id, title, source_date, source_time, source_url, page_id="1"):
        item = {}
        url = self.commnet_port_url.format(news_id, page_id)
        response = requests.get(url)
        data = response.content.decode()
        # data = re.search(r'{"result.*}\)', data).group(0)
        data = data[20:][:-1]
        data = json.loads(data)
        comments_list = data['result']['cmntlist']
        if comments_list:
            for comment in comments_list:

                item['platform'] = '新浪新闻'
                item['source_date'] = source_date
                item['source_time'] = source_time
                date_all = comment['time']
                date = date_all.split(' ')[0]
                commnet_time = date_all.split(' ')[1]
                item['date'] = date
                item['time'] = commnet_time
                item['title'] = title
                author = comment['nick']
                item['author'] = author
                content = comment['content']

                item['content'] = content
                item['floor'] = ''
                item['keyword'] = ''
                item['source_url'] = source_url
                comment_url = 'http://comment5.news.sina.com.cn/comment/skin/default.html?channel=qc&newsid=comos-{}&group=0'.format(news_id)
                item['comment_url'] = comment_url
                item['views'] = ''
                item['comments_count'] = ''
                likes = comment['agree']
                item['likes'] = likes
                self.write_comment_jsonfile(item)
            self.page_num += 1
            self.get_comments_info(news_id, title, source_date, source_time, source_url, page_id=str(self.page_num))
        else:
            self.page_num = 1
            print('评论抓取完毕', url)
    # ------------------------------------------------新能源模块--------------------------------------------------------

    # 新能源模块数据获取
    def get_energy_url(self, url):
        response = requests.get(url)
        data = response.content.decode()
        data = data[40:][:-1]
        data = json.loads(data)
        data = data['data']
        for news in data:
            if self.is_work:
                url = news['url']
                self.get_energy_info(url)
            else:
                break

    def get_energy_info(self, url):
        item = {}
        print(url)
        if 'k.sina.com.cn' in url:
            try:
                response = requests.get(url)
                data = response.content
                data = etree.HTML(data)
                # 网站
                item['platform'] = '新浪新闻'
                # 标题
                title = data.xpath('.//h1[@class="main-title"]/text()')[0]
                item['title'] = title
                date_all = data.xpath('.//div[@class="date-source"]/span/text()')[0]
                date = date_all.split(' ')[0]
                news_time = date_all.split(' ')[1]
                item['date'] = date
                item['time'] = news_time
                # 来源作者
                source_author = data.xpath('.//div[@class="date-source"]/a/text()')[0]
                item['source_author'] = source_author
                # 内容
                content = data.xpath('.//div[@id="artibody"]/p/font/text()')
                content = ''.join(content)
                item['content'] = content
                # 翻页数据
                next_page = data.xpath('.//div[@data-sudaclick="content_pagination_p"]/a/@href')
                try:
                    if len(next_page) > 3:
                        next_page = next_page[1:][:-2]
                        for page_url in next_page:
                            print('获取翻页数据')
                            next_content = self.get_next_page(page_url)
                            content = content + next_content
                except:
                    print('翻页数据获取失败')
                # 从接口处获取评论数
                item['commnets_count'] = '0'
                item['clicks'] = ''
                item['views'] = ''
                item['likes'] = ''
                item['keyword'] = ''
                item['url'] = url
                # 做时间判断部分---------------
                get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
                end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                if self.start_time != '':
                    start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                else:
                    start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                if float(get_news_time) < float(start_time):
                    # self.is_work = False
                    return

                if float(start_time) <= float(get_news_time) <= float(end_time):
                    print('写入数据中......')
                    self.write_news_jsonfile(item)
            except:
                print('网页获取错误')

    # ------------------------------------------------------------------------------------------------------------------
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../sina/17_{}_sina_news.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../sina/31_{}_sina_comment.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))

    def run(self):
        # 新车模块
        for num in range(1, 35):
            if self.is_work:
                url = self.news_url_port.format('78593', str(num))
                print(url, '新闻列表页')
                self.get_news_url(url)
            else:
                break
        self.is_work = True
        # 试车模块
        for num in range(1, 35):
            if self.is_work:
                url = self.news_url_port.format('78603', str(num))
                print(url, '新闻列表页')
                self.get_news_url(url)
            else:
                break
        self.is_work = True
        # 导购模块
        for num in range(1, 35):
            if self.is_work:
                url = self.news_url_port.format('78584', str(num))
                print(url, '新闻列表页')
                self.get_news_url(url)
            else:
                break
        self.is_work = True
        # 新闻模块
        for num in range(1, 35):
            if self.is_work:
                url = self.news_url_port.format('78590', str(num))
                print(url, '新闻列表页')
                self.get_news_url(url)
            else:
                break
        self.is_work = True
        # 技术模块
        for num in range(1, 14):
            if self.is_work:
                url = self.news_url_port.format('78580', str(num))
                print(url, '新闻列表页')
                self.get_news_url(url)
            else:
                break

        self.is_work = True
        # 新能源模块 150
        for num in range(1, 200):
            if self.is_work:
                url = self.energy_url.format(str(num))
                print(url, '新闻列表页')
                self.get_energy_url(url)
            else:
                break
        logger.info('爬取完毕......')


if __name__ == "__main__":
    sina = SinaSpider()
    try:
        sina.run()
    except:
        logger.error(traceback.format_exc())
