from Base.baseAutoHttp import ApiBase
from Base.baseLogger import Logger
from Base.baseData import DataDriver
from PageObject.chandao.p01_http_cd.api_login_page import LoginPage

Login = LoginPage()

class GetCalender(ApiBase):
    # 切换日历页面
    def __init__(self):
        super().__init__('02切换日历页面接口信息.yaml')
    def get_calender_page(self):
        Login.login('demo', '123456')
        res = self.request_base('get_calender')
        return res.text

if __name__ == '__main__':
    g = GetCalender()
    print(g.get_calender_page())