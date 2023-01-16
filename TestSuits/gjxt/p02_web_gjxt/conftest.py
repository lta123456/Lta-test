# encoding:utf-8
import pytest
from PageObject.p02_web_gjxt.web_login_page import LoginPage


@pytest.fixture(scope='function')
def init_login():
    """稿件系统登录"""
    lp = LoginPage()
    lp.login('test01', '1111')


