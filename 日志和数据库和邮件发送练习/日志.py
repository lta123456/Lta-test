# encoding: utf-8
import os
import logging
import time
log_name = time.strftime('%Y-%m-%d_%H-%M', time.localtime()) + '.log'
log_path = os.path.join(r'E:\PyCharm2017\TestFramework_demo\日志和数据库和邮件发送练习\log', log_name)


class Logger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.INFO)
        self.fileHeaders = logging.FileHandler(log_path, 'w')
        self.fileHeaders.setLevel(level=logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fileHeaders.setFormatter(self.formatter)
        self.console = logging.StreamHandler()
        self.console.setFormatter(self.formatter)
        self.console.setLevel(level=logging.INFO)
        self.logger.addHandler(self.fileHeaders)
        self.logger.addHandler(self.console)

    def getlogger(self):
        return self.logger

if __name__ == '__main__':
    l = Logger('eee').getlogger()
    l.info('ff')
    l.debug('dd')
