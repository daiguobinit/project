import requests
from lxml import etree
import uuid


headers = {
    'Cookie': '__mta=188618391.1545359031056.1545359031056.1545359031056.1; _lxsdk_cuid=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _lxsdk=167c944a374c8-0367edd4469fcb-5d1e331c-15f900-167c944a374c8; _hc.v=f1b4e908-09e1-96ed-8f92-b4bb681c5966.1545269980; dper=7d7f2fc7cdd242974d2b259b2c75ca7e8648c47620fec8ef82796aa30d5be07d9a6ce08a4b544e50ed734b716dee6a45712672cd403d7b3baeb8b546d0f33f8ad8b86955c52b409b69a75ced67f864780bdda60d0f96880f9b5b5392ce8b8e44; ua=%E5%88%AB%E9%82%A3; ctu=0e996ce0644db9ede257ad23843b309df390781b7ecdd57481956f9ef8a41718; s_ViewType=10; aburl=1; cy=1; cye=shanghai; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; ll=7fd06e815b796be3df069dec7836c3df; m_flash2=1; cityid=1; pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTQ1NzEzNzMwMTIxXV9b; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s={}'.format(uuid.uuid4()),
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/search/keyword/1/10_%E5%98%89%E9%87%8C%E4%B8%AD%E5%BF%83/g101r812',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def run():
    url = 'http://www.dianping.com/shop/93632901/review_all/p1'
    response = requests.get(url, headers=headers)
    print(response.text)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    comment = html.xpath('//div[@class="reviews-items"]/ul/li')
    for i in comment:
        xx = i.xpath('./div/div[@class="review-words"]')[0].xpath('string(.)')
        print(xx)

if __name__ == '__main__':
    run()