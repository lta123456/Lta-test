# encoding:utf-8
# from Base.baseContainer import GlobalManager
# # 导入存变量set脚本
# from TestSuits.set_var import set_var
#
# # 执行set脚本，存变量
# set_var()
#
# g = GlobalManager()
# # 取变量
# print(g.get_value('name'))


a = '["feawf", "fewarew"]'

b = eval(a)

print(';'.join(b))