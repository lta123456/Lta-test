# encoding: utf-8
from Base.baseAutoHttp import ApiBase
from Base.BasePath import BasePath
from PageObject.chandao.p01_http_cd.login import Login
from Base.baseContainer import GlobalManager
import os


class UploadPic(ApiBase):

    def __init__(self):
        super().__init__('群里的人给的项目-上传图片.yaml')

    def upload_pic(self, pic_name):
        pic_path = os.path.join(BasePath().Data_Temp_Dir, pic_name)
        file = {
            'file': (pic_name, open(pic_path, 'rb'), 'image/png')
        }
        res = self.request_base('upload_pic', files=file)
        GlobalManager().set_value('pic_url', res.json()['data']['url'])
        return res.json()

    def add_sort(self, pic_name=''):
        if pic_name:
            self.upload_pic(pic_name)
            pic_name = GlobalManager().get_value('pic_url')
        change_data = {
            'name': '图片',
            'mark': 'wwww',
            'pic_url': pic_name
        }
        res = self.request_base('add_sort', change_data=change_data)
        print(res.json())




if __name__ == '__main__':
    Login().login()
    u = UploadPic()
    u.add_sort('img.png')
