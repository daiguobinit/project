import requests
from lxml import etree
import json
import re
import math
import time


class JieMianSpider():
    def __init__(self):
        # 爬取新闻列表的headers
        self.headers_one = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Cookie':'pgv_pvi=8618249216; pgv_si=s6958286848; SERVERID=10.70.50.21',
            'Host':'a.jiemian.com',
            'Referer':'https://www.jiemian.com/lists/51.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        # 爬取评论的headers
        self.headers_two = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'pgv_pvi=8618249216; pgv_si=s6958286848; SERVERID=10.70.50.21',
            'Host': 'a.jiemian.com',
            'Referer': 'https://www.jiemian.com/article/2598846.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        # 获取新闻页的headers
        self.headers_three = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'__jsluid=e2383ce96a600d8b7af7367fb52adaaf; pgv_pvi=8618249216; pgv_si=s6958286848; _tb_sess_r=https%3A//www.jiemian.com/lists/51.html; _tb_t_ppg=https%3A//www.jiemian.com/article/2596911.html; trc_cookie_storage=taboola%2520global%253Auser-id%3D89521ea2-baa4-4a77-b1bd-dafd704907a8-tuct2dc33bb',
            'Host':'www.jiemian.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'''
        }

        self.start_url = 'https://a.jiemian.com/index.php?m=lists&a=cLists&notid=2600447,2603510,2600141&id=194&type=card&callback=jQuery110209049534785792808_1541642080659&page={}&_=1541642080661'
        self.news_page_num = 1
        # 用作爬虫时间判断的计数
        self.time_out_num = 0
        # 用作判断爬虫是否停止的参数
        self.stop_spider = False
        # 评论url模板
        self.comment_port_url = 'https://a.jiemian.com/index.php?m=comment&a=getlistCommentP&aid={}&page={}&comment_type=1&per_page=5&callback=jQuery110208603319204711195_1541662025237&_=1541662025244'
        # 打开新闻json文件
        self.news_jsonfile = open('./jiemian_news.json', 'wb')
        # 打开评论json文件
        self.comment_jsonfile = open('./jiemian_comment.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-9-1'
        # 定义结束时间 y-m-d
        self.end_time = '2018-10-1'
        # 错误计数
        self.error_num = 0
        # 错误url
        self.error_url_list = []
        # 总计新闻页
        self.all_news_num = 0

    # 获取新闻列表的url
    def get_news_url(self, url):
        print(url, '%%%%%%%%%')
        news_url_json_data = requests.get(url, headers=self.headers_one)
        content = news_url_json_data.text
        content = content.split('(')[1].split(')')[0]
        content = json.loads(content)
        content_str = content['rst']
        url_list = re.findall(r'https://www.jiemian.com.*?.html', content_str)
        try:
            data = re.search(r'">\d{2}/\d{2}', content_str).group(0).split('>')[1]
        except AttributeError as e:
            print(e)
            data = time.strftime("%m/%d")

        print(data)
        print(url_list)
        url_list_new = []
        for url in url_list:
            url_split = url.split('/')
            if 'article' in url_split:
                url_list_new.append(url)
        url_list_new = set(url_list_new)
        url_list_new = list(url_list_new)
        print(url_list_new)
        return url_list_new, data

    # 获取新闻页
    def get_news_page(self, url):
        print(url)
        # self.headers_two['Referer'] = str(url)
        response = requests.get(url, headers=self.headers_three)
        code = response.status_code
        news_page_content = etree.HTML(response.content.decode())
        title = news_page_content.xpath('.//div[@class="article-header"]/h1/text()')[0]
        # 获取新闻发表的时间，用作时间判断
        try:
            data = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[0]
        except:
            data = news_page_content.xpath('.//div[2]/p/span[2]/text()')[0].split(' ')[0]
        data = re.sub('/', '-', data)
        print(code)
        print(title, data)
        return news_page_content, code, data

    # 处理新闻html页面
    def parse_page(self, news_page_content, news_page_url):
        item = dict()
        # 网站paltform
        item['paltform'] = '汽车_界面新闻'

        # 文章标题title
        title = news_page_content.xpath('.//div[@class="article-header"]/h1/text()')[0]
        item['title'] = title
        # 文章正文content
        content = news_page_content.xpath('.//div[5]/div[@class="article-content"]/p/text()')
        item['content'] = ''.join(content)
        # 获取第一节点数据
        first_node = news_page_content.xpath('.//div[4]/p/span[1]/text()')[0]
        # first_node = first_node.split(' ')
        # 获取第三节点数据
        third_node = news_page_content.xpath('.//div[4]/p/span[3]/text()')[0]

        # 判断是否能获取第四节点数据
        if news_page_content.xpath('.//div[4]/p/span[4]/text()'):
            print(1111111111111111111111111)
            # 发布日期data
            data_tiem = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[0]
            times = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[1]
            data = re.sub('/', '-', data_tiem)
            item['data'] = data
            # 发布时间time
            item['time'] = times
            # 来源/作者source_author
            author = news_page_content.xpath('.//div[4]/p/span[1]/a/text()')[0]
            source = news_page_content.xpath('.//div[4]/p/span[4]/text()')[0]
            # 阅读量
            views = news_page_content.xpath('.//div[2]/div[4]/p/span[3]/text()')[0]
        elif re.search('/', first_node):
            print(2222222222222222222222222)
            # 发布日期data
            data_tiem = news_page_content.xpath('.//div[4]/p/span[1]/text()')[0].split(' ')[0]
            times = news_page_content.xpath('.//div[4]/p/span[1]/text()')[0].split(' ')[1]
            data = re.sub('/', '-', data_tiem)
            item['data'] = data
            # 发布时间time
            item['time'] = times
            # 来源/作者source_author
            author = ''
            source = news_page_content.xpath('.//div[4]/p/span[3]/text()')[0]
            # 阅读量
            views = news_page_content.xpath('.//div[2]/div[4]/p/span[2]/text()')[0]

        elif '浏览' in third_node and news_page_content.xpath('.//div[@class="article-author"]/div'):
            print(33333333333333333333333333333333333)
            # 发布日期data
            data_tiem = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[0]
            times = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[1]
            data = re.sub('/', '-', data_tiem)
            item['data'] = data
            # 发布时间time
            item['time'] = times
            # 来源/作者source_author
            author = news_page_content.xpath('.//div[4]/p/span[1]/a/text()')[0]
            source = ''
            # 阅读量
            views = news_page_content.xpath('.//div[4]/p/span[3]/text()')[0]
        elif '浏览' in third_node and not news_page_content.xpath('.//div[@class="article-author"]/div'):
            print(44444444444444444444444444444)
            # 发布日期data
            data_tiem = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[0]
            times = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[1]
            data = re.sub('/', '-', data_tiem)
            item['data'] = data
            # 发布时间time
            item['time'] = times
            # 来源/作者source_author
            author = ''
            source = news_page_content.xpath('.//div[4]/p/span[1]/a/text()')[0]
            # 阅读量
            views = news_page_content.xpath('.//div[4]/p/span[3]/text()')[0]
        else:
            print(5555555555555555555555555555555555)
            # 发布日期data
            data_tiem = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[0]
            times = news_page_content.xpath('.//div[4]/p/span[2]/text()')[0].split(' ')[1]
            data = re.sub('/', '-', data_tiem)
            item['data'] = data
            # 发布时间time
            item['time'] = times
            # 来源/作者source_author
            author = news_page_content.xpath('.//div[4]/p/span[1]/a/text()')[0]
            source = news_page_content.xpath('.//div[4]/p/span[3]/text()')[0]
            # 阅读量
            views = ''

        item['source_author'] = source + '/' + author
        # 点击数clicks
        item['clicks'] = ''
        # 阅读量 views
        item['views'] = views
        # 评论数comments_count
        comments_count = news_page_content.xpath('.//p[@class="title-box"]/span/text()')[0]
        item['comments_count'] = comments_count
        # 点赞数likes
        item['likes'] = news_page_content.xpath('.//span[@class="ding_count"]/text()')[0]
        # 关键词keyword
        item['keyword'] = ''
        # url
        item['url'] = news_page_url
        self.write_news_into_jsonfile(item)
        # 爬取文章评论回复内容
        if int(comments_count) != 0:
            self.parse_comment_info(news_page_url, int(comments_count), data,times, title, news_page_url)

        else:
            pass

        return item

    # 处理从评论接口处获取的评论信息
    def parse_comment_page(self, comment_port_url, source_date, source_time, source_title, source_url, floor_num):
        print(comment_port_url)
        response = requests.get(comment_port_url, headers=self.headers_two)
        data = response.content.decode()
        data = re.sub(r'\\"', '\"', data)
        print('*******',data)
        data = re.findall(r'<dd class=.*?/dd>', data)
        print(data)
        comment_item = dict()

        if data:
            print('---------------------')
            for data in data:
                data = etree.HTML(data)
                data_list = data.xpath('.//dd[@class="comment-post"]')
                for data in data_list:
                    # 网站
                    comment_item['platform'] = '界面新闻'
                    # 文章原文发表日期
                    comment_item['source_date'] = source_date
                    # 原文发表时间
                    comment_item['source_time'] = source_time
                    # 文章标题
                    comment_item['title'] = source_title
                    # 原文url
                    comment_item['source_url'] = source_url
                    # 文章回复人名称
                    author = data.xpath('.//div[@class="comment-body"]/a/text()')[0].encode('utf-8').decode('unicode_escape')
                    comment_item['author'] = author
                    # 文章回复内容
                    text = data.xpath('.//div[1]/p/text()')[0].encode('utf-8').decode('unicode_escape')
                    comment_item['text'] = text
                    try:
                        data_all = data.xpath('.//div[@class="comment-footer"]/span[1]/text()')[0]
                        print(data_all)
                        # 回复日期
                        day_date = data_all.split(' ')[0]
                        day_date = re.sub(r'\\/', '-', day_date)
                        comment_item['date'] = day_date
                        # 回复时间
                        comment_time = data_all.split(' ')[1]
                        comment_item['time'] = comment_time
                    except:
                        comment_item['date'] = ''
                        comment_item['time'] = ''
                    # 点赞数
                    likes = data.xpath('.//em/text()')[0]
                    likes = re.search('\d', likes).group(0)
                    comment_item['likes'] = likes
                    # 回复数
                    comments_count = '0'
                    comment_item['comments_count'] = comments_count
                    # 评论url
                    comment_url = comment_port_url
                    comment_item['comment_url'] = comment_url
                    # 阅读量
                    views = ''
                    comment_item['views'] = views
                    # 关键字
                    keyword = ''
                    comment_item['keyword'] = keyword
                    # 楼层
                    floor = floor_num
                    comment_item['floor'] = floor
                    floor_num += 1
                    self.write_comment_into_jsonfile(comment_item)

            return floor_num

    # 爬取评论信息
    def parse_comment_info(self, url, comments_count, data, times, title, source_url):
        all_page_num = math.ceil(comments_count/5)
        url_num = url.split('/')[-1].split('.')[0]
        floor_num = 1
        for port_page_num in range(1, all_page_num + 1):

            comment_port_url = self.comment_port_url.format(str(url_num), str(port_page_num))
            floor_num = self.parse_comment_page(comment_port_url, data, times, title, source_url, floor_num)

    # 将新闻信息写入json文件
    def write_news_into_jsonfile(self, news_item):
        news_item = json.dumps(dict(news_item), ensure_ascii=False) + ',\n'
        # try:
        self.news_jsonfile.write(news_item.encode('utf-8'))
        # except:
        #     pass

    # 将文章评论信息写入json文件
    def write_comment_into_jsonfile(self, comment_item):
        comment_item = json.dumps(dict(comment_item), ensure_ascii=False) + ',\n'
        try:
            self.comment_jsonfile.write(comment_item.encode('utf-8'))
        except:
            pass

    # 关闭新闻json文件
    def close_news_jsonfile(self):
        self.news_jsonfile.close()

    # 关闭评论json文件
    def close_comment_jsonfile(self):
        self.comment_jsonfile.close()

    def run(self):
        while self.news_page_num < 100:
            url_list_new, data = self.get_news_url(self.start_url.format(str(self.news_page_num)))
            # 时间判断
            data = '2018-' + re.sub('/', '-', data)
            get_time = time.mktime(time.strptime(data, "%Y-%m-%d"))
            start_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
            if self.start_time != '':
                end_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
            else:
                end_time = time.mktime(time.strptime('2100-1-1', "%Y-%m-%d"))
            if float(get_time) < float(end_time):
                # self.crawler.engine.close_spider(self, '爬虫终止')
                print(data)
                # break_flag = True
                break
            if float(end_time) <= float(get_time) <= float(start_time):
                print(data)

                for news_page_url in url_list_new:
                    self.all_news_num += 1
                    news_page_content, code, data = self.get_news_page(news_page_url)
                    try:
                        item = self.parse_page(news_page_content, news_page_url)
                        print(item)
                    except:
                        self.error_num += 1
                        self.error_url_list.append(news_page_url)
            self.news_page_num += 1
        print(self.error_num)
        print(self.error_url_list)
        print(self.all_news_num)

if __name__ == "__main__":
    jiemian_spider = JieMianSpider()
    jiemian_spider.run()