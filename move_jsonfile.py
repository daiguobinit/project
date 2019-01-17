import os, shutil
import zipfile, tarfile
import time
from datetime import datetime
from datetime import timedelta

yesterday = datetime.now() - timedelta(days=1)  # 昨天时间
yesterday = str(yesterday).split(' ')[0]
date_time = yesterday.replace('-', '_')


path = 'E:/chance'

for files in os.walk(path):
    list_files = files[-1]
    for file in list(list_files):
        if '2019_01_03' in file and 'json' not in files[0]:
            # print(file)
            ph = files[0]
            ph = ph.replace('\\', '/')
            path = ph + '/' + file
            print('移动文件中.....')
            shutil.copy(path, 'E:/chance/json')
    print(files)

def compress(get_files_path, set_files_path):
    print('正在打包压缩文件中......')
    f = zipfile.ZipFile(set_files_path , 'w', zipfile.ZIP_DEFLATED )
    for dirpath, dirnames, filenames in os.walk(get_files_path):
        fpath = dirpath.replace(get_files_path,'') #注意2
        fpath = fpath and fpath + os.sep or ''     #注意2
        for filename in filenames:
            f.write(os.path.join(dirpath,filename), fpath+filename)
    f.close()
    print("文件打包压缩成功")
#



def deletefile():
    """删除小于minSize的文件（单位：K）"""
    files = os.listdir('E:/chance/json')  #列出目录下的文件
    for file in files:
        print(file)
        os.remove('E:/chance/json/' + file)    #删除文件
        print('删除文件：', file)
    # return


compress('E:/chance/json', 'E:/chance/json文件/{}.zip'.format(str(yesterday)))
deletefile()