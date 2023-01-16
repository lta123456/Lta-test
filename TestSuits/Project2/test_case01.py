# encoding:utf-8

import pytest
import os

class TestCase:

    def test_case01(self):
        '''测试用例一'''
        print('-------测试用例一-------')
        assert True

if __name__ == '__main__':
    pytest.main(['-v', '--alluredir={}'.format(r'E:\PyCharm2017\TestFramework_demo\Reports\ALLURE\Result'), r'E:\PyCharm2017\TestFramework_demo\TestSuits\Project2\test_case01.py'])
    os.system('allure generate {} -o {} --clean'.format(r'E:\PyCharm2017\TestFramework_demo\Reports\ALLURE\Result', r'E:\PyCharm2017\TestFramework_demo\Reports\ALLURE\Report'))