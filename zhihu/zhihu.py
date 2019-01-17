import requests
from lxml import etree
import json
import re
import math
import time
import ast
from datetime import datetime
from datetime import timedelta
import xlrd
import logging
import traceback
import random
import proxies


# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./../zhihu/zhihu-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)
now_time = str(datetime.now()).split(' ')[0].replace('-', '_')


class ZhiHuSpider(object):
    """
    知乎爬虫，根据关键字进行搜索，爬取一周内的信息
    """
    def __init__(self):

        self.headers_one = {

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
        self.is_stop = False
        # 翻页计数
        self.page_count = 0
        # 楼层计数
        self.floor_num = 1

        # 去重列表
        self.set_list = []

        self.ip = proxies.res_ip()

        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
        ]

    # 获取知乎列表页
    def get_questions_list_page(self, url, params, keyword):
        """
        知乎搜索出来的列表页，其中包含问答类信息和文章类信息，所以在函数中页做出了适当的判断
        :param url:
        :param params: 参数
        :return:
        """

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            # 'referer': 'https://www.zhihu.com/search?q=%E5%AE%9D%E9%A9%AC&range=1w&type=content',
            'User-Agent': '{}'.format(random.choice(self.user_agent))
        }
        response = requests.get(url, headers=headers, params=params, proxies={'http':self.ip})
        print('正在抓取主链接:', response.url)
        print(111, response.content.decode())
        data = response.content.decode()
        data = json.loads(data)
        if data['data']:  # 判断获取的json数据中的data['data']的value列表是否为空，可以间接判断是否还有下一页数据
            if len(data['data']) > 1:
                data_list = data['data'][1:]
            else:
                data_list = data['data']
            for news in data_list:
                question_title = news['highlight']['title'].replace('<em>', '').replace('</em>', '')
                news_type = news['object']['type']
                # 时间判断

                if news_type == 'answer':  # 问答类信息
                    answers_url = news['object']['url']
                    question_url = news['object']['question']['url']
                    question_id = question_url.split('/')[-1]

                    url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset={}&sort_by=created'.format(question_id, '0')
                    print(url)
                    # 传入页面的url
                    source_url = 'https://www.zhihu.com/question/{}/answers/created'.format(str(question_id))
                    if source_url not in self.set_list:  # 对url进行简单的去重，避免重复的工作量
                        self.get_answers_page(url, question_title, source_url, keyword)
                        self.set_list.append(source_url)
                elif news_type == 'article':  # 文章类信息

                    item = {}
                    content = news['object']['content']
                    # item['type'] = '文章'
                    item['platform'] = '知乎'
                    crt_time = news['object']['created_time']
                    # #转换成localtime
                    time_local = time.localtime(float(crt_time))
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # "%Y-%m-%d %H:%M:%S"
                    date = dt.split(' ')[0]
                    news_time = dt.split(' ')[1]
                    item['date'] = date
                    item['time'] = news_time
                    author = news['object']['author']['name']
                    item['author'] = author
                    item['title'] = question_title
                    # content = news['content'].replace('<p>', '').replace('</p>', '').replace('<br>', '')
                    content = etree.HTML(content)
                    content = content.xpath('.//p//text()')
                    content = ''.join(content)
                    item['content'] = content
                    articles_url = news['object']['url'].split('/')[-1]
                    item['url'] = 'https://zhuanlan.zhihu.com/p/{}'.format(str(articles_url))
                    item['is_topics'] = '是'
                    item['floor'] = 0
                    item['keyword'] = keyword
                    comments_count = news['object']['comment_count']
                    item['comments_count'] = comments_count
                    item['views'] = ''
                    likes = news['object']['voteup_count']
                    item['likes'] = str(likes)

                    # 做时间判断部分---------------  这个部分区分于另外一个部分
                    get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
                    end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                    if self.start_time != '':
                        start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                    else:
                        start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                    if float(get_news_time) < float(start_time):
                        pass
                    if float(start_time) <= float(get_news_time) <= float(end_time):
                        print('爬取正文数据中.....')
                        print(item)
                        self.write_news_jsonfile(item)
                        if int(comments_count) > 0:
                            comment_id = news['object']['id']
                            comment_url = 'https://www.zhihu.com/api/v4/articles/{}/root_comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open'.format(str(comment_id))
                            comment_source_url = 'https://zhuanlan.zhihu.com/p/{}'.format(str(comment_id))
                            self.floor_num = 1
                            self.get_comment_info(comment_url, question_title, comment_source_url, keyword)
                    else:
                        print('数据时间不符合')

            is_end = data['paging']['is_end']
            if not is_end:
                next_url = data['paging']['next']
                self.get_questions_list_page(next_url, params, keyword)

    # 获取回答信息
    def get_answers_page(self, url, question_title, source_url, keyword):
        """
        获取问答类的回答列表，其中包含一条条的回答，这些回答可能还有评论，
        :param url:
        :param question_title: 问答的标题
        :param question_id: 问答的id
        :return:
        """
        item = {}
        self.is_stop = False
        # accept-encoding': 'gzip, deflate, br' 在开发中携带了这个头信息，出现乱码情况，去掉这个头信息，问题解决
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'cookie': 'tgw_l7_route=e0a07617c1a38385364125951b19eef8; _xsrf=PhxZhhuALHVLP9dntJMOL27yQZx34zUG',
            'upgrade-insecure-requests': '1',
            'user-agent': '{}'.format(random.choice(self.user_agent))
        }
        # url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset={}&sort_by=created'.format(question_id, offset)
        # print(url)
        response = requests.get(url, headers=headers, proxies={'http':self.ip})  # , proxies={'http':'49.79.67.253:7671'}
        data = json.loads(response.content)
        data_list = data['data']
        for news in data_list:
            # item['type'] = '回答'
            item['platform'] = '知乎'
            crt_time = news['created_time']
            # #转换成localtime
            time_local = time.localtime(float(crt_time))
            # 转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # "%Y-%m-%d %H:%M:%S"
            date = dt.split(' ')[0]
            news_time = dt.split(' ')[1]
            item['date'] = date
            item['time'] = news_time
            author = news['author']['name']
            item['author'] = author
            item['title'] = question_title
            # content = news['content'].replace('<p>', '').replace('</p>', '').replace('<br>', '')
            content = news['content']
            content = etree.HTML(content)
            content = content.xpath('.//p//text()')
            content = ''.join(content)
            item['content'] = content
            item['url'] = source_url
            item['is_topics'] = '是'
            item['floor'] = 0
            item['keyword'] = keyword
            comments_count = news['comment_count']
            item['comments_count'] = comments_count
            item['views'] = ''
            likes = news['voteup_count']
            item['likes'] = str(likes)

            # 做时间判断部分---------------
            get_news_time = time.mktime(time.strptime(date, "%Y-%m-%d"))
            end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
            if self.start_time != '':
                start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
            else:
                start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
            if float(get_news_time) < float(start_time):
                self.is_stop = True  # 返回的回答消息是按时间进行排序的，所以当时间小于指定时间时，就停止爬取，
                break

            if float(start_time) <= float(get_news_time) <= float(end_time):
                print('爬取正文数据中.....')
                print(item)
                self.write_news_jsonfile(item)
                comment_id = news['id']
                if int(comments_count) > 0:  # 获取评论信息
                    comment_url = 'https://www.zhihu.com/api/v4/answers/{}/root_comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open'.format(str(comment_id))
                    self.floor_num = 1
                    logger.info('写入评论中')
                    self.get_comment_info(comment_url, question_title, source_url, keyword)
            else:
                print('数据时间不符合')
                logger.info('数据时间不符合')
        if not self.is_stop:  # 当此次爬取标记为stop时，就不再执行翻页操作
            is_end = data['paging']['is_end']
            if not is_end:  # 判断是否有下一页数据
                next_page_url = data['paging']['next']
                self.get_answers_page(next_page_url, question_title, source_url, keyword)

    def get_comment_info(self, url, question_title, source_url, keyword):
        """
        获取评论信息
        :url:
        :return:
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'upgrade-insecure-requests': '1',
            'user-agent': '{}'.format(random.choice(self.user_agent))
        }
        comment_item = {}
        print(url)
        print('爬取评论数据中......')
        response = requests.get(url, headers=headers, proxies={'http':self.ip})  # , proxies={'http':'49.79.67.253:7671'}
        status_code = response.status_code
        if str(status_code) == '200':
            data = json.loads(response.content)
            comment_data = data['data']
            for comments in comment_data:
                # comment_item['type'] = '评论'
                comment_item['platform'] = '知乎'
                crt_time = comments['created_time']
                # #转换成localtime
                time_local = time.localtime(float(crt_time))
                # 转换成新的时间格式(2016-05-05 20:28:54)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # "%Y-%m-%d %H:%M:%S"
                date = dt.split(' ')[0]
                news_time = dt.split(' ')[1]
                comment_item['date'] = date
                comment_item['time'] = news_time
                author = comments['author']['member']['name']
                comment_item['author'] = author
                comment_item['title'] = question_title
                # content = news['content'].replace('<p>', '').replace('</p>', '').replace('<br>', '')
                content = comments['content']
                content = etree.HTML(content)
                content = content.xpath('.//p//text()')
                content = ''.join(content)
                comment_item['content'] = content
                comment_item['url'] = source_url
                comment_item['is_topics'] = '否'
                comment_item['floor'] = self.floor_num
                self.floor_num += 1
                comment_item['keyword'] = keyword
                comment_item['comments_count'] = 0
                comment_item['views'] = ''
                likes = comments['vote_count']
                comment_item['likes'] = str(likes)
                print(comment_item)
                self.write_news_jsonfile(comment_item)
            is_end = data['paging']['is_end']
            if not is_end:
                next_url = data['paging']['next']
                self.get_comment_info(next_url, question_title, source_url, keyword)

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../zhihu/47_{}_zhihu.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../zhihu/47_{}_zhihu_commnet.json'.format(str(now_time)), 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        # url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=%E5%AE%9D%E9%A9%AC&correction=1&offset=0&limit=10&show_all_topics=0&time_zone=a_week&search_hash_id=6fb2d6db3bf9caa85522feba29017858&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0'
        excelfile = xlrd.open_workbook(r'./../zhihu/keywordV1.4.xlsx')
        sheet1 = excelfile.sheet_by_name('Sheet1')
        cols = sheet1.col_values(0)
        cols = cols[1:]
        print(cols)
        for keyword in cols:
            logger.info('爬取关键字:{}'.format(keyword))
            url = 'https://www.zhihu.com/api/v4/search_v3'
            params = {
                't': 'general',
                'q': keyword,
                'correction': '1',
                'offset': '0',
                'limit': '10',
                'show_all_topics': '0',
                'time_zone': 'a_week',
                'search_hash_id': '6fb2d6db3bf9caa85522feba29017858',
                'vertical_info': '0,0,0,0,0,0,0,0,0,0'
            }
            try:
                self.get_questions_list_page(url, params, keyword)
            except Exception as e:
                logger.error('错误:{}'.format(str(e)))
                print(e)
        logger.info('爬取完毕......')

if __name__ == "__main__":
    spider = ZhiHuSpider()
    spider.run()


