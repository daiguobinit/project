# -*- coding: utf-8 -*-
import scrapy


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    # allowed_domains = ['http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812']
    start_urls = ['URL: http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812']

    def parse(self, response):
        pass
