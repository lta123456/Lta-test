# encoding:utf-8

import os
import time
from ExtTools.dbbase import Sqlite3Tools
from Base.baseAutoClient import GuiBase
from Base.baseLogger import Logger

logger = Logger('client_start_stop.py').getLogger()

class ClientPage(GuiBase):

    def __init__(self):
        super().__init__()
        # 应用文件夹的路径
        self.clientPath = r'E:\学习笔记\客户端自动化软件\03项目资料\学生管理系统\学生管理系统\客户端程序'
        # 应用的路径
        self.exe_path = os.path.join(self.clientPath, 'main.exe')
        # 盘符
        self.driver = self.exe_path.split('\\')
        # 数据库的路径
        self.db_path = os.path.join(self.clientPath, 'student.db')

    def start_client(self):
        """启动客户端"""
        cmd = '''{} & cd {} & start {} '''.format(self.driver[0], self.clientPath, self.exe_path)
        os.system(cmd)
        logger.info('客户端启动成功')

    def close_client(self):
        """关闭客户端"""
        os.popen('taskkill /f /t /im {}'.format(self.driver[-1]))
        logger.info('客户端关闭成功')

    def client_login(self, username, password):
        """登录"""
        # 1.输入学号
        self.click_pic('username_input.png')
        self.type(username)
        logger.info('输入学号：{} 成功'.format(username))
        # 2.输入密码
        self.click_pic('password_input.png')
        self.type(password)
        logger.info('输入密码：{} 成功'.format(password))
        # 3.点击登录
        self.click_pic('login_button.png')
        logger.info('点击登录按钮成功')

    def assert_login_ok(self, file):
        """登录断言"""
        if file == 'student':
            assert self.is_exist('student_201901010103_loginok.png')
            logger.info('【断言】 学生账号登录成功')
        elif file == 'teacher':
            assert self.is_exist('teacher_123_loginok.png')
            logger.info('【断言】 老师账号登录成功')

    def client_student_register(self, name, age, student_number, password):
        """学生注册功能"""
        # 点击学生注册按钮
        self.click_pic('zhuce_btn.png')
        time.sleep(1)
        # 输入名称
        self.rel_click_picture('name.png', x=150)
        self.input_string(name)
        # 输入年龄
        self.rel_click_picture('age.png', x=150)
        self.type(age)
        # 输入学号
        self.rel_click_picture('student_number.png', x=150)
        self.type(student_number)
        # 输入密码
        self.rel_click_picture('password.png', x=150)
        self.type(password)
        # 点击注册按钮
        self.click_pic('zhuce_commit.png')

    def assert_register_ok(self, student_number):
        """断言注册成功"""
        # 提示注册成功
        assert self.is_exist('zhuceok.png'), logger.error('【断言】：学生注册断言失败')
        logger.info('【断言】：学生注册断言成功')
        # 点击确定按钮
        self.click_pic('zhuceok_queding.png')
        # 验证数据库
        sq = Sqlite3Tools(self.db_path)
        res = sq.sqlite3_db_select('select student_name,student_number from student_info;')
        all_name = []
        for r in res:
            all_name.append(r['student_number'])
        assert student_number in all_name, logger.error('【断言】：数据库学生注册断言失败')
        logger.info('【断言】：数据库学生注册成功')
        sq.sqlite3_db_operate('DELETE FROM student_info where student_number = {};'.format(student_number))





if __name__ == '__main__':
    a = ClientPage()
    a.start_client()
    a.client_student_register('正在', '18', '777777777771', '123')
    a.assert_register_ok('777777777771')
    time.sleep(1)
    a.close_client()





