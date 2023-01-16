# encoding: utf-8
from Base.baseAutoHttp import ApiBase
from PageObject.chandao.p01_http_cd.api_login_page import LoginPage


class BackLogApi(ApiBase):
    # 待办功能
    def __init__(self):
        super().__init__('03仪表盘页面接口信息.yaml')

    def add_backlog(self, date, priority, name, start_time, end_time):
        """"""
        change_data = {
            'date': date,
            'priority': priority,
            'name': name,
            'start_time': start_time,
            'end_time': end_time
        }
        res = self.request_base('add_backlog', change_data=change_data)
        return res.json()


if __name__ == '__main__':
    lg = LoginPage()
    lg.login('demo', '123456')
    b = BackLogApi()
    print(b.add_backlog('2023-01-01', '3', '1111', '12:00', '13:00'))
