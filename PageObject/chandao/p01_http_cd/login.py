# encoding: utf-8
from Base.baseAutoHttp import ApiBase

class Login(ApiBase):

    def __init__(self):
        super().__init__('群里的人给的项目-登录接口.yaml')

    def login(self):
        res = self.request_base('login')
        return res.json()



if __name__ == '__main__':
    Login().login()
