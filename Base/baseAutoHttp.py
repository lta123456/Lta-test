# encoding:utf-8

import requests
import urllib3
from Base.baseData import DataBase
from Base.baseLogger import Logger
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urljoin
import traceback

logger = Logger('baseAutoHttp.py').getLogger()


class ApiBase(DataBase):
    '''接口自动化基类'''

    session = requests.session()

    def __init__(self, YamlName):
        super().__init__(YamlName)
        self.timeout = 10

    def request_base(self, apiName, change_data=None, **kwargs):
        '''通用接口请求'''
        try:
            logger.info('【{} : {} 接口调用开始】'.format(self.YamlName, apiName))
            # 获取接口信息
            yaml_data = self.get_element(change_data)[apiName]
            # 拼接配置文件中url
            yaml_data['url'] = urljoin(self.run_config['TEST_URL'], yaml_data['url'])
            logger.info('【获取【{}】文件【{}】接口请求数据：{}】'.format(self.YamlName, apiName, yaml_data))
            logger.info('接口的请求方式：{}'.format(yaml_data['method']))
            logger.info('接口的请求地址：{}'.format(yaml_data['url']))
            if 'data' in yaml_data.keys():
                logger.info('接口的请求体：{}'.format(yaml_data['data']))
            elif 'json' in yaml_data.keys():
                logger.info('接口的请求体：{}'.format(yaml_data['json']))
            # 消除https请求告警
            # 如果是https请求，还需要在yaml文件中加一行代码
            # verify: False
            # 取消https验证
            urllib3.disable_warnings(InsecureRequestWarning)
            res = ApiBase.session.request(**yaml_data, **kwargs)
            logger.info('接口的响应时间：{}'.format(res.elapsed.total_seconds()))
            logger.debug('接口的响应码：{}'.format(res.status_code))
            logger.debug('接口的响应体：{}'.format(res.text))
            logger.info('【{} : {} 接口调用结束】'.format(self.YamlName, apiName))
            return res
        except Exception as e:
            logger.error('接口请求失败! ：{}'.format(traceback.format_exc()))


if __name__ == '__main__':
    api = ApiBase('接口元素信息-登录.yaml')
    api.request_base('login_api')
