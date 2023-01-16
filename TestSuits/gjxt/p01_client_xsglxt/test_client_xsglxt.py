# encoding:utf-8

import pytest
from Base.baseData import DataDriver
from PageObject.p01_client_xsglxt.client_start_stop import ClientPage
from PageObject.p01_client_xsglxt.client_teacher_page import TeacherPage
from PageObject.p01_client_xsglxt.client_student_page import StudentPage


class TestClientCase1:
    """客户端自动化-学生管理系统：登录功能模块"""

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01学生管理系统登录.yaml'))
    @pytest.mark.usefixtures('init_client')
    def test_login_case01(self, case_data):
        """客户端自动化用例：用户登录测试"""
        cp = ClientPage()
        cp.client_login(case_data['username'], case_data['password'])
        cp.assert_login_ok(case_data['flag'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('02学生管理系统注册.yaml'))
    @pytest.mark.usefixtures('init_client')
    def test_register_case02(self, case_data):
        """客户端自动化用例：学生注册测试"""
        cp = ClientPage()
        cp.client_student_register(case_data['name'], case_data['age'], case_data['student_number'], case_data['password'])
        cp.assert_register_ok(case_data['student_number'])


class TestClientCase2:
    """客户端自动化-学生管理系统：老师功能模块"""

    @pytest.mark.usefixtures('init_client', 'teacher_login')
    def test_view_transcripts_case01(self):
        """客户端自动化用例：查看学生成绩单"""
        tp = TeacherPage()
        # 查看学生成绩单
        tp.client_teacher_view_transcripts()
        # 断言
        tp.assert_client_teacher_view_transcripts()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('03学生管理系统成绩.yaml'))
    @pytest.mark.usefixtures('init_client', 'teacher_login')
    def test_alter_grade_case02(self, case_data):
        """客户端自动化用例：修改学生成绩"""
        tp = TeacherPage()
        # 修改学生成绩
        tp.client_teacher_alter_grade(case_data['student_number'], case_data['ptysics_grade'])
        tp.assert_client_teacher_alter_grade(case_data['student_number'], case_data['ptysics_grade'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('04学生管理系统导出成绩单.yaml'))
    @pytest.mark.usefixtures('init_client', 'teacher_login')
    def test_export_score_case03(self, case_data):
        """客户端自动化用例: 导出学生成绩单"""
        tp = TeacherPage()
        tp.client_teacher_export_score(case_data['course'], case_data['sort'])
        tp.assert_client_teacher_export_score(case_data['file_path'])

class TestClientCase3:
    """客户端自动化-学生管理系统：学生功能模块"""

    @pytest.mark.usefixtures('init_client', 'student_login')
    def test_student_view_score_case04(self):
        """客户端自动化用例：学生查看成绩单"""
        sp = StudentPage()
        sp.client_student_view_score()
        sp.assert_student_view_score()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('05学生管理系统修改密码.yaml'))
    @pytest.mark.usefixtures('init_client')
    def test_student_alter_password(self, case_data):
        """客户端自动化用例：学生修改个人密码"""
        sp = StudentPage()
        sp.client_login(case_data['student_number'], case_data['login_password'])
        sp.client_student_alter_password(case_data['new_password'], case_data['repeat_password'])
        sp.assert_student_alter_password(case_data['student_number'], case_data['assert_database_data'], case_data['login_password'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('06学生管理系统学生导出成绩单.yaml'))
    @pytest.mark.usefixtures('init_client')
    def test_student_export_score(self, case_data):
        """客户端自动化用例：学生导出成绩单"""
        sp = StudentPage()
        sp.client_login(case_data['student_number'], case_data['password'])
        sp.client_student_export_score()
        sp.assert_student_export_score(case_data['file_path'], case_data['student_number'])





