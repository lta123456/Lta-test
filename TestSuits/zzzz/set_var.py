# encoding:utf-8

from Base.baseContainer import GlobalManager

g = GlobalManager()


def set_var():
    g.set_value('name', '取出的变量')