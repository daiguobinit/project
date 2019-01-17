import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.gevent import GeventScheduler

# from zhihu.zhihu import *
import os
from datetime import datetime
from datetime import timedelta
import logging
import traceback
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED

# 设置日志记录
LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
yesterday = str(yesterday).split(' ')[0]
file_name = r"./timed_task-{}.log".format(str(datetime.now()).split(' ')[0])
logging.basicConfig(level=logging.DEBUG,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,  # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )
headle = logging.FileHandler(filename=file_name, encoding='utf-8')
logger = logging.getLogger()
logger.addHandler(headle)

executors = {
    # 'default': ThreadPoolExecutor(20),  # 线程
    'processpool': ProcessPoolExecutor(15)  # 进程   两者可同时启用也可以单独启用
}
sched = BlockingScheduler(executors=executors)
sched_two = BackgroundScheduler(executors=executors)


def zhihu():
    os.system('python ./../zhihu/zhihu.py')
    print('知乎爬虫任务开启......')

def xiaohongshu():
    os.system('python ./../xiaohongshu/xiaohongshu_selenium.py')
    print('小红书爬虫任务开启......')


def dianping():
    os.system('python ./../dazhongdianping/dianping.py')
    print('大众点评任务开启......')

def hupu():
    os.system('python ./../hupu/hupu.py')
    print('虎扑任务开启......')

def wangyi():
    os.system('python ./../wangyi/newcarts.py')
    print('网易新闻任务开启......')

def tencent():
    os.system('python ./../tencent/newcarts.py')
    print('腾讯新闻任务开启......')

def yidian():
    os.system('python ./../yidianzixun/yidianzixun.py')
    print('一点资讯任务开启......')

def ifeng():
    os.system('scrapy crawl ifeng')
    os.system('python ./../chance/zimeiti.py')
    print('凤凰网任务开启......')

def jiemian():
    os.system('python ./../jiemian/jiemian_spider.py')
    print('界面新闻任务开启......')

def mop():
    os.system('python ./../mop/mop_spider.py')
    print('猫扑新闻任务开启......')

def sina():
    os.system('python ./../sina/newcarts.py')
    print('新浪网任务开启......')

def souhu():
    os.system('python ./../souhu/souhu.py')
    print('搜狐网任务开启......')

def toutiao():
    os.system('python ./../toutiao/run.py')
    print('今日头条任务开启......')


# sched.add_job(func=yidian, trigger='cron', hour=9, minute=21, second=3, id='yidian', max_instances=2)
# sched.add_job(func=jiemian, trigger='cron', hour=9, minute=21, second=3, id='jiemian', max_instances=2)
sched.add_job(func=toutiao, trigger='cron', hour=0, minute=2, second=3, id='toutiao', max_instances=2)
# sched.add_job(func=xiaohongshu, trigger='cron', hour=9, minute=21, second=3, id='xiaohongshu', max_instances=2)


def err_listener(event):
    if event.exception:
        logging.error(traceback.format_exc())
    else:
        logging.info('{} miss'.format(str(event.job)))


sched_two.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

print('定时任务开启')
logging.info('定时任务开启')
sched.start()




