# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 网站
    platform = scrapy.Field()
    # 日期
    data = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 原贴内容
    content = scrapy.Field()
    # url
    url = scrapy.Field()
    # 是否是主帖
    is_topics = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 关键词
    keyword = scrapy.Field()
    # 评论数
    comments_count = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 点赞
    like = scrapy.Field()


