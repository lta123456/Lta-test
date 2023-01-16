# encoding:utf-8
import os
import re
import time

from Base.BasePath import BasePath as BP
from Base.baseLogger import Logger
from Base.baseAutoHttp import ApiBase
from ExtTools.dbbase import MysqlHelp
from PageObject.gjxt.p03_http_gjxt.api_login_page import LoginPage

logger = Logger('api_folder_page.py').getLogger()

class FolderPage(ApiBase):

    def __init__(self):
        super().__init__('03文件管理接口信息.yaml')

    def add_folder(self, name, describe):
        """新增文件夹"""
        change_data = {
            '_20_name':  name,
            '_20_description': describe
        }
        res = self.request_base('add_folder', change_data=change_data)
        return res.text

    def select_folder(self):
        """文件夹查询"""
        res = self.request_base('select_folder')
        re_info = re.findall('2Fdocument_library%2Fview&_20_folderId=(.*?)">(.*?)</a>', res.text)
        return re_info

    def assert_add_folder(self, name):
        """【断言】文件夹新增页面断言"""
        re_info = self.select_folder()[0]
        assert name in re_info, logger.error('【断言】：文件夹新增页面断言失败!')
        logger.info('【断言】：文件夹新增页面断言成功!')

    def assert_add_folder_db(self, name, describe):
        """【断言】文件夹新增数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select name, description from dlfolder order by createDate desc')
        assert res[0]['name'] == name, logger.error('【断言】：文件夹新增数据库断言失败! 名称错误')
        assert res[0]['description'] == describe, logger.error('【断言】：文件夹新增数据库断言失败! 描述错误')
        logger.info('【断言】：文件夹新增数据库断言成功!')

    def del_folder(self, name):
        """删除文件夹"""
        # 将查询接口返回的[('文件夹id', ('文件夹名称')]转换为
        # {'名称': '文件夹id'}格式
        dict = {}
        a = self.select_folder()
        for i in range(len(a)):
            dict[a[i][1]] = a[i][0]
        try:
            folder_id = dict[name]
        except KeyError as e:
            print('文件夹不存在，请检查文件夹名称：{}'.format(e))
        change_data = {
            '_20_folderId': folder_id
        }
        self.request_base('del_folder', change_data=change_data)

    def assert_del_folder(self, name):
        """【断言】：删除文件夹"""
        res = self.select_folder()
        assert name not in str(res), logger.error('【断言】：文件夹删除页面断言失败!')
        logger.info('【断言】：文件夹删除页面断言成功!')

    def assert_del_folder_db(self, name):
        """【断言】：删除文件夹数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select count(*) as "总数" from dlfolder where name = "{}"'.format(name))[0]
        assert res['总数'] == 0, logger.error('【断言】：文件夹删除数据库断言失败!')
        logger.info('【断言】：文件夹删除数据库断言成功!')

    def upload_file(self, folder_name, file_name, file_desc):
        """上传文件"""
        folder = self.select_folder()
        name_id = {}
        for r in range(len(folder)):
            name_id[folder[r][1]] = folder[r][0]
        try:
            change_data = {
                'folder_id': name_id[folder_name],
                '_20_folderId': name_id[folder_name],
                '_20_title': file_name,
                '_20_description': file_desc
            }
        except KeyError as e:
            print('文件夹名称错误!')
        file_path = os.path.join(BP.Data_Temp_Dir, 'upload_file.txt')
        files = {
            '_20_file': ('file_name.txt', open(file_path, 'r'), 'text/plain')
        }
        return self.request_base('upload_file', change_data=change_data, files=files).text

    def assert_upload_file(self, res, name, filedesc):
        """【断言】：上传文件页面断言"""
        filename = name
        rename_info = re.findall('<input  id="_20_title" name="_20_title" style="width: 350px; " type="text" value="(.*?)"', res)[0]
        redesc_info = re.findall('onKeyPress="Liferay.Util.checkMaxLength\(this, 4000\);">(.*?)</textarea>', res)[0]
        assert filename == rename_info, logger.error('【断言】：文件上传页面断言错误! 名称错误!')
        assert filedesc == redesc_info, logger.error('【断言】：文件上传页面断言错误! 描述错误')
        logger.info('【断言】：文件上传页面断言成功!')

    def assert_upload_file_db(self, filename, filedesc):
        """【断言】：上传文件页面数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select * from dlfileentry order by createDate desc')[0]
        assert filename.split('.')[0] == res['title'], logger.error('【断言】：文件上传数据库断言错误! 名称错误!')
        assert filedesc == res['description'], logger.error('【断言】：文件上传数据库断言错误! 描述错误!')
        logger.info('【断言】：文件上传数据库断言成功!')

        db.mysql_db_operate('delete from dlfileentry where title = "{}"'.format(filename))
        logger.info('上传文件数据清除完成')

    def select_file(self, filename=''):
        """查询文件"""
        change_data = {
            '_20_keywords': filename
        }
        return self.request_base('select_file', change_data=change_data).text

    def download_file(self, rename):
        """下载文件"""
        res = self.select_file(rename.split('.')[0])
        re_info = re.findall('<a href="http://127.0.0.1/group/10779/upload\?'
                                     'p_p_id=20&p_p_lifecycle=1&p_p_state=exclusive&'
                                     'p_p_mode=view&_20_struts_action=%2Fdocument_library'
                                     '%2Fget_file&_20_folderId=(.*?)&_20_name=(.*?)">(.*?)</a>', res)
        # 将文件的id，名称属性转为集合
        # 将[(文件夹ID, 数据库文件名称, 文件名称)]
        # 转化为{文件名称: [文件夹ID, 数据库文件名称]}格式 方便读取
        dict = {}
        for r in range(len(re_info)):
            list = []
            for i in range(2):
                list.append(re_info[r][i])
                dict[re_info[r][2]] = list

        change_data = {
            'folderId': dict[rename.split('.')[0]][0],
            'name': dict[rename.split('.')[0]][1]
        }
        res = self.request_base('download_file', change_data=change_data)
        filename = os.path.join(BP.Data_Temp_Dir, rename.split('.')[0]+'.txt')
        # 通过二级制方式写入
        with open(filename, 'wb') as f:
            # content获取它的二进制内容
            f.write(res.content)
        logger.info('文档下载接口调用结束')

    def assert_download_file(self, filename):
        """【断言】：下载文件"""
        filepath = os.path.join(BP.Data_Temp_Dir, filename.split('.')[0]+'.txt')
        assert os.path.exists(filepath), logger.error('【断言】：下载文件失败! 文档不存在!')
        logger.info('【断言】：下载文件成功!')
        os.remove(filepath)






if __name__ == '__main__':
    lg = LoginPage()
    fl = FolderPage()
    lg.login('test01', '1111')
    fl.add_folder('下载文件测试文件夹名称', '下载文件测试文件夹描述')
    fl.upload_file('下载文件测试文件夹名称', '下载文件测试文件名称.txt', '下载文件测试文件描述')
    fl.download_file('下载文件测试文件名称')
    fl.del_folder('下载文件测试文件夹名称')
    fl.assert_download_file('下载文件测试文件名称')

