import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import datetime as dt
# from joblib import Parallel,delayed
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie':'XCWEBLOG_testcookie=yes; bitauto_framecity=; CarStateForBitAuto=e90efb04-f507-3e65-84c7-1b0e86c2d747; UserGuid=e99cffbc-d229-4bfc-b0f6-a19feed54b2e; _dc3c=1; BitAutoUserCode=62c0556e-ff89-c960-942d-1bf9a076afad; BitAutoLogId=7869de06a7f921bed028f73968a105b4; Hm_lvt_22edde7a3d9f7292db958737180fa21f=1533778246,1533782235,1534209639,1534209745; CIGDCID=15dd225b7d97be30d5a8acd301aff17e; Hm_lvt_cfe245d2bfde38dcfc0ca2ba84478ad6=1535337745,1537172040,1537234965,1537333426; selectcity=310100; carCssummaryAdCookier=1542951898599; locatecity=310100; bitauto_ipregion=101.86.55.85%3a%e4%b8%8a%e6%b5%b7%e5%b8%82%3b2401%2c%e4%b8%8a%e6%b5%b7%2cshanghai; dc_search10=; Hm_lvt_96d6ae57edf658c0e19e6529cc4fc694=1543541268,1545029118; csids=4742_2748_3821_3152_2334_5398; NewsEstimate6924587=0,0; dcad10=; Hm_lvt_445e24b5f22cacb9d51a837c10e91a3f=1544668741,1545019359,1545369998,1545711327; Hm_lpvt_445e24b5f22cacb9d51a837c10e91a3f=1545711327; Hm_lvt_7b86db06beda666182190f07e1af98e3=1545200771,1545208814,1545370002,1545711328; Hm_lpvt_7b86db06beda666182190f07e1af98e3=1545711328; dmts10=1; bdshare_firstime=1545711329342; __xsptplus12=12.112.1545711331.1545711331.1%232%7Cwww.baidu.com%7C%7C%7C%25E7%25A6%258F%25E7%2591%259E%25E8%25BF%25AA%7C%23%23T-CwApmjCHNzbEh1_idf7SEgOa3ebDn9%23; dmt10=3%7C0%7C0%7Cshanghai.bitauto.com%2F%3Freferrer%3Dhttp%3A%2F%2Fbaa.bitauto.com%2Fbaomax1%2Fthread-15522895.html%7C; dm10=138%7C1545711327%7C1%7Cwww.cheyisou.com%7C%2Fqiche%2F%25e9%2580%2594%25e5%25b2%25b3%2F%7C%7C%7C1535617601%7C1544504607%7C1545625870%7C1545711328%7C15dd225b7d97be30d5a8acd301aff17e%7C0%7C%7C'}

def get_price(car_serial_id):
    car_serial_id = re.findall('[\d]+', str(car_serial_id))[0]
    url = 'http://car.bitauto.com/tree_chexing/sb_{}/'.format(car_serial_id)
    wb_data = requests.get(url,headers = headers)
    content_data = etree.HTML(wb_data.content.decode())
    soup = BeautifulSoup(wb_data.text,'lxml')
    car_type_ids = soup.select('tbody td.txt-left a')
    car_type_ids = list(filter((lambda x:x.get_text().find('上市')==-1),car_type_ids)) # ==-1表示找不到
    # 获取car_type_id和car_type_desc
    for car_type_id in car_type_ids:
        d = {}
        car_type_desc = car_type_id.get_text().strip()
        car_type_id = car_type_id.get('href').strip('/').split('/')[-1]
        car_type_id = re.findall('\d+',car_type_id)[0]
        d['car_serial_id'] = car_serial_id
        d['car_type_id'] = car_type_id
        d['car_type_desc'] = car_type_desc
        # get_car_type_price
        url = 'http://frontapi.easypass.cn/ReferPriceAPI/GetReferPriceByCityCarFront/2401/{}?callback=GetCarAreaPriceListCallback'.format(car_type_id)
        wb_data = requests.get(url)
        items = re.findall('[\d\.]+', wb_data.text)
        d['url'] = 'http://car.bitauto.com/tree_chexing/sb_{}/'.format(car_serial_id)
        d['price_4s'] = items[1] if items[1] else None#MinReferPrice
        d['price_max'] = items[2] if items[2] else None,#MaxReferPrice
        d['price_max'] = d['price_max'][0]
        d['price_official'] = soup.select('#car_filter_id_{} > td > span'.format(car_type_id))[0].get_text()
        d['focus'] = content_data.xpath('.//tr[@id="car_filter_id_{}"]/td[2]/div/div/@style')
        focus = content_data.xpath('.//tr[@id="car_filter_id_{}"]/td[2]/div/div/@style'.format(car_type_id))[0]
        focus = focus.split(' ')[1]
        num = focus.split('%')[0]
        if int(num) > 100 or int(num) < 0:
            focus = '100%'
        d['focus'] = focus
        yield d

if __name__ == '__main__':
    id_file = pd.read_csv(r'D:\PycharmProjects\ipsos_thg\8wang_id\yiche_price\ref\yiche_test.txt', sep='\t')
    car_satus = pd.read_csv(r'D:\PycharmProjects\ipsos_thg\8wang_id\yiche_price\ref\car_status.txt', sep='\t')
    car_type_id = pd.read_excel(r'D:\PycharmProjects\ipsos_thg\8wang_id\yiche_price\ref\car_typ_id.xlsx')
    # car_serial_ids = id_file['yiche_id']
    car_serial_ids = ['3999', '5394']
    df = pd.DataFrame()
    i = 0
    for car_serial_id in car_serial_ids:
        file = pd.DataFrame(get_price(car_serial_id))
        # i += 1
        # time.sleep(0.5)
        # if i % 100 ==0:
        #     print('程序执行进度',i,len(car_serial_ids))
        # try:
        #     file = pd.DataFrame(get_price(car_serial_id))
        #     print(file, 111)
        #     df = df.append(file)
        # except:
        #     print('can not reach price',car_serial_id)

    ddate = dt.datetime.today().strftime("%y%m%d")
    # df['car_type_id'] = df['car_type_id'].astype(int)
    # df = df.merge(car_type_id, on='car_type_id', how='left')
    # df = df[['Ipsos_Model_Level1', 'Ipsos_ID_L1', 'car_serial_id', 'car_type_desc', 'car_type_id', 'price_4s', 'price_max', 'price_official', 'url']]
    # writer = pd.ExcelWriter(r'D:\PycharmProjects\ipsos_thg\8wang_id\yiche_price\result\yiche_price_{}.xlsx'.format(ddate), engine='xlsxwriter',options={'strings_to_urls': False})
    # df.to_excel(writer, sheet_name = 'yiche_price', index=False)
    #
    # weicaiji = id_file.merge(df[['Ipsos_Model_Level1', 'car_serial_id']], on=['Ipsos_Model_Level1'], how='left')
    # weicaiji = weicaiji[weicaiji['car_serial_id'].isnull()]
    # weicaiji = weicaiji.merge(car_satus, on=['Ipsos_Model_Level1', 'yiche_id'], how='left')
    # weicaiji = weicaiji[['Ipsos_Model_Level1', 'yiche_id', '易车网站状态']]
    # weicaiji.to_excel(writer, sheet_name='未采集id状态', index=False)
    # writer.save()
    print(df.shape)
    print('done')