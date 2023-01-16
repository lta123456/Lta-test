# encoding:utf-8

class GlobalManager:

    _globadict = {}
    _instance = False

    def set_value(self, name, value):
        '''存变量'''
        self._globadict[name] = value

    def get_value(self, name):
        '''取变量'''
        try:
            return self._globadict[name]
        except KeyError as e:
            print('变量不存在：{}'.format(name))

    def __new__(cls, *args, **kwargs):
        if cls._instance == False:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance