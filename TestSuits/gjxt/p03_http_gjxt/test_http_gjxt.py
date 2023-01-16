# encoding: utf-8
import time

import pytest
from Base.baseData import DataDriver
from PageObject.gjxt.p03_http_gjxt.api_login_page import LoginPage
from PageObject.gjxt.p03_http_gjxt.api_gj_page import ApiGj
from PageObject.gjxt.p03_http_gjxt.api_folder_page import FolderPage


class TestApiCase:
    """接口自动化-稿件管理系统：登录功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01稿件系统-登录功能.yaml'))
    def test_login_case01(self, case_data):
        """稿件管理系统：登录功能"""
        lp = LoginPage()
        res = lp.login(case_data['uasename'], case_data['password'])
        lp.assert_login(res, case_data['title'])


class TestApiCase02:
    """接口自动化-稿件管理系统：稿件管理功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('02稿件系统-新增稿件功能.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_add_gj_case01(self, case_data):
        """稿件管理系统：稿件新增"""
        ap = ApiGj()
        ap.add_gj(case_data['title'], case_data['content'])
        ap.assert_add_gj(case_data['title'])
        ap.assert_add_gj_db(case_data['title'], case_data['content'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('03稿件系统-删除稿件.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_del_gj_case02(self, case_data):
        """稿件管理系统：稿件删除"""
        ap = ApiGj()
        ap.add_gj(case_data['title'], case_data['content'])
        ap.del_gj(case_data['title'])
        ap.assert_del_gj()
        ap.assert_del_gj_db()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('04稿件系统-修改稿件.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_alter_gj_case02(self, case_data):
        """稿件管理系统：稿件修改"""
        ap = ApiGj()
        ap.add_gj(case_data['add_title'], case_data['add_content'])
        ap.alter_gj(case_data['add_title'], case_data['alter_title'], case_data['alter_content'])
        ap.assert_alter_gj(case_data['alter_title'])
        ap.assert_alter_gj_db(case_data['alter_title'], case_data['alter_content'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('05稿件系统-查询稿件.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_select_gj_case03(self, case_data):
        """稿件管理系统：稿件查询"""
        ap = ApiGj()
        ap.add_gj(case_data['title'], case_data['content'])
        res = ap.select_gj(case_data['title'])
        ap.assert_select_gj(res, case_data['title'])
        ap.assert_select_gj_db(case_data['title'])

class TestApiCase03:
    """接口自动化-稿件管理系统：文件管理功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('06稿件系统-文件夹新增和删除.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_add_del_folder_case01(self, case_data):
        """稿件管理系统：文件夹新增和删除"""
        fl = FolderPage()
        fl.add_folder(case_data['name'], case_data['describe'])
        fl.assert_add_folder(case_data['name'])
        fl.assert_add_folder_db(case_data['name'], case_data['describe'])
        fl.del_folder(case_data['name'])
        fl.assert_del_folder(case_data['name'])
        fl.assert_del_folder_db(case_data['name'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('07稿件系统-文件上传.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_upload_file_case02(self, case_data):
        """稿件管理系统：文件上传"""
        fl = FolderPage()
        fl.add_folder(case_data['folder_name'], case_data['folder_desc'])
        res = fl.upload_file(case_data['folder_name'], case_data['file_name'], case_data['file_path'])
        fl.assert_upload_file(res, case_data['file_name'], case_data['file_path'])
        fl.assert_upload_file_db(case_data['file_name'], case_data['file_path'])
        fl.del_folder(case_data['folder_name'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('08稿件系统-文件下载.yaml'))
    @pytest.mark.usefixtures('init_login')
    def test_download_file_case03(self, case_data):
        """稿件管理系统：文件下载"""
        fl = FolderPage()
        fl.add_folder(case_data['folder_name'], case_data['folder_desc'])
        fl.upload_file(case_data['folder_name'], case_data['file_name'], case_data['file_desc'])
        fl.download_file(case_data['file_name'])
        fl.assert_download_file(case_data['file_name'])
        fl.del_folder(case_data['folder_name'])





