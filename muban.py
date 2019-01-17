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
file_name = r"./hupu-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=file_name,   # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)

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
        # # 打开json文件
        # self.news_jsonfile = open('./sina_newsfile.json', 'wb')
        # self.comment_jsonfile = open('./sina_commentfile.json', 'wb')
        # 定义开始时间 y-m-d
        self.start_time = '2018-11-13'
        # 定义结束时间 y-m-d
        self.end_time = '2018-11-20'
        # 标记爬虫工作
        self.is_work = True

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./sina_newsfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./sina_commentfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        pass


if __name__ == "__main__":
    spider = SinaSpider()
    spider.run()
