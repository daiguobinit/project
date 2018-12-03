import requests
from lxml import etree
import json
import re
import math
import time
import ast


class SouHuSpider(object):
    """
    搜狐新闻的采集爬虫，采集汽车相关的新闻，一共1000+的车系内容，并根据时间做判断采集
    """
    def __init__(self):

        self.headers_one = {

        }

        self.start_url = 'http://db.auto.sohu.com/home/'
        # 评论接口模板
        self.commnet_port_url = 'http://apiv2.sohu.com/api/topic/load?callback=jQuery112408588342831604119_1543212932163&page_size=10&topic_source_id=mp_{}&page_no={}&hot_size=5&media_id={}&topic_category_id=18&topic_title=%E5%A4%96%E8%A7%82%E6%94%BB%E5%87%BB%E6%80%A7%E6%9B%B4%E5%BC%BA%E5%AE%9D%E9%A9%AC7%E7%B3%BBM%E8%BF%90%E5%8A%A8%E5%A5%97%E4%BB%B6%E7%89%88%E8%B0%8D%E7%85%A7&topic_url=http%3A%2F%2Fwww.sohu.com%2Fa%2F242124808_430526%3Freferid%3D001cxzs00020004&source_id=mp_{}&_=1543212932164'
        # 打开json文件
        self.news_jsonfile = open('./souhu_newsfile.json', 'wb')
        self.comment_jsonfile = open('./souhu_commentfile.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-25'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-25'
        # 标记爬虫工作
        self.is_work = True
        # 评论页数
        self.comment_page_num = 1
        # 去重列表
        self.set_list = []

    # 获取所有的车系连接
    def get_all_carts_category(self, url):
        response = requests.get(url)
        data = etree.HTML(response.content.decode())
        url_list = data.xpath('.//ul[@class="tree_con"]/li/a[@class="model-a"]/@href')
        # print(url_list)
        for carts_url in url_list:
            for i in range(1, 7):
                self.get_carts_page_info(carts_url, page_id=str(i))

    # 获取车系详情页
    def get_carts_page_info(self, url, page_id='1'):
        text = '/news_{}/page_1.html'
        url = 'http:' + url + text.format(page_id)
        # http://db.auto.sohu.com/yiqiaudi/4414/news_1/page_1.html
        print(url)
        response = requests.get(url)
        data = etree.HTML(response.content.decode())
        news_list = data.xpath('.//ul[@id="txt_list"]/li')
        if news_list:
            for news in news_list:
                try:
                    news_time_info = news.xpath('.//em/text()')[0]
                    news_time = re.search('\d{4}-\d{1,2}-\d{1,2}', news_time_info).group(0)
                    source = news_time_info.strip()
                    source = re.sub(' ', '', source)
                    source = re.sub(r'\r\n', '', source)
                    source = source.split('(')[0].split('：')[1]
                    news_url = news.xpath('.//a/@href')[0]
                    print(news_time, '-------------------')
                    # 做时间判断部分---------------
                    get_news_time = time.mktime(time.strptime(news_time, "%Y-%m-%d"))
                    end_time = time.mktime(time.strptime(self.end_time, "%Y-%m-%d"))
                    if self.start_time != '':
                        start_time = time.mktime(time.strptime(self.start_time, "%Y-%m-%d"))
                    else:
                        start_time = time.mktime(time.strptime('2010-1-1', "%Y-%m-%d"))
                    if float(get_news_time) < float(start_time):
                        self.is_work = False
                        break
                    if float(start_time) <= float(get_news_time) <= float(end_time):
                        # 根据url进行简单的去重
                        if news_url not in self.set_list:
                            self.get_news_page_info(news_url, source)
                            self.set_list.append(news_url)
                except IndexError:
                    print('空白节点')
                except Exception as e:
                    print(e, '其他错误')
        else:
            print('板块没有新闻--------------------------------')

    # 获取新闻详情页信息
    def get_news_page_info(self, url, source):
        item = {}
        url = 'http:' + url
        response = requests.get(url)
        data = etree.HTML(response.content.decode())
        item['platform'] = '搜狐新闻'
        title = data.xpath('.//h3[@class="article-title"]/text()')[0].strip()
        item['title'] = title
        date_all = data.xpath('.//span[@class="l time"]/text()')[0]
        date = date_all.split(' ')[0]
        news_time = date_all.split(' ')[1]
        item['date'] = date
        item['time'] = news_time
        item['source_author'] = source
        content = data.xpath('.//article[@class="article-text"]/p/text()')
        content = ''.join(content)
        content = re.sub(' ', '', content)
        content = re.sub('\n', '', content)
        item['content'] = content
        views = data.xpath('.//div[@class="l read-num"]/text()')[0]
        views = views.split('(')[1].split(')')[0]
        item['clicks'] = views
        item['url'] = url
        source_id = url.split('/')[-1].split('_')[0]
        media_id = url.split('/')[-1].split('_')[1]
        comment_count = self.get_comment_info(source_id, media_id, title, date, news_time, url)
        item['comments_count'] = comment_count
        item['keyword'] = ''
        item['likes'] = ''
        print(item)
        print('正在写入新闻信息')
        self.write_news_jsonfile(item)

    # 获取评论信息
    def get_comment_info(self, source_id, media_id, title, source_date, source_time, source_url, page_id='1'):
        item = {}
        # 构建url
        url = self.commnet_port_url.format(source_id, page_id, media_id, source_id)
        print(url)
        response = requests.get(url)
        data = response.content.decode()
        data = data[42:][:-2]
        data = json.loads(data)
        comment_count = data['jsonObject']['cmt_sum']
        comments_list = data['jsonObject']['comments']
        total_page_no = data['jsonObject']['total_page_no']
        if comments_list:
            for comment in comments_list:
                item['platform'] = '搜狐新闻'
                item['source_date'] = source_date
                item['source_time'] = source_time
                item['title'] = title
                item['source_url'] = source_url
                comment_all_time = comment['create_time']
                comment_all_time = str(comment_all_time)[:10] + '.' + str(comment_all_time)[-3:]
                comment_all_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(comment_all_time)))
                date = comment_all_time.split(' ')[0]
                comment_time = comment_all_time.split(' ')[1]
                item['date'] = date
                item['time'] = comment_time
                content = comment['content']
                item['content'] = content
                author = comment['passport']['nickname']
                item['author'] = author
                item['comment_url'] = source_url
                item['floor'] = ''
                item['keyword'] = ''
                item['views'] = ''
                item['comments_count'] = ''
                item['likes'] = ''
                print('正在写入评论信息')
                # 写入json文件
                self.write_comment_jsonfile(item)
            if int(total_page_no) > 1 and self.comment_page_num+1 <= int(total_page_no):
                self.comment_page_num += 1
                print('爬取翻页评论信息')
                self.get_comment_info(source_id, media_id, title, source_date, source_time, source_url, page_id=str(self.comment_page_num))
        self.comment_page_num = 1
        return comment_count

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.comment_jsonfile.write(item.encode("utf-8"))

    def close_file(self):
        self.news_jsonfile.close()
        self.comment_jsonfile.close()

    def run(self):
        self.get_all_carts_category(self.start_url)
        # 关闭文件
        self.close_file()


if __name__ == "__main__":
    souhu = SouHuSpider()
    souhu.run()
