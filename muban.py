import requests
from lxml import etree
import json
import re
import math
import time
import ast


class SinaSpider(object):
    """
    这是一个爬虫模板
    """
    def __init__(self):

        self.headers_one = {

        }

        self.start_url = ''
        # 评论接口模板
        self.commnet_port_url = ''
        # 打开json文件
        self.news_jsonfile = open('./sina_newsfile.json', 'wb')
        self.comment_jsonfile = open('./sina_commentfile.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-13'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-20'
        # 标记爬虫工作
        self.is_work = True

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
        pass


if __name__ == "__main__":
    sina = SinaSpider()
    sina.run()
