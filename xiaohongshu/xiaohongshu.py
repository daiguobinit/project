import requests
from lxml import etree
import json
import re
import math
import time
import ast
import xlrd
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class XiaoHongShuSpider(object):
    """
    小红书网站的爬虫
    这是一个爬虫模板
    """
    def __init__(self):

        self.headers_one = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.baidu.com',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.headers_two = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        self.headers_three = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.xiaohongshu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        self.start_url = ''
        # 评论接口模板
        self.commnet_port_url = ''
        # # 打开json文件
        # self.news_jsonfile = open('./sina_newsfile.json', 'wb')
        # self.comment_jsonfile = open('./sina_commentfile.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-13'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-20'
        # 标记爬虫工作
        self.is_work = True
        # ip代理
        self.proxies_list = [
            '49.67.149.238:8736',
            '49.84.38.45:4203',
            '117.44.27.173:4201',
            '106.110.203.250:4276'
        ]

    def get_news_url(self, carts):
        """
        从百度搜索关键词，然后获取符合的新闻的url
        :param carts:
        :return:
        """
        url = 'https://www.baidu.com/s?q1={}&q2=&q3=&q4=&gpc=stf%3D1543216862.078%2C1543821662.078%7Cstftype%3D1&ft=&q5=&q6=xiaohongshu.com&tn=baiduadv'.format(str(carts))
        print(url)

        ip = random.choice(self.proxies_list)
        response = requests.get(url, headers=self.headers_one, proxies={'https': ip}, verify=False)
        content = etree.HTML(response.content.decode())
        if content.xpath('.//h3[@class="t"]/a/@href'):
            url_list = content.xpath('.//h3[@class="t"]/a/@href')
            print(url_list)
            for url in url_list:
                news_url = url.replace('http', 'https')
                try:
                    self.get_news_page(news_url)
                except KeyError:
                    print('ip可能被封')
                time.sleep(10)
        elif content.xpath('.//div[@class="content_none"]/div/p//text()'):
            txt = content.xpath('.//div[@class="content_none"]/div/p//text()')
            print(txt)
        else:
            print('其他错误', url)
        print('------------------------------------------------')

    def get_news_page(self, url):
        """
        获取新闻详情页
        :param url:
        :return:
        """

        print(url, '*******************')
        ip = random.choice(self.proxies_list)
        # 通过重定向网址获取目标网址
        response = requests.get(url, headers=self.headers_two, proxies={'https': ip}, allow_redirects=False)
        print(response.status_code)
        news_url = response.headers['Location']
        print(news_url)
        id = news_url.split('?')[0].split('/')[-1]
        print(id)

        # 获取cookies
        response_cookie = requests.get(news_url, allow_redirects=False, proxies={'https': ip})
        print(response_cookie.url)
        cookies = response_cookie.headers['Set-Cookie']
        xhs = cookies.split(';')[0]
        ant = cookies.split(';')[6].split(',')[1]
        cook = xhs + ';extra_exp_ids=;' + ant + ';xhsuid=VtBxhJLvZQVsqyxR'
        print(cook)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.xiaohongshu.com',
            'Cookie': cook,
            'Referer': 'https://www.xiaohongshu.com/discovery/item/' + str(id),
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }

        # 从服务器获取参数
        text = self.get_at()
        params_id = text.split('|')[0]
        news_url = news_url.split('?')[0] + '?_at={}'.format(params_id)
        print(news_url, '==========')
        # 通过目标网址获取新闻页
        news_response = requests.get(news_url, headers=headers, proxies={'https': ip})
        # print(news_response.content.decode())
        data = etree.HTML(news_response.content.decode())
        if data.xpath('.//div/div[@class="content"]/p/text()'):
            content = data.xpath('.//div/div[@class="content"]/p/text()')
        else:
            content = data.xpath('.//div/div[@class="content"]//text()')
        content = ''.join(content)
        print(content)
        item = {}
        item['url'] = news_url
        item['content'] = content
        self.write_news_jsonfile(item)

    def get_at(self):
        url = 'https://anti-bot.baidu.com/abdr'
        data = 'eyIxIjoiMSIsIjMiOiI1ZTg1MThiY2RhOTlmNzczZWRmMDZmZTJmY2ZlYzVkNDc0ZmU3Njg1IiwiNCI6IjI0IiwiNSI6IjE2MDB4OTAwIiwiNiI6IjE2MDB4ODYwIiwiNyI6IiwiLCI4IjoiQ2hyb21lJTIwUERGJTIwUGx1Z2luLENocm9tZSUyMFBERiUyMFZpZXdlcixOYXRpdmUlMjBDbGllbnQiLCI5IjoiLFBvcnRhYmxlJTIwRG9jdW1lbnQlMjBGb3JtYXQsTmF0aXZlJTIwQ2xpZW50JTIwRXhlY3V0YWJsZSxQb3J0YWJsZSUyME5hdGl2ZSUyMENsaWVudCUyMEV4ZWN1dGFibGUiLCIxMSI6IjEiLCIxMiI6IjEiLCIxMyI6InRydWUiLCIxNCI6Ii00ODAiLCIxNSI6InpoLUNOIiwiMTYiOiIiLCIxNyI6IjEsMSwxLDEsMSwwIiwiMTgiOiIxIiwiMTkiOiIyIiwiMjAiOiIwIiwiMjEiOiIiLCIyMiI6IkdlY2tvLDIwMDMwMTA3LEdvb2dsZSBJbmMuLCxNb3ppbGxhLE5ldHNjYXBlLFdpbjMyLDMzLCIsIjIzIjoiMCwwLDAiLCIyNCI6IjEiLCIyNyI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzcwLjAuMzUzOC4xMTAgU2FmYXJpLzUzNy4zNiIsIjI4IjoiZmFsc2UsZmFsc2UiLCIyOSI6InRydWUsdHJ1ZSx0cnVlIiwiMzIiOiIzNCIsIjM0IjoiV2luMzIiLCIzNSI6ImZhbHNlLHRydWUiLCIxMDEiOiJhNTQ2Nzg4NGI4ZTg5YjlmMTE2MTJhNDExZThhYjdmNDgyYmNkY2JiIiwiMTAzIjoiMTU0Mzg5MTU0MzgyMCIsIjEwNCI6IiIsIjEwNiI6IjIwMDUiLCIxMDciOiIxMiIsIjEwOCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjMzNDIvY2hhbmNlL3R4Lmh0bWw/X2lqdD1oOWU5bDdpNDlsM2pjZjA2bDY2Y2ZjZWplMCIsIjEwOSI6IiIsIjExMCI6IjkxZTkzMDhjNGE2MmNkYTM2Y2EzNDdiN2RhNmQ4ZDFiYmY1YTEiLCIxMTIiOiIiLCIxMTMiOiIiLCIxMTQiOiIiLCIxMTUiOiIiLCIyMDAiOiIxIn0='
        response = requests.post(url, data=data)
        text = response.text
        return text

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('./sina_newsfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        with open('./sina_commentfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        excelfile = xlrd.open_workbook(r'./keyword_20181126.xlsx')
        print(excelfile.sheet_names())
        sheet1 = excelfile.sheet_by_name('Sheet1')
        cols = sheet1.col_values(0)
        cols = cols[1:]
        for cart in cols:
            # time.sleep(2)
            self.get_news_url(cart)


if __name__ == "__main__":
    xiaohongshu = XiaoHongShuSpider()
    xiaohongshu.run()
