# encoding: utf-8
import copy
from ExtTools.md5DES import get_md5_psw
from Base.baseAutoHttp import ApiBase
from Base.baseLogger import Logger
import time
import hashlib
from Base.baseContainer import GlobalManager


def show_time(func):  # 装饰函数
    def inner(*args):
        begin_time = time.time()
        res = func(*args)
        end_time = time.time()
        run_tile = end_time - begin_time
        print(f'测试用例运行时间：{run_tile}s')
        return res
    return inner

logger = Logger('api_login_page.py').getLogger()

class LoginPage(ApiBase):
    def __init__(self):
        super().__init__('01登录页面接口信息.yaml')
    @show_time
    def login(self, username, password):
        """
        禅道登录功能
        :param username: 用户名
        :param password: 密码
        :return: 响应信息
        """
        res = self.get_refreshRandom()
        password1 = copy.copy(password)
        f = get_md5_psw(password1)+res
        psw = get_md5_psw(f)
        change_data = {
            'username': username,
            'password': psw,
            'verifyRand': res
        }

        res = self.request_base('login_api', change_data=change_data)
        res.encoding = 'utf-8'
        return res.json()

    def assert_login(self, res, assert_info):
        """
        断言登录是否成功
        :param res: 接口返回的数据
        :param assert_info: 预期结果
        :return:
        """
        assert res == assert_info, logger.info(f'断言错误，接口返回的数据：{res}, 请求的数据：{assert_info}')
        logger.info(f'断言成功, 断言信息：{assert_info}')

    def out_api(self):
        """"""
        res = self.request_base('out_api')
        res.encoding = 'utf-8'

    def get_refreshRandom(self):
        res = self.request_base('get_refreshRandom').text
        return res





if __name__ == '__main__':
    # username = DataDriver().get_case_data('01禅道系统-登录功能.yaml')[0]['username']
    # password = DataDriver().get_case_data('01禅道系统-登录功能.yaml')[0]['password']
    # print(LoginPage().login(username=username, password=password))
    # LoginPage().out_api()
    # username1 = DataDriver().get_case_data('01禅道系统-登录功能.yaml')[1]['username']
    # password1 = DataDriver().get_case_data('01禅道系统-登录功能.yaml')[1]['password']
    # print(LoginPage().login(username=username1, password=password1))
    print(LoginPage().login('demo', '123456'))