# encoding:utf-8
import logging
import os
import time
from Base.utils import read_config_ini
from Base.BasePath import BasePath as BP

config = read_config_ini(BP.Config_File)['日志打印配置']
LogName = time.strftime('%Y-%m-%d_%H%M', time.localtime()) + '.log'


class Log:
    def __init__(self, name):
        self.name = name
        # 创建日志对象
        self.logger = logging.getLogger(self.name)
        # 设置日志打印总级别
        self.logger.setLevel(config['lever'])
        # 创建文件管理对象
        self.filehandler = logging.FileHandler(os.path.join(BP.Log_Dir, LogName), 'w', encoding='utf-8')
        # 设置打印级别
        self.filehandler.setLevel(config['file_handler_level'])
        # 设置打印格式
        self.formatter = logging.Formatter(config['formatter'])
        self.filehandler.setFormatter(self.formatter)
        # 创建控制台
        self.console = logging.StreamHandler()
        # 设置打印级别
        self.console.setLevel(config['stream_handler_level'])
        # 设置打印格式
        self.console.setFormatter(self.formatter)

        # 添加到日志对象中
        self.logger.addHandler(self.filehandler)
        self.logger.addHandler(self.console)

    def getLogger(self):
        return self.logger


if __name__ == '__main__':
    L = Log('fwe')
    L.getLogger().warning('fea')
