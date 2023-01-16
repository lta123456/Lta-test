import os

import allure
import pytest
from Base.baseData import DataDriver
from PageObject.chandao.p01_http_cd.api_login_page import LoginPage
from PageObject.chandao.p01_http_cd.api_Dashboard_page import BackLogApi
from Base.baseLogger import Logger
import time
log = Logger(name='test_http_cd').getLogger()

@allure.epic('禅道系统')
@pytest.mark.login
@allure.feature('登录模块')
class TestLogin:

    @pytest.mark.login_login
    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01禅道系统-登录功能.yaml'))
    @allure.story('登录接口')
    def test_login(self, case_data):
        lp = LoginPage()
        res = lp.login(case_data['username'], case_data['password'])
        lp.out_api()
        lp.assert_login(res, case_data['assert_data'])
        log.info('成功')


@allure.epic('禅道系统')
@allure.feature('仪表盘模块')
@pytest.mark.DashboardPage
class TestDashboardPage:

    @pytest.mark.add_backlog
    @pytest.mark.parametrize('case_data, title', DataDriver().get_case_data('02禅道系统-待办功能.yaml'))
    @pytest.mark.usefixtures('init_login')
    @allure.story('添加待办接口')
    @allure.title('{title}')
    def test_add_backlog(self, case_data, title):
        b = BackLogApi()
        res = b.add_backlog(case_data['date'], case_data['priorityL'], case_data['name'], case_data['start_time'],
                            case_data['end_time'])


@allure.epic('禅道系统')
@allure.feature('假代码')
class TestFF:

    @pytest.mark.usefixtures('init_login')
    def test_aaa(self):
        print('无关1')

    def test_bbb(self):
        print('无关2')


if __name__ == '__main__':
    pytest.main(['test_http_cd.py', '-s', '-m', 'add_backlog', '--alluredir', '../../Reports/ALLURE/Result'])
    os.system('allure generate ../../Reports/ALLURE/Result -o ../../Reports/ALLURE/Report')
    # os.system('allure server ../../Reports/ALLURE/Result')
