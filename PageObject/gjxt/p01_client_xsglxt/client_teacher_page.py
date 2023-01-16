# encoding:utf-8

import os
import time
from Base.baseExcel import Excel
from ExtTools.dbbase import Sqlite3Tools
from PageObject.p01_client_xsglxt.client_start_stop import ClientPage
from Base.baseAutoClient import GuiBase
from Base.baseLogger import Logger

logger = Logger('client_teacher_page.py').getLogger()


class TeacherPage(GuiBase):

    def __init__(self):
        super().__init__()
        self.db_path = r'E:\学习笔记\客户端自动化软件\03项目资料\学生管理系统\学生管理系统\客户端程序\student.db'

    def client_teacher_view_transcripts(self):
        """老师查看学生成绩单"""
        # 点击查看学生成绩单按钮
        self.click_pic('teacher_view_Transcripts.png')
        # 点击下拉框
        self.click_pic('view_Transcripts_Dropdowns_Btn.png')
        # 点击数学
        self.click_pic('math.png')
        # 点击降序
        self.rel_click_picture('DESC.png', x=-35)
        # 点击查看学生成绩单按钮
        self.click_pic('View_Transcripts.png')

    def assert_client_teacher_view_transcripts(self):
        """断言查看学生成绩单"""
        assert self.is_exist('assert_Transcripts.png'), logger.info('【断言】：查看学生成绩单用例断言失败')
        logger.info('【断言】：查看学生成绩单用例断言成功')
        assert self.is_exist('assert_desc.png'), logger.info('【断言】：未按数学成绩降序排序')
        logger.info('【断言】：按数学成绩降序排序')

    def client_teacher_alter_grade(self, student_number, grade):
        """老师修改学生成绩"""
        # 点击修改学生成绩按钮
        self.click_pic('teacher_alter_grade_btn.png')
        # 点击科目下拉框
        self.click_pic('teacher_course_dropdown.png')
        # 选中物理
        self.click_pic('physics.png')
        # 点击学号输入框
        self.rel_click_picture('student_number.png', x=100)
        # 输入学号
        self.type(student_number)
        # 点击成绩输入框
        self.rel_click_picture('grade.png', x=100)
        # 全选输入框中的文本
        self.hotkey('ctrl', 'a')
        # 删除输入框中的文本
        self.press('BackSpace')
        # 输入成绩
        self.type(grade)
        # 点击确定修改
        self.click_pic('alter_commit_btn.png')

    def assert_client_teacher_alter_grade(self, student_number, grade):
        """【断言】：修改物理成绩"""
        assert self.is_exist('assert_alter_ok.png'), logger.error('【断言】：修改学生成绩失败')
        logger.info('【断言】：修改学生成绩成功')
        sq = Sqlite3Tools(self.db_path)
        res = sq.sqlite3_db_select('select * from student_achievement where student_number = {}'.format(student_number))
        print(res)
        assert res[0]['物理'] == int(grade), logger.error('【断言】：数据库修改学生成绩失败')
        logger.info('【断言】：数据库修改学生成绩成功')

    def client_teacher_export_score(self, course, sort):
        """老师导出学生成绩"""
        # 点击查看学生成绩单
        self.click_pic('teacher_view_score.png')
        # 选择科目
        self.click_pic('course_dropdown_btn.png')
        # 根据传入的数据选择科目
        if course == '语文':
            self.click_pic('course_language.png')
        elif course == '数学':
            self.click_pic('course_math.png')
        elif course == '英语':
            self.click_pic('course_English.png')
        elif course == '物理':
            self.click_pic('course_phy.png')
        if sort == '升序':
            self.rel_click_picture('sort_asc.png', x=-35)
        elif sort == '降序':
            self.rel_click_picture('sort_desc.png', x=-35)
        # 点击导出某科升序/降序学生成绩单
        self.click_pic('teacher_export_score.png')

    def assert_client_teacher_export_score(self, file_path):
        """【断言】：老师导出学生成绩"""
        assert self.is_exist('assert_export_ok.png'), logger.error('【断言】：导出学生成绩失败!')
        logger.info('【断言】：导出学生成绩成功!')
        assert os.path.exists(file_path), logger.error('【断言】：导出文件不存在，或者路径错误')
        logger.info('【断言】：导出文件成功!')
        time.sleep(3)
        # 数据库与excel文件数据对比
        sq = Sqlite3Tools(self.db_path)
        res = sq.sqlite3_db_select('select * from student_achievement order by student_number;')
        excel_data = Excel(file_path).dict_data()

        # 将从excel表中传入的空值转换为None
        for c in range(len(excel_data)):
            a = excel_data[c]
            # 获取集合中的key值
            key = [key for key in a.keys()]
            # 获取集合中的value值
            value = [value for value in a.values()]

            # 循环判断value值是否等于''，等于则将value列表中的''转换为None
            for i in range(len(key)):
                if value[i] == '':
                    value[i] = None

            # 把key列表中的元素当作
            a = {}
            for i in range(len(key)):
                a[key[i]] = value[i]
            # 把excel读取的数据替换为转换后的数据
            excel_data[c] = a

        # 排序
        def sort(list):
            for i in range(1, len(list)):
                for j in range(0, len(list) - 1):
                    if list[j]['student_number'] > list[j + 1]['student_number']:
                        list[j], list[j + 1] = list[j + 1], list[j]
            return list

        assert sort(excel_data) == sort(res), logger.error('【断言】：导出文件数据与数据库数据不一致!')
        logger.info('【断言】：导出文件数据与数据库数据一致!')

        # 删除文件
        os.remove(file_path)





if __name__ == '__main__':
    cp = ClientPage()
    cp.start_client()
    cp.client_login('123', '123')
    tp = TeacherPage()
    tp.client_teacher_export_score('数学', '降序')
    tp.assert_client_teacher_export_score(r'E:\学习笔记\客户端自动化软件\03项目资料\学生管理系统\学生管理系统\客户端程序\语文排序成绩.xls')


