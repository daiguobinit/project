# coding=gbk
import requests
from lxml import etree
import json
import re
import time
from datetime import datetime
from datetime import timedelta
import logging
import traceback
from ippro.proxies import res_ip
import random
import uuid
from css_pojie import CssPojie


# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
file_name = r"./dianping-{}.log".format(str(datetime.now()).split(' ')[0])
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

        # ip
        ip = res_ip()
        self.ip_one = ip
        self.ip_two = ip
        print('使用IP：{}'.format(ip))
        self.user_agent = [
            'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
        ]

        # 去重列表
        self.set_list = []
        # 表示商铺css样式坐标链接
        self.shop_css_url = ''
        # 表示商铺css坐标字典
        self.shop_css_dict = {}

        # 表示评论css样式坐标的链接
        self.css_url_first = ''
        # 评论css坐标字典
        self.css_list = {}

    # 获取搜索页面
    def get_serach_page(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'Cookie': 'navCtgScroll=0; _lxsdk_cuid=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _lxsdk=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _hc.v=f1b4e908-09e1-96ed-8f92-b4bb681c5966.1545269980; thirdtoken=abd3d7c7-e2e4-4b41-b231-dded6297e0cc; uamo=15638829723; dper=7d7f2fc7cdd242974d2b259b2c75ca7e8648c47620fec8ef82796aa30d5be07d9a6ce08a4b544e50ed734b716dee6a45712672cd403d7b3baeb8b546d0f33f8ad8b86955c52b409b69a75ced67f864780bdda60d0f96880f9b5b5392ce8b8e44; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%88%AB%E9%82%A3; ctu=0e996ce0644db9ede257ad23843b309df390781b7ecdd57481956f9ef8a41718; s_ViewType=10; aburl=1; cy=1; cye=shanghai; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; _lxsdk_s=167cf52b312-e53-0cc-661%7C%7C21',
            # 'Referer': 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

        response = requests.get(url, headers=headers, proxies={'http': self.ip_one})  # , proxies={'http': self.ip_one}
        content = etree.HTML(response.content.decode())

        # 这个模块可以获取父级节点 ------------------------
        url_list = content.xpath('.//div[@id="classfy"]/a[@data-cat-id]/@href')
        print(url_list)
        for child_url in url_list:
            with open('url_shop_father_two.txt', 'a') as f:
                f.write(child_url + '\n')
            # ------------------------------------------------------------

            # # 获取所有的子级节点中的商铺信息 ---------------------------
            # child_response = requests.get(child_url, headers=headers, proxies={'http': self.ip_one})  # , proxies={'http': self.ip_one}
            # data = etree.HTML(child_response.content.decode())
            # shop_url_list = data.xpath('.//div[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href')
            # print('-------------', shop_url_list)
            # if shop_url_list:
            #     for shop_url in shop_url_list:
            #         print('2222222222222222222222', shop_url)
            #         if shop_url not in self.set_list:
            #             with open('url_shop_two.txt', 'a') as f:
            #                 f.write(shop_url + '\n')
            #             self.set_list.append(shop_url)
            #             # self.get_shop_page(shop_url, url)
            #             # time.sleep(1)
            #
            #     next_page_url_list = content.xpath('.//div[@class="page"]/a[@class="next"]/@href')
            #     if next_page_url_list:
            #         print('3333333333333333333333333')
            #         self.get_serach_page(next_page_url_list[0])
            # else:
            #     try:
            #         self.ip_one = res_ip()
            #     except:
            #         time.sleep(3)
            #         self.ip_one = res_ip()
            #         self.get_serach_page(url)
        # -------------------------------------------------------------------

    # 获取商铺详情页
    def get_shop_page(self, url, up_url):
        user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/536.6',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.1',
        ]

        Cookies = [
            '_lxsdk_s=b458c64cc9ef92adce92c199a6b7%7C%7C4; __mta=214784936.1512623224439.1512623224439.1512623226558.2; client-id=8d050bd8-51b6-46fc-be96-cb6871d91fe7; ci=89; webloc_geo=31.778615%2C119.958931%2Cwgs84; _lxsdk=1602f5eb154c8-05c63a41825c168-1b451e24-13c680-1602f5eb154c8; uuid={}',
            '_lxsdk_s=55618265813fc43043ce562acf29%7C%7C2; ci=89; __mta=252597174.1512623399814.1512623399814.1512623399814.1; _lxsdk=1602f6161c1c8-034ae66c3842d88-1b451e24-13c680-1602f6161c170; client-id=8ca2fe5f-ba96-41ae-b919-f8d3665e2f10; webloc_geo=31.778620%2C119.958935%2Cwgs84; uuid={}',
            '_lxsdk_s=4ffb12d5a90c2361745e6d0993a2%7C%7C2; ci=89; __mta=40613533.1512623465821.1512623465821.1512623465821.1; client-id=a31f1c79-3287-4ef1-8bd3-56bfb431a7da; webloc_geo=31.778616%2C119.958936%2Cwgs84; _lxsdk=1602f6262117d-0f173d7fde38d18-1b451e24-13c680-1602f626212c8; uuid={}',
            '_lxsdk_s=4ba654e682eaf4d69efb90ae9cf1%7C%7C2; __mta=152351622.1512623525333.1512623525333.1512623525333.1; ci=89; client-id=e8101f58-a778-4332-81c2-75ba410b2bb3; webloc_geo=31.778611%2C119.958934%2Cwgs84; _lxsdk=1602f634c448d-0c74adf6d00e2e8-1b451e24-13c680-1602f634c45c8; uuid={}',
            '_lxsdk_s=f6511ca715103c33b7bb4aea1e9f%7C%7C2; __mta=40629917.1512623573270.1512623573270.1512623573270.1; ci=89; client-id=c69db65e-b5d1-4fe6-aa7a-340e3608aeb6; webloc_geo=31.778617%2C119.958930%2Cwgs84; _lxsdk=1602f64072fc8-04cf33034885b08-1b451e24-13c680-1602f640730c8; uuid={}',
            '_lxsdk_s=38327d7cfda78d0cfc4810838c32%7C%7C2; __mta=150795529.1512623625315.1512623625315.1512623625315.1; ci=89; client-id=221306b1-bfb7-4cfa-ab3f-2e4a85089864; webloc_geo=31.778610%2C119.958933%2Cwgs84; _lxsdk=1602f64d24531-0623a27320ba75-1b451e24-13c680-1602f64d246c8; uuid={}',
            '_lxsdk_s=c2f111bde916cad4d653e07a35c9%7C%7C2; __mta=42950426.1512623702441.1512623702441.1512623702441.1; _lxsdk=1602f66000dc8-0bb60c750cf17b8-1b451e24-13c680-1602f66000d7f; ci=89; client-id=38cc3a86-fe57-491b-8564-c9b1a251cd4a; webloc_geo=31.778617%2C119.958931%2Cwgs84; uuid={}',
            '_lxsdk_s=fd711080efee1adf6de57c1d4c88%7C%7C2; ci=89; webloc_geo=31.778612%2C119.958939%2Cwgs84; __mta=218070313.1512623752950.1512623752950.1512623752950.1; _lxsdk=1602f66c53e35-0b363d23b0e435-1b451e24-13c680-1602f66c53fc8; client-id=1a4a2af3-4201-4e61-bf26-92016709444b; uuid={}',
            '_lxsdk_s=810677247f21b53cd75826e60cb8%7C%7C2; __mta=146594315.1512623869611.1512623869611.1512623869611.1; _lxsdk=1602f688ce80-074a1ec97ff043-1b451e24-13c680-1602f688ce9c8; ci=89; client-id=e60488fa-51fe-4d12-99a3-257a5a0853cc; webloc_geo=31.778609%2C119.958928%2Cwgs84; uuid={}',
            '_lxsdk_s=c44c26606c13c651ab5a20447428%7C%7C2; __mta=89516452.1512623906613.1512623906613.1512623906613.1; _lxsdk=1602f691da0c8-024ebcb15833bc-1b451e24-13c680-1602f691da04b; ci=89; client-id=a6846506-a50a-4612-8106-ff31978802a8; webloc_geo=31.778607%2C119.958929%2Cwgs84; uuid={}',
            '_lxsdk_s=071dfe26ce64d6e46d03323d2f71%7C%7C2; __mta=210099498.1512623985254.1512623985254.1512623985254.1; ci=89; client-id=f2cea0fa-0d83-479a-a863-f2b7156fb392; webloc_geo=31.778621%2C119.958925%2Cwgs84; _lxsdk=1602f6a4f88c8-0ce1602d9c121a-1b451e24-13c680-1602f6a4f88c8; uuid={}',
            '_lxsdk_s=833017bd50026c6c57b327f1f51a%7C%7C2; __mta=244702778.1512624031536.1512624031536.1512624031536.1; ci=89; client-id=ec7106e4-9dda-4ce0-aa8d-c12288812644; webloc_geo=31.778622%2C119.958921%2Cwgs84; _lxsdk=1602f6b0459c8-011b3f8b51c9328-1b451e24-13c680-1602f6b045ac8; uuid={}',
            '_lxsdk_s=9a68aaba42beb1ebdfc3e726d94e%7C%7C2; ci=89; webloc_geo=31.778629%2C119.958912%2Cwgs84; __mta=45406747.1512624277952.1512624277952.1512624277952.1; _lxsdk=1602f6ec7b84-095c2ecf9438458-1b451e24-13c680-1602f6ec7b9c8; uuid=33acafd1-4a03-4f0f-9572-1ccbfd570efc; client-id={}',
            '_lxsdk_s=c1508df449b0616ba37c5d9166f2%7C%7C2; __mta=216814121.1512624317347.1512624317347.1512624317347.1; ci=89; client-id=5d8e3ff2-5370-4c08-855e-9d26e5187040; webloc_geo=31.778633%2C119.958912%2Cwgs84; _lxsdk=1602f6f6187a2-029abec138ea508-1b451e24-13c680-1602f6f6188c8; uuid={}',
            '_lxsdk_s=7a249ecc9a048cbb826ea3b1f4e7%7C%7C2; __mta=256753588.1512624355644.1512624355644.1512624355644.1; _lxsdk=1602f6ff822c8-01f025c7119f968-1b451e24-13c680-1602f6ff823c8; ci=89; client-id=33339c7c-4dd0-4da8-8617-add389e72438; webloc_geo=31.778634%2C119.958912%2Cwgs84; uuid={}',
            '_lxsdk_s=93f6847b5f37e552ae083beb48c2%7C%7C2; __mta=218397606.1512624389136.1512624389136.1512624389136.1; ci=89; client-id=21540b20-0240-48fa-ae1e-c1ce4dba892f; webloc_geo=31.778631%2C119.958925%2Cwgs84; _lxsdk=1602f707a3d3-0d7db668e6d9498-1b451e24-13c680-1602f707a3ec8; uuid={}',
            '_lxsdk_s=0ffdd4e2dddd57d3c05606eb82f3%7C%7C2; __mta=141367821.1512624428164.1512624428164.1512624428164.1; ci=89; client-id=d6e8de67-48b8-4262-b3b3-47851c46db5c; webloc_geo=31.778620%2C119.958977%2Cwgs84; _lxsdk=1602f7112b9c8-09d6e858772c1d8-1b451e24-13c680-1602f7112bac8; uuid={}',
            ]

        cook = random.choice(Cookies)
        cook = cook.format(uuid.uuid4())
        headers_three = {
            # 'Cookie': 'Cookie: cy=1; cye=shanghai; _lxsdk_cuid=167ce86cb5cc8-0ef0bb253f622a-c343567-15f900-167ce86cb5cc8; _lxsdk=167ce86cb5cc8-0ef0bb253f622a-c343567-15f900-167ce86cb5cc8; _hc.v=6c8d00bc-7fd5-adef-2b8f-8ea0623850c7.1545358200; s_ViewType=10; ua=%E3%80%81%E5%94%90%E5%AE%8B_8205; ctu=baaf5442d52416965af0cf11004f094d95add57d4366fa42d38f98e316f2c8cc; uamo=13912816467; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s={}'.format(random.choice(cookies_list)),
            'Cookie': cook,
            'Host': 'www.dianping.com',
            'Referer': up_url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': '{}'.format(random.choice(user_agent))
        }

        print(111, url)
        try:
            response = requests.get(url, headers=headers_three, proxies={'http': self.ip_two})  # , proxies={'http': self.ip_two}
            print(response.status_code)
            data = response.content.decode()

            # print(data)
            if '页面不存在' in data or '页面无法访问' in data:
                try:
                    self.ip_two = res_ip()
                except IndexError:
                    time.sleep(2)
                    self.ip_two = res_ip()
                print('ip被封，更换ip中......')
                print('更换ip为：{}'.format(self.ip_two))
                logging.warning('爬取店铺信息的IP被封，更换IP为：{}'.format(self.ip_two))
                self.get_shop_page(url, up_url)
            else:
                css_url = re.search(r'//s3plus.meituan.net/.*/svgtextcss/[a-z0-9]*\.css', response.text)[0]  # 通过正则匹配出css样式定位的css链接
                print(css_url)
                css_url = 'http:' + css_url
                if css_url != self.shop_css_url:  # 如果css样式变更，则会获取和生成新的css样式字典
                    logging.info('新的css样式链接：{}'.format(css_url))
                    css_pojie = CssPojie(css_url)
                    item_svg = css_pojie.get_css_page()
                    logging.info('新的css样式字典：{}'.format(str(item_svg)))
                    self.shop_css_dict = item_svg
                    self.shop_css_url = css_url
                shop_item = {}
                data = etree.HTML(data)
                tel = data.xpath('.//div[@id="basic-info"]/p/text() | .//div[@id="basic-info"]/p/d/@class')
                tel = self.change_shop_css_index(tel)
                # 店铺名称
                shop_name = data.xpath('.//h1[@class="shop-name"]/text()')[0]
                shop_item['shop_name'] = shop_name
                # 星级
                star_level = data.xpath('.//div[@class="brief-info"]/span[1]/@title')[0]
                shop_item['star_level'] = star_level
                shop_item['tel'] = tel
                # 人均
                per_capita = data.xpath('.//span[@id="avgPriceTitle"]/text() | .//span[@id="avgPriceTitle"]/child::*/@class')
                per_capita = self.change_shop_css_index(per_capita)
                shop_item['per_capita'] = per_capita
                # 口味
                taste = data.xpath('.//span[@id="comment_score"]/span[1]/text() | .//span[@id="comment_score"]/span[1]/child::*/@class')
                taste = self.change_shop_css_index(taste)
                shop_item['taste'] = taste
                # 环境
                environment = data.xpath('.//span[@id="comment_score"]/span[2]/text() | .//span[@id="comment_score"]/span[2]/child::*/@class')
                environment = self.change_shop_css_index(environment)
                shop_item['environment'] = environment
                # 服务
                serve = data.xpath('.//span[@id="comment_score"]/span[3]/text() | .//span[@id="comment_score"]/span[3]/child::*/@class')
                serve = self.change_shop_css_index(serve)
                shop_item['serve'] = serve
                # 地址
                address = data.xpath('.//span[@id="address"]/text() | .//span[@id="address"]/child::*/@class')
                address = self.change_shop_css_index(address)
                shop_item['address'] = address
                # 评论数
                comment_count = data.xpath('.//span[@id="reviewCount"]/text() | .//span[@id="reviewCount"]/child::*/@class')
                comment_count = self.change_shop_css_index(comment_count)
                shop_item['comment_count'] = comment_count

                shop_item['url'] = url
                print(shop_item)
                self.write_news_jsonfile(shop_item)

        except requests.exceptions.ProxyError:
            print('ip出现问题')
            self.ip_two = res_ip()
            self.get_shop_page(url, up_url)
            # print(traceback.format_exc())

    def get_comment(self, shop_id):
        headers = {
            'Cookie': '__mta=188618391.1545359031056.1545359031056.1545359031056.1; _lxsdk_cuid=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _lxsdk=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _hc.v=f1b4e908-09e1-96ed-8f92-b4bb681c5966.1545269980; dper=7d7f2fc7cdd242974d2b259b2c75ca7e8648c47620fec8ef82796aa30d5be07d9a6ce08a4b544e50ed734b716dee6a45712672cd403d7b3baeb8b546d0f33f8ad8b86955c52b409b69a75ced67f864780bdda60d0f96880f9b5b5392ce8b8e44; ua=%E5%88%AB%E9%82%A3; ctu=0e996ce0644db9ede257ad23843b309df390781b7ecdd57481956f9ef8a41718; s_ViewType=10; aburl=1; cy=1; cye=shanghai; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; ll=7fd06e815b796be3df069dec7836c3df; m_flash2=1; cityid=1; pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTQ1NzEzNzMwMTIxXV9b; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s={}'.format(uuid.uuid4()),
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

        for i in range(1, 10000):
            time.sleep(1)
            url = 'http://www.dianping.com/shop/{}/review_all/p{}'.format(shop_id, str(i))
            # url = 'http://www.dianping.com/shop/14184826/review_all/p{}'.format(str(i))
            response = requests.get(url, headers=headers, allow_redirects=False, proxies={'http': self.ip_one})
            status_code = response.status_code
            if status_code == 200:
                css_url = re.search('//s3plus.meituan.net/.*/svgtextcss/.*css', response.text)[0]  # 通过正则匹配出css样式定位的css链接
                print(css_url)
                css_url = 'http:' + css_url
                if css_url != self.css_url_first:  # 如果css样式变更，则会获取和生成新的css样式字典
                    logging.info('新的css样式链接：{}'.format(css_url))
                    css_pojie = CssPojie(css_url)
                    item_svg = css_pojie.get_css_page()
                    logging.info('新的css样式字典：{}'.format(str(item_svg)))
                    self.css_list = item_svg
                    self.css_url_first = css_url
                # print(response.text)
                time.sleep(3)
                response.encoding = 'utf-8'
                html = etree.HTML(response.text)
                comment = html.xpath('.//div[@class="reviews-items"]/ul/li')
                if comment:  # 判断是否获取到评论列表，如果为空的话就是没有评论或者评论已经翻页完毕
                    for i in comment:
                        item = {}
                        if i.xpath('./div/div[@class="review-words Hide"]/text()'):

                            xx = i.xpath('./div/div[@class="review-words Hide"]/text() | ./div/div[@class="review-words Hide"]/span/@class')
                        else:
                            xx = i.xpath('./div/div[@class="review-truncated-words"]/text() | ./div/div[@class="review-truncated-words"]/span/@class | .//div/div[@class="review-words"]/text() | .//div/div[@class="review-words"]/span/@class')

                        con = self.change_css_index(xx)
                        con = con.strip()
                        user_name = i.xpath('.//div[@class="dper-info"]/a/text()')[0]
                        grade = i.xpath('.//div[@class="review-rank"]/span/@class')[0]
                        grade = str(re.search('\d{2}', grade).group(0)).replace('0', '')
                        other_info = i.xpath('.//span[@class="score"]//text()')
                        con_t = ''
                        for j in other_info:
                            con_t = con_t + j.strip() + ' '
                        other_info = con_t
                        date_all = i.xpath('.//div[@class="misc-info clearfix"]/span[1]/text()')[0]
                        date = date_all.split(' ')[0].strip()
                        comment_time = date_all.split(' ')[1]
                        shop_name = i.xpath('.//div[@class="misc-info clearfix"]/span[2]/text()')[0]
                        try:
                            likes = i.xpath('.//em[@class="col-exp"]/text()')[0]
                        except:
                            likes = ''
                        if i.xpath('.//img[@class="user-rank-rst "]/@src | .//img[@class="user-rank-rst user-rank-rst-high"]/@src'):
                            lv = i.xpath('.//img[@class="user-rank-rst "]/@src | .//img[@class="user-rank-rst user-rank-rst-high"]/@src')[0]
                            lv = lv.split('/')[-1]
                            lv = re.search('\d{1,2}', lv).group(0)
                        else:
                            lv = ''
                        if i.xpath('.//div[@class="dper-info"]/span/@class'):
                            vip = i.xpath('.//div[@class="dper-info"]/span/@class')[0]
                            if vip == 'vip-gray':
                                is_vip = '否'
                            else:
                                is_vip = '是'
                        else:
                            is_vip = '否'
                        item['shop_name'] = shop_name
                        item['user_name'] = user_name.strip()
                        item['user_lv'] = lv
                        item['is_vip'] = is_vip
                        item['grade'] = grade
                        item['other_info'] = other_info
                        item['date'] = date
                        item['time'] = comment_time
                        item['likes'] = likes
                        shop_url = 'http://www.dianping.com/shop/' + shop_id
                        item['shop_url'] = shop_url
                        item['comment_url'] = url
                        item['content'] = con
                        print(item)
                        self.write_comment_jsonfile(item)
                else:
                    print('未获取到评论')
                    break
            else:
                try:
                    self.ip_one = res_ip()
                except:
                    time.sleep(2)
                    self.ip_one = res_ip()
                logging.info('爬取评论的IP可能被封,更换ip：{}'.format(str(self.ip_one)))

    def change_css_index(self, content_list):
        """
        这个函数用来处理css坐标的，将css坐标替换成对应的文字或数字，返回正确的文本
        :param content_list: 传入的xpath获取的文本列表
        :return: 返回正确的文本内容
        """
        for i in range(len(content_list)):
            a = content_list[i]
            a = a.replace(' ', '')
            one_list = ['1-', '1']
            try:
                if a and a not in one_list:
                    num_one = self.css_list[a]
                    content_list[i] = num_one
            except:
                pass
        content_list = ''.join(content_list)
        return content_list

    def change_shop_css_index(self, shop_list):
        """
        这个函数用来处理css坐标的，将css坐标替换成对应的文字或数字，返回正确的文本
        :param content_list: 传入的xpath获取的文本列表
        :return: 返回正确的文本内容
        """
        for i in range(len(shop_list)):
            a = shop_list[i]
            a = a.replace(' ', '')
            one_list = ['1-', '1']
            try:
                if a and a not in one_list:
                    num_one = self.shop_css_dict[a]
                    shop_list[i] = num_one
            except:
                pass
        shop_list = ''.join(shop_list)
        return shop_list


    # 获取所有的一级链接
    def get_all_shop(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'Cookie': 'navCtgScroll=0; _lxsdk_cuid=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _lxsdk=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _hc.v=f1b4e908-09e1-96ed-8f92-b4bb681c5966.1545269980; thirdtoken=abd3d7c7-e2e4-4b41-b231-dded6297e0cc; uamo=15638829723; dper=7d7f2fc7cdd242974d2b259b2c75ca7e8648c47620fec8ef82796aa30d5be07d9a6ce08a4b544e50ed734b716dee6a45712672cd403d7b3baeb8b546d0f33f8ad8b86955c52b409b69a75ced67f864780bdda60d0f96880f9b5b5392ce8b8e44; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%88%AB%E9%82%A3; ctu=0e996ce0644db9ede257ad23843b309df390781b7ecdd57481956f9ef8a41718; s_ViewType=10; aburl=1; cy=1; cye=shanghai; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; _lxsdk_s=167cf52b312-e53-0cc-661%7C%7C21',
            # 'Referer': 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

        response = requests.get(url, headers=headers, proxies={'http': self.ip_one})  # , proxies={'http': self.ip_one}
        data = etree.HTML(response.content.decode())
        shop_url_list = data.xpath('.//div[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href')
        print('-------------', shop_url_list)
        if shop_url_list:
            for shop_url in shop_url_list:
                print('2222222222222222222222', shop_url)
                if shop_url not in self.set_list:
                    with open('url_shop_two.txt', 'a') as f:
                        f.write(shop_url + '\n')
                    self.set_list.append(shop_url)
                    # self.get_shop_page(shop_url, url)
                    # time.sleep(1)

            next_page_url_list = data.xpath('.//div[@class="page"]/a[@class="next"]/@href')
            if next_page_url_list:
                print('3333333333333333333333333')
                self.get_all_shop(next_page_url_list[0])
        else:
            try:
                self.ip_one = res_ip()
            except:
                time.sleep(3)
                self.ip_one = res_ip()
                self.get_all_shop(url)

    # 写入json文件
    def write_news_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../dazhongdianping/dianping_two.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.news_jsonfile.write(item.encode("utf-8"))

    def write_comment_jsonfile(self, item):
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../dazhongdianping/dianping_commentfile.json', 'ab') as f:
            f.write(item.encode("utf-8"))
        # self.comment_jsonfile.write(item.encode("utf-8"))

    def run(self):

        # 获取商铺父级链接的模块
        url = 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812'
        self.get_serach_page(url)
        # url_list = ['http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g113r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g112r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g117r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g110r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g116r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g111r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g103r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g114r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g219r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g508r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g34236r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g34014r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g102r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g215r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g118r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g115r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g251r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g106r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g3243r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g109r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g6743r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g104r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g34032r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g26481r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g34015r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g34055r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g311r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g25474r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g107r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g2714r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g1783r812', 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g33759r812']

        # 获取所有商铺链接的模块
        for url_one in open('./url_shop_father_two.txt'):
            print('1111111111111111')
            url_one = url_one.strip()
            try:
                self.get_all_shop(url_one)
            except:
                logging.error(traceback.format_exc())


        # 以下模块是获取评论的模块
        # for shop_url in open('./url_shop.txt'):
        #     shop_url = shop_url.strip()
        #     print(shop_url)
        #     # 爬取店铺信息
        #     self.get_shop_page(shop_url, shop_url)
            #
            # 爬取评论部分
            # print(shop_url)
            # shop_id = shop_url.split('/')[-1]
            # self.get_comment(shop_id)
            # time.sleep(1)


if __name__ == "__main__":
    spider = SinaSpider()
    spider.run()
