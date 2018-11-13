# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ChancePipeline(object):
    def __init__(self):
        print('打开json文件')
        self.filename = open("./hangye9month.json", 'wb')

    def process_item(self, item, spider):
        print("写入json数据")
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(text.encode('utf-8'))
        return item

    def close_spider(self, spider):
        print('关闭json文件')
        self.filename.close()
