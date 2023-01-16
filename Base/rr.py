# encoding:utf-8
import os
from Base.utils import read_config_ini
from Base.BasePath import BasePath as BP
from ExtTools.dbbase import Sqlite3Tools
from Base.baseExcel import Excel


dir_path = r'E:\学习笔记\客户端自动化软件\03项目资料\学生管理系统\学生管理系统\客户端程序'
client_path = os.path.join(dir_path, 'main.exe')
db_path = os.path.join(dir_path, 'student.db')
excel_path = os.path.join(dir_path, '语文排序成绩.xls')

sq = Sqlite3Tools(db_path)
res = sq.sqlite3_db_select('select * from student_achievement order by student_number;')

excel = Excel(excel_path)
excel_data = excel.dict_data()

# 把从excel表中传入的空值转换为None
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

    excel_data[c] = a



def sort(list):
    for i in range(1, len(list)):
        for j in range(0, len(list) - 1):
            if list[j]['student_number'] > list[j + 1]['student_number']:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list


if sort(excel_data) == res:
    print('成功！！！')





# dict = {'a': '1', 'b': '2', 'c': '3'}
# my = [k for k, v in dict.items() if v == '3']
# print(my)
# a = [('a', '1'), ('b', '2'), ('c', '2')]
# for b, c in a:
#     if c == '2':
#         print(b)

