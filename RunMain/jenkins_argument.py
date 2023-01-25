# encoding: utf-8
import os
import argparse
from configobj import ConfigObj
import configparser

'''读取配置文件.ini'''


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, 'Config', '配置文件.ini')
config = ConfigObj(CONFIG_FILE, encoding='GBK')

# 获取命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--AUTO_TYPE', type=str, default='HTTP')
parser.add_argument('--REPORT_TYPE', type=str, default='ALLURE')
parser.add_argument('--DATA_DRIVER_TYPE', type=str, default='YamlDriver')
parser.add_argument('--TEST_PROJECT', type=str, default='')
parser.add_argument('--TEST_URL', type=str, default='')
args = parser.parse_args()

config['项目运行设置']['AUTO_TYPE'] = args.AUTO_TYPE
#


