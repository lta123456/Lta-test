# encoding:utf-8
import re

from Base.baseAutoHttp import ApiBase
from Base.baseLogger import Logger

logger = Logger('api_login_page.py').getLogger()

class LoginPage(ApiBase):

    def __init__(self):
        super().__init__('01登录页面接口信息.yaml')

    def login(self, username, password):
        """登录功能"""
        change_data = {
            '_58_login': username,
            '_58_password': password
        }
        self.request_base('home_api')
        res = self.request_base('login_api', change_data=change_data)
        return res.text

    def assert_login(self, res, title):
        """【断言】：登录功能"""
        page_title = re.findall('<title>(.*?)</title>', res)[0]
        assert page_title == title, logger.info('【断言】：登录验证失败!')
        logger.info('【断言】：登录验证成功!')




if __name__ == '__main__':
    lp = LoginPage()
    res = lp.login('test01', '1111')
    print(re.findall('<title>(.*?)</title>', res)[0])
    print(res)

