# #coding:UTF-8
import time
from datetime import datetime
from datetime import timedelta
#
# 531987016061   1542335263.313
timestamp = '1544923517'
# timestamp = timestamp[:10] + '.' + timestamp[-3:]
#
# #转换成localtime
time_local = time.localtime(float(timestamp))
#转换成新的时间格式(2016-05-05 20:28:54)
dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)  # "%Y-%m-%d %H:%M:%S"
#
print(dt)
# # for i in range(1, 11):
# #     print(i)
#
# get_time = time.time()
# # str_time = str(get_time)[:-4]
# date = datetime.now() - timedelta(days=7)
# a = str(date).split(' ')[0]
# # timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
# # # 转换为时间戳:
# # timeStamp = int(time.mktime(timeArray))
# # end_time = str(timeStamp) + '.001'
# print(str(datetime.now()).split(' ')[0])
# print(a)
#

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
# LOG_FORMAT = "%(asctime)s %(filename)s %(levelname)s %(lineno)d %(message)s "  # 配置输出日志格式
# DATE_FORMAT = '%Y-%m-%d  %H:%M:%S '   # 配置输出时间的格式，注意月份和天数不要搞乱了
# file_name = r"./timed_task-{}.log".format(str(datetime.now()).split(' ')[0])
# logging.basicConfig(level=logging.DEBUG,
#                     format=LOG_FORMAT,
#                     datefmt=DATE_FORMAT,  # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
#                     )
# headle = logging.FileHandler(filename=file_name, encoding='utf-8')
# logger = logging.getLogger()
# logger.addHandler(headle)
#
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(10)
# }
#
# sched= BlockingScheduler(executors=executors)
#
#
# def zhihu():
#     print('知乎爬虫任务开启......')
#
#
# def xiaohongshu():
#     raise IndexError
#     # print('小红书爬虫任务开启......')


# sched.add_job(func=zhihu, trigger='cron', hour=17, minute=27, second=3, id='zhihu')
# sched.add_job(func=xiaohongshu, trigger='cron', hour=17, minute=27, second=3, id='xiaohongshu')
#
#
# def err_listener(ev):
#     if ev.exception:
#         logging.info(traceback.format_exc())
#     else:
#         logging.info('{} miss'.format(str(ev.job)))
#
#
# sched.add_listener(err_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

# print('定时任务开启')
# logging.info('定时任务开启')
# sched.start()
# sched.print_jobs()
