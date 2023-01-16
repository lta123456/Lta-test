# encoding:utf-8
import pytest
from PageObject.gjxt.p02_web_gjxt.web_login_page import LoginPage
from PageObject.gjxt.p02_web_gjxt.web_article_page import GJPage
from PageObject.gjxt.p02_web_gjxt.web_file_page import FilePage
from Base.baseData import DataDriver


class TestCase01:
    """WEB自动化-稿件管理系统：登录功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01稿件系统登录功能.yaml'))
    def test_login_case01(self, driver, case_data):
        """WEB自动化用例：用户登录测试"""
        lp = LoginPage()
        lp.login(case_data['username'], case_data['password'])
        lp.assert_login(case_data['flag'])

class TestCase02:
    """WEB自动化-稿件管理系统：稿件管理功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('02稿件系统新增功能.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_gj_add_case01(self, case_data):
        """稿件管理系统：新增稿件"""
        gj = GJPage()
        gj.add_article(case_data['title'], case_data['content'])
        gj.assert_add_article(case_data['title'], case_data['content'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('03稿件系统删除功能.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_gj_del_case02(self, case_data):
        """稿件管理系统：删除稿件"""
        gj = GJPage()
        gj.add_article(case_data['title'])
        gj.del_gj(case_data['title'])
        gj.assert_del_gj(case_data['title'])
        gj.assert_db_del_gj(case_data['title'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('04稿件系统修改功能.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_gj_alter_case03(self, case_data):
        """稿件管理系统：修改稿件"""
        gj = GJPage()
        gj.add_article(case_data['old_title'], case_data['old_content'])
        gj.alter_gj(case_data['new_title'], case_data['new_content'])
        gj.assert_alter_gj(case_data['new_title'])
        gj.assert_alter_db_gj(case_data['new_title'], case_data['new_content'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('05稿件系统查询功能.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_gj_select_case04(self, case_data):
        """稿件管理系统：查询稿件"""
        gj = GJPage()
        gj.add_article(case_data['title'], case_data['content'])
        gj.select_gj(case_data['title'])
        gj.assert_select_gj(case_data['title'])
        gj.assert_select_gj_db(case_data['title'])


class TestCase03:
    """WEB自动化-稿件管理系统：文件上传下载功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('06稿件系统文件夹新增与删除.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_add_del_folder_case01(self, case_data):
        """稿件管理系统：新增稿件"""
        fp = FilePage()
        fp.add_folder(case_data['name'], case_data['desc'])
        fp.assert_add_folder(case_data['name'])
        fp.assert_add_folder_db(case_data['name'], case_data['desc'])
        # 删除文件夹
        fp.del_folder()
        fp.assert_del_folder()
        fp.assert_del_folder_db(case_data['name'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('07稿件系统上传文件功能.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_upload_file_case02(self, case_data):
        """稿件管理系统：上传文件"""
        fp = FilePage()
        fp.add_folder(case_data['folder_name'], case_data['folder_content'])
        fp.upload_file(case_data['file_name'], case_data['file_spec'])
        fp.assert_upload_file_page(case_data['file_name'], case_data['file_spec'])
        fp.assert_upload_file_db(case_data['file_name'], case_data['file_spec'])
        fp.del_folder()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('08稿件系统下载文件.yaml'))
    @pytest.mark.usefixtures('driver', 'init_login')
    def test_download_file_case03(self, case_data):
        """稿件管理系统：下载文件"""
        fp = FilePage()
        fp.add_folder(case_data['folder_name'], case_data['folder_content'])
        fp.upload_file(case_data['file_name'], case_data['file_spec'])
        fp.download_file()
        fp.assert_download_file(case_data['file_name'])
        fp.del_folder()



