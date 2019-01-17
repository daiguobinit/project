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
file_name = r"./../hupu/hupu-{}.log".format(str(datetime.now()).split(' ')[0])
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
    """
    这是一个爬虫模板
    """
    def __init__(self, day=3):

        self.headers_one = {

        }
        self.start_url = ''
        # 评论接口模板
        self.commnet_port_url = ''
        # # 打开json文件
        # self.news_jsonfile = open('./sina_newsfile.json', 'wb')
        # self.comment_jsonfile = open('./sina_commentfile.json', 'wb')
        # 通过系统时间自动计算时间间隔
        date = datetime.now() - timedelta(days=day)  # 七天前的时间，不包括今天
        str_time = str(date).split(' ')[0]

        yesterday = datetime.now() - timedelta(days=1)  # 昨天时间

        now_time = str(yesterday).split(' ')[0]
        print('爬取时间段：{}到{}'.format(str_time, now_time))

        logging.info('爬取时间段：{}到{}'.format(str_time, now_time))
        # 定义开始时间 y-m-d  离现在时间远
        self.start_time = str_time
        # 定义结束时间 y-m-d  离现在时间近
        self.end_time = now_time
        # 标记爬虫工作
        self.is_work = True

    def get_forum_list(self, url):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'PHPSESSID=da8474303baac9d465965911aae4c69e; _dacevid3=c6b2c5bd.ab53.710d.1951.0a871bffb6f4; _cnzz_CV30020080=buzi_cookie%7Cc6b2c5bd.ab53.710d.1951.0a871bffb6f4%7C-1; __gads=ID=b57c7251f1ea8930:T=1544583356:S=ALNI_Mbh5oNFJOGikKCFOFsu9ZXWiDcfDQ; _fmdata=LDwCdQHpXdYXGJD3j0882yMyZP5Ivi4MbR2dSu%2FradlbJxKKEt5yIqZNq5noEZHoUwkCLCi1yul3Ntn7n2TqOcKBVtJSJ%2BW0Re4uaC%2Fug8M%3D; _HUPUSSOID=1eb0b12b-e700-478e-b8c4-7d40c4c4b62b; _CLT=b0c2a05996d8b48b354e1fa4ddfc1fef; u=42101303|5ZWm5ZWm5Y2h5Y2h5Y2h5ZWm|7dbb|d72e6b442fce2e4bb3ce5ef39b4990bb|2fce2e4bb3ce5ef3|aHVwdV9iNTkwZGVhNTJiZmEwNTNk; us=8850633673843fdaf6fbda6052428be4782b38fdf9cb1e24a7be78b591ef21b497db3e03f3af039ea75a35cb55547d23bca3d6205193b6b59f81716866d5d8f9; ua=386146240; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1544583357,1544583591,1544584976; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1544585177; __dacevst=3d855dc7.4e206a33|1544592183554',
            'referer': 'https://bbs.hupu.com/cars-98',
            'Connection': 'close',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }
        print(url)
        logging.info('爬取论坛页url:{}'.format(url))
        response = requests.get(url, headers=headers)
        data = response.content.decode()
        data = etree.HTML(data)
        # .//ul[@class="for-list"]/li[1]/div[1]/a[2]/@href
        li_list = data.xpath('.//ul[@class="for-list"]/li')
        for li in li_list:  # 提取论坛页面帖子的信息
            try:
                url_html = li.xpath('.//a[@class="truetit"]/@href')[0]
                views = li.xpath('.//span[@class="ansour box"]/text()')[0].strip()
                date = li.xpath('.//div[2]/a[2]/text()')[0]
                author = li.xpath('.//div[2]/a[1]/text()')[0]
                print(date, author)
                posted_url = 'https://bbs.hupu.com/' + url_html

                # 做时间判断部分---------------
                get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
                end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                if self.start_time != '':
                    start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                else:
                    start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                if float(get_news_time) < float(start_time):
                    if url != 'https://bbs.hupu.com/cars-postdate':  # 论坛首页不做时间判断
                        self.is_work = False
                        logging.info('帖子时间小于指定时间，停止往下爬取, URL:'+posted_url)
                        break
                elif float(start_time) <= float(get_news_time) <= float(end_time):
                    max_page = self.get_posted_page(posted_url, views)  # 获取帖子的详情页
                    logging.info('爬取URL：{}'.format(posted_url))
                    if int(max_page) > 1:  # 判断帖子的翻页数，是否进行翻页操作
                        for j in range(2, int(max_page) + 1):
                            time.sleep(2)
                            page_url = posted_url.split('.html')[0]
                            next_page_url = page_url + '-' + str(j) + '.html'
                            self.get_posted_page(next_page_url, views)
                            logging.info('爬取URL：{}'.format(posted_url))
                else:
                    logging.info('不符合时间的 url:'+posted_url)
            except:
                logging.error('爬取时出错:{}'.format(traceback.format_exc()))

    def get_posted_page(self, url,  views):
        headers = {
            ''
        }
        s = requests.session()
        s.keep_alive = False
        response = requests.get(url)
        print(url)
        logging.info(u'获取帖子的详细信息url:{}'.format(url))
        content = response.content.decode()
        if '由于数据量过大，服务器进行数据迁移' not in content:  # 有的帖子会报这样的错误
            data = etree.HTML(content)
            floor_list = data.xpath('.//form/div[@class="floor"]')
            max_page = data.xpath('.//h1/@data-maxpage')[0]  # 获取的帖子的翻页数
            print('共计{}页'.format(max_page))
            for floor in floor_list:
                have_floor = floor.xpath('.//div[@class="floor-show  "]')
                if have_floor:  # 判断楼层是否存在
                    item = {}
                    item['platform'] = '虎扑社区'
                    floor_num = floor.xpath('.//a[@class="floornum"]/@id')[0]
                    if int(floor_num) == 0:  # 楼层0的时候是楼主的帖子，xpath规则不同
                        text = floor.xpath('.//div[@class="quote-content"]//text()')
                        text = ''.join(text).strip()
                        is_topics = '是'
                        reply_no = str(views).split('/')[0].strip()
                        clicks = str(views).split('/')[1].strip()
                        likes = ''
                    else:  # 这是回帖内容的 xpath
                        text = floor.xpath('.//tr/td/text() | .//tr/td/p/text() | .//tr/td/br/text()')
                        text = ''.join(text).strip()
                        is_topics = '否'
                        reply_no = ''
                        clicks = ''
                        likes = floor.xpath('.//div[@class="left"]/span/span/span[@class="stime"]/text()')[0]

                    create_time = floor.xpath('.//div[@class="left"]/span[@class="stime"]/text()')[0]
                    item['date'] = create_time.split(' ')[0]
                    item['time'] = create_time.split(' ')[1]
                    author = floor.xpath('.//div[@class="left"]/a[@class="u"]/text()')[0]
                    item['author'] = author
                    title = floor.xpath('//*[@id="j_data"]/text()')[0]
                    item['title'] = title
                    item['keyword'] = ''
                    item['content'] = text
                    item['brand'] = ''
                    item['carseries'] = ''
                    item['from'] = ''
                    item['url'] = url
                    item['is_topics'] = is_topics
                    item['floor'] = floor_num
                    item['identification'] = '无'
                    item['signin_time'] = ''
                    item['reply_no'] = reply_no
                    item['views'] = clicks
                    item['likes'] = likes
                    self.write_news_jsonfile(item)
        else:
            max_page = 1

        return max_page

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../hupu/61_{}_hupu.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../hupu/hupu_commentfile_{}.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        url = 'https://bbs.hupu.com/cars-postdate'
        self.get_forum_list(url)
        for i in range(2, 10000):
            logging.info('进行论坛第{}翻页'.format(str(i)))
            if self.is_work:
                time.sleep(3)
                url = 'https://bbs.hupu.com/cars-postdate' + '-' + str(i)
                self.get_forum_list(url)
            else:
                print('爬取到指定时间，爬虫停止.....')
                logging.info('爬取到指定时间，爬虫停止.....')
                break


if __name__ == "__main__":
    spider = SinaSpider()
    spider.run()
