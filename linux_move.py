import os, shutil
import zipfile, tarfile
import time
from datetime import datetime
from datetime import timedelta

now_time = str(datetime.now()).split(' ')[0].replace('-', '_')
# print(now_time)
yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
yesterday = str(yesterday).split(' ')[0]
date_time = yesterday.replace('-', '_')

path = '/home/Cspider/data/chance'

# now_time = '2019_01_13'

for files in os.walk(path):
    list_files = files[-1]
    for file in list(list_files):
        if now_time in file and 'json' not in files[0]:
            # print(file)
            ph = files[0]
            ph = ph.replace('\\', '/')
            path = ph + '/' + file
            print('移动文件中.....')
            shutil.copy(path, '/home/Cspider/data/chance/json')


def compress(get_files_path, set_files_path):
    print('正在打包压缩文件中......')
    f = zipfile.ZipFile(set_files_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(get_files_path):
        fpath = dirpath.replace(get_files_path, '')  # 注意2
        fpath = fpath and fpath + os.sep or ''  # 注意2
        for filename in filenames:
            f.write(os.path.join(dirpath, filename), fpath + filename)
    f.close()
    print("文件打包压缩成功")


def deletefile():
    """删除小于minSize的文件（单位：K）"""
    files_li = os.listdir('/home/Cspider/data/chance/json')  # 列出目录下的文件
    for file in files_li:
        print(file)
        os.remove('/home/Cspider/data/chance/json/' + file)  # 删除文件
        print('删除文件：', file)


compress('/home/Cspider/data/chance/json', '/home/Cspider/data/chance/json文件/{}.zip'.format(str(now_time)))  # str(yesterday)
deletefile()