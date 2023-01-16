# encoding:utf-8
import os
import logging
import sys
import time
from Base.BasePath import BasePath as BP
from Base.utils import read_config_ini

config = read_config_ini(BP.Config_File)['日志打印配置']
rq = time.strftime('%Y-%m-%d_%H%M', time.localtime()) + '.log'

class Logger:
    def __init__(self, name='few'):
        self.name = name
        # 1.创建日志对象
        self.logger = logging.getLogger(self.name)
        # 设置日志总级别
        self.logger.setLevel(config['lever'])

        # 2.创建文件管理器
        # 定义一个文件处理器
        self.rHandler = logging.FileHandler(os.path.join(BP.Log_Dir, rq), mode='a', encoding='utf-8')
        # 设置文件处理器的级别
        self.rHandler.setLevel(config['file_handler_level'])
        # 设置文件打印格式
        self.formatter = logging.Formatter(config['formatter'])
        # 设置日志打印格式
        self.rHandler.setFormatter(self.formatter)

        # 3.设置控制台输出
        # 创建控制台管理器
        if config['console'] == "yes":
            self.console = logging.StreamHandler()
            # 设置控制台日志的级别
            self.console.setLevel(config['stream_handler_level'])
            # 设置日志打印格式
            self.console.setFormatter(self.formatter)
            # 将控制器添加到日志对象
            self.logger.addHandler(self.console)

        # 4.将文件处理器添加到日志对象
        self.logger.addHandler(self.rHandler)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'obj'):
            cls.obj = object.__new__(cls)
        return cls.obj

    def getLogger(self):
        return self.logger

if __name__ == '__main__':
    a = Logger()
    b = Logger()
    print(id(a))
    print(id(b))

