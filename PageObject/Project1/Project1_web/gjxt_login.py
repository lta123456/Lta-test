# encoding:utf-8
from Base.baseLogger import Logger
from Base.baseAutoWeb import WebBase

loger = Logger('gjxt_login.py').getLogger()

class Login(WebBase):
    def __init__(self):
        super().__init__('Web元素定位信息-稿件系统登录.yaml')

    def login(self, user, password):
        '''登录'''
        loger.info('稿件系统登录开始')
        self.get_url('http://127.0.0.1/web/guest/home')
        self.clear('login/用户名输入框')
        self.sendkeys('login/用户名输入框', user)
        self.clear('login/密码输入框')
        self.sendkeys('login/密码输入框', password)
        self.click('login/登录按钮')
        loger.info('稿件系统登录结束')

    def assert_login_ok(self):
        '''断言'''
        title = '测试比对样品 - 稿件管理'
        gjxt_title = self.get_title()
        assert self.is_title(title), loger.error('断言失败：{}'.format(gjxt_title))
        loger.info('【断言】: 登录成功!')

