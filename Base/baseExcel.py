# encoding:utf-8
import xlrd

class Excel:
    def __init__(self, ExcelPaht, read_sheet_name='Sheet1'):
        # 1、创建Excel对象
        self.data = xlrd.open_workbook(ExcelPaht)
        # 打开表
        self.table = self.data.sheet_by_name(read_sheet_name)
        # 获取有效行数
        self.Row = self.table.nrows
        # 获取有效列数
        self.Col = self.table.ncols
        # 获取标题
        self.key = self.table.row_values(0)

    def dict_data(self):
        if self.Row <= 1:
            print('表中没有有效的数据')
        else:
            r = []
            j = 1
            for i in range(self.Row - 1):
                s = {}
                value = self.table.row_values(j)
                for x in range(self.Col):
                    s[self.key[x]] = value[x]
                r.append(s)
                j += 1
            return r