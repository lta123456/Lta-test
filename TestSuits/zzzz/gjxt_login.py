# encoding:utf-8
import re
from Base.baseLogger import Logger
from Base.baseAutoHttp import ApiBase

logger = Logger('gjxt_login.py').getLogger()

class gjxt_login(ApiBase):
    def __init__(self):
        super().__init__('接口元素信息-登录.yaml')

    def login(self, user, psw):
        change_data = {
            'user': user,
            'password': psw
        }
        self.request_base('login_page')
        res = self.request_base('login_api', change_data)
        return res

    def assert_login_ok(self, res, title):
        title_page = re.findall('<title>(.*?)</title>', res)[0]
        assert title_page == title, logger.error('【断言】：当前页面验证失败 {}'.format(title_page))
        logger.info('【断言：当前页面验证成功 {}】'.format(title_page))


if __name__ == '__main__':
    gjxt = gjxt_login()
    res = gjxt.login('test02', '1111')
    gjxt.assert_login_ok(res.text, '测试比对样品 - 稿件管理')


