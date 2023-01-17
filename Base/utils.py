# coding: utf-8
# 专门用来存放工具方法的PY文件
import os
import zipfile
from configparser import RawConfigParser

def read_config_ini(ConfigPath):
    '''读取配置文件.ini'''
    config = RawConfigParser()
    config.read(ConfigPath, encoding='gbk')
    # 返回读取到的内容
    return config

# localPath：测试报告路径
# pname：打包后的路径
def make_zip(localPath, pname):
    '''打包zip'''
    zipf = zipfile.ZipFile(pname, 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(localPath))
    for parent, dirname, filenames in os.walk(localPath):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()
    return pname

def file_all_del(Path):
    '''删除文件夹下，所有的文件'''
    # 遍历文件夹下所有的文件
    for filename in os.listdir(Path):
        os.unlink(os.path.join(Path, filename))

if __name__ == '__main__':
    make_zip(r'D:\学习笔记', r'D:\tt.zip')

