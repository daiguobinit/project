import json
import ast
import re
import traceback
import requests


class CssPojie(object):
    def __init__(self, url):
        self.url = url

        # 列表
        self.class_name_list = []

        # Y轴字典
        self.y_num_dict = {}

        # svg 内容
        self.svg_content = {}

    def get_css_page(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 's3plus.meituan.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        data = response.text
        # print(response.status_code)
        # print(data)
        data = data.replace(' ', '').replace('{', ':{').split(";}")
        # print(data)
        data = data[:-1]
        item_svg = self.parse_css_content(data)
        return item_svg

    def parse_css_content(self, data):

        item = {}  # css坐标字典
        class_list = []

        for i in data:
            try:
                data_child = str(re.search('(\d{0,5}).0px(-\d{0,5}).0px', i).group(1,2)).replace("('", '').replace("', '", '').replace("')", '')

                data_name = i.split(':')[0].split('.')[1]
                # print(data_name, data)
                # if 'xha' in data_name:
                #     num = int(str(data_child).split('-')[1])
                #     if num not in high:
                #         high.append(num)
                data_child = '{"' + data_child + '":"' + data_name +'"}'
                data_child = json.loads(data_child)
                # print(data)
                item.update(data_child)  # 将符合的css坐标添加坐标字典
            except AttributeError:
                # print(i, 333333)

                type_id = re.search('="([a-z]{2,3})"', i).group(1)
                # print(type_id)  # class name  efy,xpy,ieu
                class_list.append(type_id)  # 将svg图片中的分类的class name 添加进列表，供后续使用
                text_dict = re.search('{.*', i).group(0)
                # print(text_dict)
                width = re.search('width:(\d{0,5})px;', i).group(1)  # width 这个字段用来计算数字类的图片的起始位置的px
                # print(width)
                # 获取svg图片内容的链接
                svg_url = re.search(r'background-image:url\(//(.*)\);', i).group(1)
                svg_url ='http://' + svg_url
                # print(svg_url)
                # margin-left 通过获取这个字段来判断是数字类图片，还是汉字类图片,如果有则是数字类图片，没有则是汉字类图片
                margin_left = re.search('margin-left:.*px', i)
                if margin_left:  # 数字类
                    response = requests.get(svg_url)  # 请求svg图片的链接，获取svg图片信息
                    txt = response.text
                    # print(txt)
                    data_list = re.findall('<text.*">(\d{0,100})</text>', txt)
                    # print(data_list)
                    text_data = {}
                    new_data_list = []
                    for j in data_list:
                        i = j.encode('utf-8').decode('utf-8')
                        # text_data.append(i)
                        new_data_list.append(i)
                    text_data['num'] = new_data_list
                    # text_data['num'].append(i)
                    text_data['type'] = 'num'
                    text_data['width'] = width
                    # print(text_data)
                    self.svg_content[type_id] = text_data
                else:  # 汉字类
                    response = requests.get(svg_url)
                    txt = response.text
                    data_list = re.findall('<textPath xlink:href="#\d{0,4}" textLength="\d{0,4}">(.*)</textPath>', txt)
                    text_data = {}  # 一张保存svg图片内容的列表
                    new_data_list = []
                    for j in data_list:
                        i = j.encode('utf-8').decode('utf-8')
                        # text_data.append(i)
                        new_data_list.append(i)
                    text_data['num'] = new_data_list
                    text_data['type'] = 'hanzi'
                    text_data['width'] = width
                    # print(text_data)
                    self.svg_content[type_id] = text_data
            except:
                print(traceback.format_exc())

        class_list_dict = {}
        for name in class_list:  # 遍历保存class name的列表，通过以下代码获取每张svg图片的Y轴的坐标
            class_list_dict[name] = []
            for i in data:
                try:
                    data_child = str(re.search('(\d{0,5}).0px(-\d{0,5}).0px', i).group(1, 2)).replace("('", '').replace("', '", '').replace("')", '')
                    data_name = i.split(':')[0].split('.')[1]
                    # print('------', data_name, data_child)
                    # if name in data_name:
                    if re.match(name, data_name):
                        num = int(str(data_child).split('-')[1])
                        if num not in class_list_dict[name]:
                            class_list_dict[name].append(num)  # 将对应的class name的键值对添加进字典中的列表中
                except:
                    pass

        # print(item)
        # print(class_list_dict)
        # print(self.svg_content)
        item_svg = {}
        for type_id in class_list:
            for i in range(0, len(class_list_dict[type_id])):
                a = self.svg_content[type_id]['num'][i]
                # print(self.svg_content[type_id]['num'])
                css_num = sorted(class_list_dict[type_id])
                # print(css_num)
                # print(a)
                num_id = css_num[i]
                if self.svg_content[type_id]['type'] == 'hanzi':
                    b = 0
                else:
                    b = int((int(self.svg_content[type_id]['width'])+2) / 2)
                    # b = 7
                for p in range(0, len(a)):
                    # b += 14  # 1111
                    try:
                        # print(str(b)+'-{}'.format(str(num_id)),":",a[p])
                        name = str(b)+'-{}'.format(str(num_id))
                        try:
                            # print(item[name])
                            item_svg[item[name]] = str(a[p])
                        except:
                            print(111111, traceback.format_exc())
                    except:
                        print(22222, traceback.format_exc())
                    b += int(self.svg_content[type_id]['width'])

        # print(item_svg)
        # print(len(item_svg))
        return item_svg

    def run(self):

        return self.get_css_page()


if __name__ == "__main__":
    url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/c67ccdf6fe74ff673cb2581bb87a5d17.css'
    css_parse = CssPojie(url)
    css_parse.run()
