# encoding: utf-8
import os
import traceback

from Base.baseAutoHttp import ApiBase

try:
    a = ApiBase('01登录页面接口信息.yaml')
    a.request_base('login_api')
except Exception as e:
    print(e)


