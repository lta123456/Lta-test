# encoding:utf-8

import os
import time

from Base.baseExcel import Excel
from PageObject.p01_client_xsglxt.client_start_stop import ClientPage

from Base.baseAutoClient import GuiBase
from Base.baseLogger import Logger
from ExtTools.dbbase import Sqlite3Tools

logger = Logger('client_student_page.py').getLogger()

class StudentPage(ClientPage):
    """学生功能页面"""

    def __init__(self):
        super().__init__()

    def client_student_view_score(self):
        """学生查看成绩单"""
        self.click_pic('view_score.png')

    def assert_student_view_score(self):
        """【断言】：学生查看成绩单"""
        assert self.is_exist('assert_view_score_ok.png'), logger.error('【断言】：学生查看学生成绩单失败!')
        logger.info('【断言】：学生查看学生成绩单成功!')

    def client_student_alter_password(self, password, repeat_password):
        """学生修改个人密码"""
        self.click_pic('student_alter_password.png')
        self.rel_click_picture('new_password_input.png', x=50)
        self.type(password)
        self.rel_click_picture('repeat_password_input.png', x=50)
        self.type(repeat_password)
        self.click_pic('commit_alter_btn.png')

    def assert_student_alter_password(self, student_number, new_password, old_password):
        """【断言】：学生修改个人密码"""
        assert self.is_exist('assert_alter_password_ok.png'), logger.error('【断言】：学生修改个人密码错误!')
        logger.info('【断言】：学生修改个人密码成功!')

        # 获取数据库
        sq = Sqlite3Tools(self.db_path)
        res = sq.sqlite3_db_select('select * from student_info where student_number = {}'.format(student_number))
        assert new_password == res[0]['student_passworld'], logger.error('【断言】：学生修改个人密码数据库验证错误!')
        logger.info('【断言】：学生修改个人密码数据库验证成功!')
        sq.sqlite3_db_operate('UPDATE student_info SET student_passworld = {} WHERE student_number = {}'.format(old_password, student_number))
        logger.info('学生密码重置成功')

    def client_student_export_score(self):
        """学生导出成绩单"""
        self.click_pic('export_score_btn.png')

    def assert_student_export_score(self, file_path, student_number):
        """【断言】：学生导出成绩单"""
        assert self.is_exist('export_score_ok.png'), logger.error('【断言】：学生导出成绩单失败!')
        logger.info('【断言】：学生导出成绩单成功!')
        assert os.path.exists(file_path), logger.error('【断言】：文件不存在，或者文件路径错误')
        logger.info('【断言】：文件存在!')

        sq = Sqlite3Tools(self.db_path)
        excel_data = Excel(file_path).dict_data()
        res = sq.sqlite3_db_select('select * from student_achievement where student_number = {}'.format(student_number))

        key = [key for key in excel_data[0].keys()]
        value = [value for value in excel_data[0].values()]
        for c in range(len(excel_data)):
            for i in range(len(value)):
                if value[i] == '':
                    value[i] = None

            j = {}
            for i in range(0, len(key)):
                j[key[i]] = value[i]

            excel_data[c] = j
        assert res == excel_data, logger.error('【断言】：导出文件数据与数据库中数据不匹配!')
        logger.info('【断言】：导出文件数据与数据库中数据匹配!')

        # 删除文件
        os.remove(file_path)





if __name__ == '__main__':
    c = ClientPage()
    c.start_client()
    c.client_login('888888888881', '123')
    s = StudentPage()
    s.client_student_export_score()
    s.assert_student_export_score(r'E:\学习笔记\客户端自动化软件\03项目资料\学生管理系统\学生管理系统\客户端程序\888888888881_student_achievement.xls', '888888888881')







