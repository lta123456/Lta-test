# encoding:utf-8
from Base.baseAutoWeb import WebBase
from Base.baseLogger import Logger
from Base.utils import read_config_ini
from Base.BasePath import BasePath as BP

logger = Logger('web_login_page.py').getLogger()

config = read_config_ini(BP.Config_File)

class LoginPage(WebBase):
    """登录功能"""

    def __init__(self):
        super().__init__('01登录页面元素信息.yaml')

    def login(self, username, password):
        """稿件系统登录"""
        logger.info('稿件系统登录开始')
        self.username = username
        self.get_url(config['项目运行设置']['TEST_URL'])
        logger.info('打开测试网址：{}'.format(config['项目运行设置']['TEST_URL']))
        # 1、输入用户名
        self.clear('login/username_input')
        self.sendkeys('login/username_input', username)
        # 2、输入密码
        self.clear('login/password_input')
        self.sendkeys('login/password_input', password)
        # 3、点击登录按钮
        self.click('login/login_btn')
        logger.info('稿件系统登录结束')

    def assert_login(self, flag):
        title = self.get_title()
        if flag == '1':
            assert title == '测试比对样品 - 稿件管理', logger.error('【断言】：登录失败!页面title不符合预期：{}'.format(title))
            logger.info('【断言】：登录成功!页面title符合预期：{}'.format(title))
            text = self.get_text('login/assert_login_welcome')
            assert text == 'Welcome {}!'.format(self.username), logger.error('【断言】：登录失败!首页欢迎语显示错误：{}'.format(text))
            logger.info('【断言】：登录成功!首页欢迎语符合预期：{}'.format(text))
        elif flag == '2':
            assert title == '测试比对样品 - 登录', logger.error('【断言】：断言失败!页面title不符合预期：{}'.format(title))
            logger.info('【断言】：断言成功!页面title符合预期：{}'.format(title))
            text = self.get_text('login/login_error')
            assert text == '请输入有效的登入。', logger.error('【断言】：断言失败!页面提示信息不符合预期：{}'.format(text))
            logger.info('【断言】：登录成功!页面提示信息符合预期：{}'.format(text))
        elif flag == '3':
            assert title == '测试比对样品 - 登录', logger.error('【断言】：断言失败!页面title不符合预期：{}'.format(title))
            logger.info('【断言】：断言成功!页面title符合预期：{}'.format(title))
            text = self.get_text('login/login_error')
            assert text == '登入认证失败。请再试试。', logger.error('【断言】：断言失败!页面提示信息不符合预期：{}'.format(text))
            logger.info('【断言】：登录成功!页面提示信息符合预期：{}'.format(text))


if __name__ == '__main__':
    from selenium import webdriver
    from Base.baseContainer import GlobalManager
    gm = GlobalManager()
    driver = webdriver.Ie(r'E:\PyCharm2017\TestFramework_demo\Driver\IEDriverServer.exe')
    gm.set_value('driver', driver)
    lo = LoginPage()
    lo.login('test01', '4151')
    lo.assert_login('3')


