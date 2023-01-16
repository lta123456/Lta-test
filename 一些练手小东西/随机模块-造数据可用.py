# encoding: utf-8

from faker import Faker

f = Faker()
f1 = Faker(locale="zh_CN")

# 创建随机名称：
print(f'随机英文人名：{f.name()}')
# 中文需要在实例化Faker()括号中输入  locale="zh_CN"
print(f'随机中文人名：{f1.name()}')
# 随机地址
print(f'随机地址：{f1.address()}')
# 随机岗位
print(f'随机岗位：{f1.job()}')
