# -*- coding: utf-8 -*-
import scrapy
from chance.items import ChanceItem
from scrapy.http import Request
import re
import time
from datetime import datetime
from datetime import timedelta

# 自定义爬取结束时间2018-10-30

date = datetime.now() - timedelta(days=3)
news_start_time = str(date).split(' ')[0]
yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
yesterday = str(yesterday).split(' ')[0]
print('爬取时间段：{}到{}'.format(news_start_time, yesterday))

END_TIME = news_start_time
START_TIME = yesterday
# 自定义爬取最大页数,默认是网站目前的最大页数1645
MAX_PAGE_NUM = 1645

class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    # allowed_domains = ['https://auto.ifeng.com/']"https://auto.ifeng.com/xinche/","https://auto.ifeng.com/daogou/",
    # "https://auto.ifeng.com/shijia/",https://auto.ifeng.com/hangye/
    start_urls = [
        "https://auto.ifeng.com/xinche/",
                  ]
    page_num = 1
    count = 1
    shijia_page_num = 1
    daogou_page_num = 1
    hangye_page_num = 1

    xinche_stop = False
    daogou_stop = False
    shijia_stop = False
    hangye_stop = False

    def parse(self, response):
        item = ChanceItem()
        # cart_news = response.xpath(".//div[@class='v2c-lst-li']/a[@class='tit']/@href").extract()
        cart_news_list = response.xpath(".//div[@class='v2c-lst-li']")
        for cart_new in cart_news_list:
            cart_new_url = cart_new.xpath('.//a[@class="tit"]/@href').extract()[0]
            data_all = cart_new.xpath('.//div/span[2]/em/text()').extract()[0]
            data = data_all.split(" ")[0]
            try:
                data = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data).group(0)
            except:
                data = '2018-08-08'
            print(data)
            # 日期
            # data = re.sub('年', '-', data)
            # data = re.sub('月', '-', data)
            # data = re.sub('日', '', data)
            get_time = time.mktime(time.strptime(data, "%Y-%m-%d"))
            start_time = time.mktime(time.strptime(START_TIME, "%Y-%m-%d"))
            if END_TIME != '':
                end_time = time.mktime(time.strptime(END_TIME, "%Y-%m-%d"))
            else:
                end_time = time.mktime(time.strptime('2100-1-1', "%Y-%m-%d"))
            if END_TIME != '' and float(get_time) < float(end_time):
                # self.crawler.engine.close_spider(self, '爬虫终止')
                print(response.url)
                if 'xinche' in response.url:
                    self.xinche_stop = True
                if 'shijia' in response.url:
                    self.shijia_stop = True
                if 'daogou' in response.url:
                    self.daogou_stop = True
                if 'hangye' in response.url:
                    self.hangye_stop = True
            # else:
            # http://data.auto.ifeng.com/pic/g-14722.html#pid=2283636
            if float(end_time) <= float(get_time) <= float(start_time):
                cart_new_url_list = cart_new_url.split("/")

                title = cart_new.xpath('.//a/text()').extract()[0]
                content = cart_new.xpath('.//div/span[1]/text()').extract()[0]
                data_all = cart_new.xpath('.//em/text()').extract()[0]
                time_new = data_all.split(" ")[1]
                data = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data_all).group(0)
                if cart_new_url_list[3] == "pic":

                    item['title'] = title
                    item['content'] = content
                    item['time'] = time_new
                    item['date'] = data
                    item['url'] = cart_new_url
                    item['platform'] = '凤凰网汽车'
                    item['source_author'] = '凤凰网汽车'
                    item['comments_count'] = ''
                    item['likes'] = ''
                    item['views'] = ''
                    item['keyword'] = ''
                    print(item)
                    yield item
                else:

                    yield scrapy.Request(cart_new_url, callback=self.parse_new_page, meta={'title':title, 'content': content, 'data':data, 'time':time_new, 'url': cart_new_url})

        if not self.xinche_stop:
            if self.page_num <= MAX_PAGE_NUM:

                self.page_num += 1
                print('新车'+str(self.page_num)+"页")
                new_url = self.start_urls[0]+str(self.page_num)+".shtml"
                yield scrapy.Request(new_url, callback=self.parse)

        if not self.shijia_stop:
            if self.shijia_page_num < 128:
                print('试驾' + str(self.shijia_page_num) + '页')
                new_url = "https://auto.ifeng.com/shijia/"+str(self.shijia_page_num)+".shtml"
                self.shijia_page_num += 1
                yield scrapy.Request(new_url, callback=self.parse)

        if not self.daogou_stop:
            if self.daogou_page_num <= 145:
                print('导购' + str(self.daogou_page_num) + '页')
                new_url = 'https://auto.ifeng.com/daogou/'+str(self.daogou_page_num)+".shtml"
                self.daogou_page_num += 1
                yield scrapy.Request(new_url, callback=self.parse)

        if not self.hangye_stop:
            if self.hangye_page_num < 1641:
                print('行业' + str(self.hangye_page_num) + '页')
                new_url = 'https://auto.ifeng.com/hangye/'+str(self.hangye_page_num)+".shtml"
                self.hangye_page_num += 1
                yield scrapy.Request(new_url, callback=self.parse)

    def parse_new_page(self, response):

        print("爬取第%d条数据" % self.count)
        self.count += 1
        item = ChanceItem()
        # try:
        # 网站
        try:
            item['platform'] = response.xpath(".//div/h1/a/text()").extract()[0]
            item['source'] = response.xpath(".//div/h1/a/text()").extract()[0]
        except:
            item['platform'] = '凤凰网汽车'
            item['source'] = '凤凰网汽车'
        # 来源

        # 标题
        item['title'] = response.meta['title']
        # 内容
        # try:
        content = response.xpath('.//div[1]/div[3]/p/text()').extract()
        if content != []:
            pass
        else:
            content = response.xpath('.//div/div[@id="artical_real"]/p/text()').extract()
        item['content'] = ''.join(content)
        # 时间
        item['time'] = response.meta['time']
        item['data'] = response.meta['data']
        # 作者
        # try:
        #     item['author'] = response.xpath('.//*[@id="author_baidu"]/text()').extract()[0].split("：")[1]
        # except Exception as e:
        #     print(e, '1111')
        #     item['author'] = '无'
        # 评论数
        try:
            item['comments_count'] = response.xpath('.//*[@id="comments"]/div[1]/div[1]/div[2]/div[2]/text()').extract()[0]
        except Exception as e:
            print(e, '2222')
            item['comments_count'] = response.xpath('.//*[@id="webUser"]/text()').extract()[0]
        # 点赞数
        try:
            item['like'] = response.xpath('.//*[@id="comments"]/div[1]/div[1]/div[2]/div[1]/text()').extract()[0]
        except:
            item['like'] = '无'
        # 网页url
        item['url'] = response.url
        # 关键词
        item['keyword'] = ""
        yield item
        # except:
        #     item['title'] = response.meta['title']
        #     item['content'] = response.meta['content']
        #     item['time'] = response.meta['time']
        #     item['data'] = response.meta['data']
        #     item['url'] = response.meta['url']
        #     item['platform'] = '凤凰网汽车'
        #     item['source'] = '凤凰网汽车'
        #     item['author'] = ''
        #     item['comments_count'] = ''
        #     item['like'] = ''
        #     item['keyword'] = ''
        #     yield item



