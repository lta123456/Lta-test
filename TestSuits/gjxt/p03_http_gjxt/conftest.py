# encoding: utf-8
import pytest
from PageObject.gjxt.p03_http_gjxt.api_login_page import LoginPage
from PageObject.gjxt.p03_http_gjxt.api_gj_page import ApiGj


@pytest.fixture(scope='function')
def init_login():
    lp = LoginPage()
    lp.login('test01', '1111')


@pytest.fixture(scope='function')
def gj_add_del(request):
    """稿件新增删除"""
    # pytest中的request参数，通过这个参数拿到测试用例传来的值
    case_data = request.param
    ap = ApiGj()
    ap.fff(case_data)
    yield
    print(case_data)


if __name__ == '__main__':
    init_login()