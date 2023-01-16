# encoding:utf-8
import pytest
from Base.baseData import DataDriver
from PageObject.Project1.Project1_web.gjxt_login import Login


class Test_Case01:

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('稿件系统登录信息.yaml'))
    def test_login_case01(self, driver, case_data):
        '''WEB自动化用例-用户登录测试'''
        lg = Login()
        lg.login(case_data['user'], case_data['password'])
        lg.assert_login_ok()
