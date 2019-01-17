from selenium import webdriver
from lxml import etree
import time
import json
from datetime import datetime, date, timedelta
import xlrd


str_time = str(datetime.now()).split(' ')[0]
now_time = str_time.replace('-', '')

class QiChe(object):
    def __init__(self):
        print('开始任务.....')


    def get_page(self, url):
        self_webdrive = webdriver.Chrome()  # Get local session of Chrome
        # self_webdrive = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-windows/bin/phantomjs.exe')
        self_webdrive.set_page_load_timeout(120)
        self_webdrive.get(url)
        time.sleep(5)
        data = self_webdrive.page_source
        data = etree.HTML(data)
        car_list = data.xpath('.//table[@class="tbset"]/tbody/tr/td')  # 顶部的车款列表信息

        car_xi = data.xpath('.//div[@class="subnav-title-name"]/a/text()')[0]

        cart_conf_dict = {}  # 总的字典，
        config_num = 1
        for car in car_list:
            car_name = car.xpath('.//div[@class="carbox"]/div/a/text() | .//div[@class="carbox"]/div/a/span/@class')
            # print(car_name)
            if car_name:
                car_name = self.parse_css_class(self_webdrive, car_name)
                cart_conf_dict['car_' + str(config_num)] = {}  # 这里会根据车款的数量自动生成相应个数的车款字典
                cart_conf_dict['car_' + str(config_num)]['车系'] = car_xi
                cart_conf_dict['car_' + str(config_num)]['车款'] = car_name
            config_num += 1
        tbcs = data.xpath('.//div[@class="conbox"]/table[@class="tbcs"]')

        tbc_num = 0  # table所在的位置,第一个与其他的不同即下标为0
        for tbc in tbcs:  # 一级循环
            if tbc_num == 0:  # 第一个table
                child_tr = tbc.xpath('.//tr')
                for tr in child_tr:
                    th_name = tr.xpath('.//th/div/text()')[0]
                    # print(th_name)
                    tds = tr.xpath('.//td')
                    td_num = 1
                    for td in tds:
                        if td.xpath('.//a'):
                            tr_value = td.xpath('.//div/text() | .//div/span/a/text()')
                            tr_value = ''.join(tr_value)
                            cart_conf_dict['car_' + str(td_num)][th_name] = tr_value.replace('"', '')
                            td_num += 1
                    # tr_td = tr.xpath('.//td/div/text() | .//td/div/span/a/text()')
                    # print(tr_td)
                    # td_num = 1
                    # # print(tr_td)
                    # for tr_value in tr_td:
                    #
                    #     cart_conf_dict['car_' + str(td_num)][th_name] = tr_value.replace('"', '')
                    #     td_num += 1

                tbc_num += 1
            else:
                tr_list = tbc.xpath('.//tr[@id]')
                for tr in tr_list:
                    th = tr.xpath('.//th/div//text() | .//th/div/a/span/@class | .//th/div/span/@class')
                    th_name = self.parse_css_class(self_webdrive, th)
                    time.sleep(0.3)
                    th_name = th_name.replace('"', '')
                    # print(th_name)
                    td_list = tr.xpath('.//td')
                    td_num = 1
                    for td in td_list:

                        if td:
                            if td.xpath('.//div/ul[@class="color-ul"]'):
                                tr_value = td.xpath('.//a/@title | .//span/@title')
                                # print(','.join(tr_value), 55555)
                                tr_value = ','.join(tr_value)
                            else:

                                tr_value = td.xpath('.//div//text() | .//div/span/@class | .//div/p/span/child::*/@class | .//div/i/@class')
                                # print(tr_value)
                                tr_value = self.parse_css_class(self_webdrive, tr_value)
                                # print(tr_value, 3333)

                                tr_value = tr_value.replace('"', '').replace('icons-standard', '●').replace('icons-select', '○').replace('\xa0', '')
                                # print(tr_value, 44444)
                            try:
                                cart_conf_dict['car_' + str(td_num)][th_name] = tr_value
                            except KeyError:
                                break
                            td_num += 1
        for key in cart_conf_dict:  # 写入数据
            item = cart_conf_dict[key]
            # item['url'] = url
            self.write_config_file(item)

        self_webdrive.quit()

    def parse_css_class(self, self_webdrive, car_name):
        """
        将从css样式名中获取content属性值
        :param self_webdrive:
        :param car_name: 传入的xpath获取的列表
        :return: 经过处理的xpath列表，返回正确的，通顺的语句
        """
        for car_class in car_name:
            if car_class != 'icons-standard' and car_class != 'icons-select' and 'hs_kw' in car_class:  # 只对符合的css样式名进行以下操作
                try:
                    index_num = car_name.index(car_class)
                    js = "var win = window.open();console.log(win);win.close();window.getComputedStyle = win.getComputedStyle;var all = document.getElementsByClassName('%s');for(var x = 0;x< all.length;x++){var content =window.getComputedStyle(all[x],'::before').getPropertyValue('content');console.log(content); return content;}" % car_class
                    css_content = self_webdrive.execute_script(js)
                    car_name[index_num] = css_content.replace('"', '')
                except:
                    pass
        car_name = ''.join(car_name)
        return car_name

    def write_config_file(self, item):
        print('正在写入配置数据......')
        item = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open('./../aika_config/qichezhijia_config_2019_1_20.json', 'ab') as f:
            f.write(item.encode('utf-8'))

    def run(self):

        # 打开excel文件
        excel_file = xlrd.open_workbook(r'./url20181031.xlsx')
        aika = excel_file.sheet_by_name('汽车之家')
        colses = aika.col_values(1)
        length = len(colses)
        url_num = 1  # url 在xlsx中的位置
        colses = colses[url_num:]
        for car_url in colses:
            print(car_url, '爬取进度{}/{}'.format(str(url_num), str(length)))
            if car_url:
                car_id = car_url.split('/')[-2]
                url = "https://car.autohome.com.cn/config/series/{}.html".format(str(car_id))
                print('正在爬取配置页url：', url)
                self.get_page(url)
            url_num += 1
        print('爬取完毕......')


if __name__ == "__main__":
    qiche = QiChe()
    qiche.run()