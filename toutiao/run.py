import os
import time

print('今日头条selenium启动')   # 爬取第一遍
os.system('python ./../toutiao/toutiao_sele.py')
print('新闻详情页爬取')
os.system('python ./../toutiao/toutiao.py')

print('暂停900s后进行下一轮爬取')
time.sleep(900)

print('今日头条selenium启动')  # 爬取第二遍
os.system('python ./../toutiao/toutiao_sele.py')
print('新闻详情页爬取')
os.system('python ./../toutiao/toutiao.py')

print('暂停900s后进行下一轮爬取')
time.sleep(900)

print('今日头条selenium启动')  # 爬取第三遍
os.system('python ./../toutiao/toutiao_sele.py')
print('新闻详情页爬取')
os.system('python ./../toutiao/toutiao.py')

print('暂停900s后进行下一轮爬取')
time.sleep(900)

print('今日头条selenium启动')  # 爬取第四遍
os.system('python ./../toutiao/toutiao_sele.py')
print('新闻详情页爬取')
os.system('python ./../toutiao/toutiao.py')

print('暂停900s后进行下一轮爬取')
time.sleep(900)

print('今日头条selenium启动')  # 爬取第五遍
os.system('python ./../toutiao/toutiao_sele.py')
print('新闻详情页爬取')
os.system('python ./../toutiao/toutiao.py')


time.sleep(120)
print('小红书任务启动.....')
os.system('python ./../xiaohongshu/xiaohongshu_selenium.py')
print('小红书爬虫任务开启......')

print('爬取完毕.....')