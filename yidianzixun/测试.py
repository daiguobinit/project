import execjs
import requests

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=1683bb2492431a-094bc6de6a2a34-5d1e331c-15f900-1683bb249257ee; JSESSIONID=6d9c89ea908ad4018a5737264c1083c0cf3bb7f05104577e6b7f7deebfed12e7; wuid=789835887113804; wuid_createAt=2019-01-16 9:36:16; weather_auth=2; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1547602576; CNZZDATA1255169715=432644633-1547597213-http%253A%252F%252Fwww.yidianzixun.com%252F%7C1547597213; captcha=s%3A229eaf5dc322b2b9390527804ef8124c.yGCMPLr%2FjIqPwCriUMcf0ZznNz7D3ZAabmz2DZWLIVM; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1547604886; cn_1255169715_dplus=%7B%22distinct_id%22%3A%20%221683bb2492431a-094bc6de6a2a34-5d1e331c-15f900-1683bb249257ee%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201547604876%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201547604876%7D%7D',
    'Host': 'www.yidianzixun.com',
    'Referer': 'http://www.yidianzixun.com/channel/c11',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=11722850328&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&_spt=yz~eaod%3B%3B%3D882%3F%3A982%3A%3B%3A&appid=web_yidian&_=1547604885104'
response = requests.get(url)
print(response.text)