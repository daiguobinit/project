import requests
from lxml import etree
import json
import re
import math
import time
import ast
import xlrd


class AiKaSpider(object):
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
        # 打开excel文件
        excel_file = xlrd.open_workbook(r'./url20181031.xlsx')
        aika = excel_file.sheet_by_name('爱卡')
        cols = aika.col_values(1)
        self.cols = cols[1:]

    # 获取页面
    def get_page(self, url):
        response = requests.get(url)
        data = etree.HTML(response.content.decode('gb2312'))
        # 车系
        cars = data.xpath('.//div[@class="demio_main main_mt0"]/div/span[2]/text()')[0] + data.xpath('.//div[@class="demio_main main_mt0"]/div/h1/text()')[0]
        # 车款
        models = data.xpath('.//tr[@id="base_title"]/td[@scope="col"]/a/text()')
        id_list = data.xpath('.//tr[@id="base_title"]/td[@scope="col"]/@id')
        print(id_list)
        num = len(models)  # 这个num表示有多少个车款类型
        # url
        print(num, '个车型')
        id = url.split('/')[-2]
        price_url = 'http://newcar.xcar.com.cn/auto/index.php?r=ajax/GetDealerPrice2&flag=1&did_type=1&is_num=1&sort_price=1&city_id=507&pserid={}&rand=0.892742433471938'.format(id)
        if num > 0:

            dict_list = dict()
            for i in id_list:
                key = i.split('_')[1]
                print(key)
                dict_list[key] = {}
            for table_num in range(1, 17):
                table = data.xpath('.//table[@id="base_{}"]/tr'.format(str(table_num)))  # 获取一个表的节点
                for tr in table:  # 从表中获取子节点， 可以看做是一行行的获取数据
                    name = tr.xpath('.//td[1]//text()')
                    name = ''.join(name).strip().replace('：', '')
                    if name == '本地最低报价':
                        name = '最低报价'
                    for i in id_list:
                        item_dict = dict_list[i.split('_')[1]]
                        text = tr.xpath('.//td[@ci="{}"]//text()'.format(str(id_list.index(i)+1)))  # 从一行的的数据再获取子数据，进行分类
                        text = ''.join(text).strip()
                        item_dict[name] = text
                        item_dict['URL'] = url
                        item_dict['车系'] = cars
                        item_dict['车款'] = models[id_list.index(i)]
            # 获取价格的json数据
            print(price_url)
            price_response = requests.get(price_url)
            price_data = json.loads(price_response.content.decode())
            print(price_data)
            try:
                price_list = price_data['model_list']
                for price in price_list:
                    try:
                        prc_id = price['mid']
                        dict_list[prc_id]['最低报价'] = price['min_price']
                    except:
                        pass
            except Exception as e:
                print(e)
                print('无最低报价')

            for key in dict_list:
                value = dict_list[key]
                print('写入数据中......')
                self.write_news_jsonfile(value)

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./AiKa_newsfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./AiKa_commentfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    # def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()

    def run(self):
        for url in self.cols:
            url = url + 'config.htm'
            print("正在爬取   ", url)
            try:
                self.get_page(url)
            except IndexError:
                print('网页未找到......')
            except Exception as e:
                print(e, '其他错误')
            time.sleep(1)


if __name__ == "__main__":
    spider = AiKaSpider()
    spider.run()
