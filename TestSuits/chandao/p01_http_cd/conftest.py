# encoding: utf-8
import pytest
from PageObject.chandao.p01_http_cd.api_login_page import LoginPage


@pytest.fixture(scope='function')
def init_login():
    lg = LoginPage()
    lg.login('demo', '123456')
    yield
    lg.out_api()


