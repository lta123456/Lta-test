# encoding: utf-8
import threading
from threading import Thread


class MyThread(Thread):

    def __init__(self, fo, *args):
        """
        多线程执行
        :param fo: 方法名称，不要加括号
        :param args: 这个方法的各项参数
        """
        Thread.__init__(self)
        self.fo = fo
        self.param = args

    def run(self):
        lock = threading.Lock
        lock.acquire()
        self.result = self.fo(*self.param)

    def get_result(self):
        """
        返回方法的返回值
        :return: 方法的返回值
        """

        return self.result

