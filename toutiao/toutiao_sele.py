from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import json
import requests
import re
import time
from xml.sax.saxutils import unescape


class TouTiao(object):

    def __init__(self):
        self.headers_one = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'tt_webid=6628733243796178436; tt_webid=6628733243796178436; csrftoken=3a6f2dc0f315bd1fe957319a75bba4ed; uuid="w:2203d39caf3249c0bcda19ee5839b850"; UM_distinctid=1675827673a27a-0dd556679b3f63-3a3a5d0c-15f900-1675827673b22c; __tasessionId=qb2c0x9mb1543386267822; CNZZDATA1259612802=992935523-1543369669-%7C1543385869',
        'referer': 'https://www.toutiao.com/ch/news_car/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    }


        self.old_url_list_file = open('./../toutiao/old_url_list.json', 'r+')  # 打开文件初始化历史url列表
        self.old_url_data = self.old_url_list_file.readlines()
        self.old_url_list_file.close()  # 关闭上面的文件
        self.new_url_file = open('./../toutiao/new_url_file.json', 'w')  # 初始化中打开一个最新新闻的url列表的存放文件，以供爬虫的增量爬取
        self.new_url_list = []

        # 打开json文件
        # self.news_jsonfile = open('./toutiao_newsfile.json', 'wb')
        # self.comment_jsonfile = open('./toutiao_commentfile.json', 'wb')
        # 搜集问答类网页的列表
        self.questions_list = []

        self.is_fresh = False

    def get_page(self):

        proxy = [
            '--proxy=%s' % "222.185.137.143:4216",  # 设置的代理ip
            '--proxy-type=http',  # 代理类型
            '--ignore-ssl-errors=true',  # 忽略https错误
        ]
        self_webdrive = webdriver.Chrome()  # Get local session of Chrome
        self_webdrive.set_page_load_timeout(30)
        # self_webdrive = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args=proxy)
        try:

            self_webdrive.get("https://www.toutiao.com/ch/news_car/")  # Load page
            time.sleep(10)
        except:
            print('超时')
            self_webdrive.refresh()
            time.sleep(10)
            try:
                self_webdrive.find_element_by_xpath('.//div[@class="title-box"]')
            except:
                self.is_fresh = True

            while self.is_fresh:
                print('页面刷新重试中......')
                self_webdrive.refresh()
                time.sleep(10)
                try:
                    self_webdrive.find_element_by_xpath('.//div[@class="title-box"]')
                    self.is_fresh = False
                except:
                    pass


        print('获取页面中.....')
        # time.sleep(10)
        cheshi_data = self_webdrive.page_source
        cheshi_data = etree.HTML(cheshi_data)
        ceshi_data_list = cheshi_data.xpath('.//li[@class="item    "]/div/div[1]')
        if ceshi_data_list:
            j = 4000  # 设定翻页的最大数， 建议不要设置太大，否者selenium会卡顿
            k = 0
            for i in range(j):
                print('第{}/{}次翻页'.format(str(i), str(j)))
                time.sleep(0.1)
                # if k > 10:
                #     time.sleep(8)
                #     k = 0
                # k += 1
                ActionChains(self_webdrive).key_down(Keys.DOWN).perform()
            data = self_webdrive.page_source
            data = etree.HTML(data)
            data_list = data.xpath('.//li[@class="item    "]/div/div[1]')
            for child in data_list:
                url = child.xpath('.//div/div[1]/a/@href')[0]
                source_author = child.xpath('.//div/div[1]/a/text()')
                source_author = ''.join(source_author)
                if '悟空问答' not in source_author:  # 筛选掉悟空问答的链接，可以在此处修改
                    print(source_author)
                    url = 'https://www.toutiao.com/a' + url.split('/')[2]
                    if (url + '\n') not in self.old_url_data:  # 如果url不在历史数据中

                        if url != 'https://www.toutiao.com/apc':
                            self.new_url_list.append(url)  # 将新的url添加进新的url列表中
                            self.old_url_data.append(url)  # 将新的url添加进判断url列表中， 做去重使用
                            with open('./../toutiao/old_url_list.json', 'a') as f:  # 打开历史数据的url文件，将新的url写入，保存url记录
                                f.write(url + '\n')
                            self.new_url_file.write(url + '\n')
                        # try:
                        #     time.sleep(3)
                        #     self.get_news_page(url)
                        # except Exception as e:
                        #     print(e)
            print(self.old_url_data)
            print(self.new_url_list)
        else:
            print('首页未加载......')
            self_webdrive.quit()

    # def get_news_page(self, url):
    #     item = {}
    #     response = requests.get(url, headers=self.headers_one)
    #     data_all = response.content.decode()
    #     try:
    #         data = re.search(r"articleInfo: {([\s\S]*time: '\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",data_all).group(1)
    #         data = '{' + data + "'}}"
    #         print(data)
    #         data = re.sub('\n', '', data)
    #         data = unescape(data)
    #         data = data.replace('&quot;', '"').replace('&#x3D;', '=')
    #         content = re.search('content: ([\s\S]*)groupId', data).group(1).strip()[1:][:-2]
    #         content = etree.HTML(content)
    #         text = content.xpath('.//p//text()')
    #         text_con = ''.join(text)
    #         date, create_time = re.search('(\d{4}-\d{1,2}-\d{1,2}) (\d{1,2}:\d{1,2}:\d{1,2})', data).group(1, 2)
    #         id_num = re.search("groupId: '(\d{1,50}).*itemId", data).group(1)
    #         source = re.search("source: '(.*)time", data).group(1).strip()[:-2]
    #         comment_count = re.search("commentCount: '(\d{0,10})[\s\S]*ban_comment", data_all).group(1)
    #         item['content'] = text_con
    #         item['id'] = id_num
    #         item['source'] = source
    #         item['date'] = date
    #         item['time'] = create_time
    #         item['comment_count'] = comment_count
    #         self.write_news_jsonfile(item)
    #     except AttributeError:
    #         print('问答类网页', url)
    #         self.questions_list.append(url)
    #         print(self.questions_list)

    # # 写入json文件
    # def write_news_jsonfile(self, item):
    #     item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
    #     self.news_jsonfile.write(item.encode("utf-8"))
    #
    # def write_comment_jsonfile(self, item):
    #     item = json.dumps(dict(item), ensure_ascii=False) + ',\n'
    #     self.comment_jsonfile.write(item.encode("utf-8"))
    #
    def close_file(self):
    #     self.news_jsonfile.close()
    #     self.comment_jsonfile.close()
        self.new_url_file.close()

    def run(self):
        self.get_page()
        self.close_file()


if __name__ == "__main__":
    toutiao = TouTiao()
    toutiao.run()
