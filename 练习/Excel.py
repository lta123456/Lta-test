# encoding:utf8
import xlrd
import os

class Excel:
    def __init__(self, ExcelPath, sheet='Sheet1'):
        if not os.path.isfile(ExcelPath):
            raise FileNotFoundError("文件路径错误，请检查：{}".format(ExcelPath))
        # 创建一个文件
        self.data = xlrd.open_workbook(ExcelPath)
        # 选择表
        self.table = self.data.sheet_by_name(sheet)
        # 获取行数
        self.Row = self.table.nrows
        # 获取列数
        self.Col = self.table.ncols
        # 获取第一行数据，作为Key
        self.Key = self.table.row_values(0)

    def dict_data(self):
        if self.Row <= 1:
            print('文件中没有数据')
        else:
            r = []
            j = 1
            for i in range(self.Row - 1):
                # 获取每一行的数据
                value = self.table.row_values(j)
                # 拼接将获取到的标题和值进行拼接
                s = {}
                for x in range(self.Col):
                    s[self.Key[x]] = value[x]
                j += 1
                r.append(s)
            return r


if __name__ == '__main__':
    Path = r'E:\PyCharm2017\dome1\datadriver\excel数据读取\test_data.xlsx'
    a = Excel(Path).dict_data()
    print(a)
