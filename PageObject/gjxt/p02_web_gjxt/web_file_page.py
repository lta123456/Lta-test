# encoding:utf-8
import os
import time
import pyautogui
from Base.BasePath import BasePath as BP
from Base.baseAutoWeb import WebBase
from Base.baseLogger import Logger
from ExtTools.dbbase import MysqlHelp

logger = Logger('web_file_page.py').getLogger()

class FilePage(WebBase):
    """文件上传与下载功能测试"""

    def __init__(self):
        super().__init__('03文件上传下载元素信息.yaml')

    def add_folder(self, name, content):
        """新增文件夹"""
        logger.info('-----------------------------------------文件夹新增开始-----------------------------------------')
        time.sleep(1)
        self.click('add_folder/file_upload_download_btn')
        self.click('add_folder/add_folder_btn')
        self.sendkeys('add_folder/name_input', name)
        self.sendkeys('add_folder/content_input', content)
        self.click('add_folder/commit_btn')
        logger.info('-----------------------------------------文件夹新增结束-----------------------------------------')

    def assert_add_folder(self, name):
        """【断言】：新增文件夹页面断言"""
        assert self.get_text('add_folder/msg_sucess') == '您的请求执行成功。', logger.error('【断言】：新增文件夹失败，提示信息错误!')
        logger.info('【断言】：新增文件夹成功!')
        assert self.get_text('add_folder/firer_folder_title') == name, logger.error('【断言】：新增文件夹失败，名称错误!')
        logger.info('【断言】：新增文件夹成功!')

    def assert_add_folder_db(self, name, content):
        """【断言】：新增文件夹数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('SELECT * FROM dlfolder order by createDate desc')
        assert res[0]['name'] == name, logger.error('【断言】：数据库断言失败，文件名称与数据库中的名称不一致!')
        assert res[0]['description'] == content, logger.error('【断言】：数据库断言失败，文件描述与数据库中的描述不一致!')
        logger.info('【断言】：数据库断言成功!')

    def del_folder(self):
        """删除文件夹"""
        logger.info('-----------------------------------------删除文件夹开始-----------------------------------------')
        self.click('del_folder/file_upload_download_btn')
        self.click('del_folder/firer_del_btn')
        self.is_alert().accept()
        logger.info('-----------------------------------------删除文件夹结束-----------------------------------------')

    def assert_del_folder(self):
        """【断言】：文件夹删除页面"""
        assert self.get_text('del_folder/msg_sucess') == '您的请求执行成功。', logger.error('【断言】：删除文件夹失败，提示信息错误!')
        logger.info('【断言】：删除文件夹成功!')

    def assert_del_folder_db(self, name):
        """【断言】：文件夹删除数据库"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select count(*) as "总数" from dlfolder where name = "{}"'.format(name))
        assert res[0]["总数"] == 0, logger.error('【断言】：删除文件夹失败，数据库中依然存在!')
        logger.info('【断言】：数据库断言，删除文件夹成功!')

    def upload_file(self, filename, filespec):
        """上传文件操作"""
        logger.info('-'*40+'上传文件开始'+'-'*40)
        # 点击文件上传下载按钮
        self.click('add_file/file_upload_download_btn')
        # 点击第一个文件夹的标题
        self.click('add_file/firer_folder_title')
        # 点击上传文件按钮
        self.click('add_file/add_file_btn')
        # 切换iframe
        self.switch_iframe('add_file/upload_file_iframe')
        # 选择文件
        file_path = os.path.join(BP.Data_Temp_Dir, 'upload_file.txt')
        self.sendkeys('add_file/select_file_btn', file_path)
        # 输入文件名称
        self.sendkeys('add_file/file_title', filename)
        # 输入文件说明
        self.sendkeys('add_file/filespec', filespec)
        # 点击上传文件按钮
        self.click('add_file/upload_file_btn')
        # 切出iframe
        self.switch_iframe_out()
        logger.info('-'*40+'上传文件结束'+'-'*40)

    def assert_upload_file_page(self, filename, filespec):
        """【断言】：上传文件操作页面断言"""
        name_spec = self.get_text('add_file/firer_file_name_spec')
        name = name_spec.split()[0]
        spec = name_spec.split()[1]
        assert name == filename+'.txt', logger.error('【断言】：上传文件失败，文件名称错误!')
        assert spec == filespec, logger.error('【断言】：上传文件失败，文件说明错误!')
        logger.info('【断言】：上传文件页面断言成功!')

    def assert_upload_file_db(self, title, spec):
        """【断言】：上传文件操作数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select * from dlfileentry order by createDate desc')
        assert res[0]['title'] == title, logger.error('【断言】：上传文件失败，数据库中文件名称错误!')
        assert res[0]['description'] == spec, logger.error('【断言】：上传文件失败，数据库中文件描述错误!')
        logger.info('【断言】：上传文件数据库断言成功!')

    def download_file(self):
        """文件下载"""
        logger.info('-' * 40 + '文件下载开始' + '-' * 40)
        self.click('download_file/file_upload_download_btn')
        self.click('download_file/firer_folder_title')
        time.sleep(1)
        download_url = self.get_attribute('download_file/firer_file_name', 'href')
        self.get_url(download_url)
        time.sleep(1)
        pyautogui.hotkey('alt', 's')
        logger.info('-' * 40 + '文件下载结束' + '-' * 40)

    def assert_download_file(self, filename):
        """【断言】：文件下载"""
        time.sleep(1)
        path = r'E:\稿件管理项目\稿件系统下载文件测试文件夹'
        filepath = os.path.join(path, filename)
        assert os.path.exists(filepath), logger.error('【断言】：文件下载失败，文件夹 {} 中不存在!'.format(path))
        logger.info('【断言】：文件下载成功!')

        os.remove(filepath)



if __name__ == '__main__':
    from selenium import webdriver
    from Base.baseContainer import GlobalManager
    from PageObject.p02_web_gjxt.web_login_page import LoginPage
    driver = webdriver.Ie(r'E:\PyCharm2017\TestFramework_demo\Driver\IEDriverServer.exe')
    gm = GlobalManager()
    gm.set_value('driver', driver)
    lg = LoginPage()

    fl = FilePage()
    lg.login('test01', '1111')
    fl.add_folder('aaa', '测试彩色')
    fl.upload_file('文件名称', '文件描述')
    fl.download_file()
    fl.assert_download_file('文件名称.txt')
    fl.del_folder()

