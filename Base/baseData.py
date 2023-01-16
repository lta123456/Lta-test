# -*- coding: utf-8 -*-
import os
import sys
import yaml
from string import Template
from Base.BasePath import BasePath as BP
from Base.baseContainer import GlobalManager
from Base.baseLogger import Logger
from Base.utils import read_config_ini
from Base.baseExcel import Excel
from Base.baseYaml import read_yaml
from Base.baseYaml import yaml_template

logger = Logger('baseData.py').getLogger()


def init_file_path(pic_path):
    '''遍历文件夹下所有Yaml文件路径'''
    path = {}
    # 返回一个列表
    # [('E:\\PyCharm2017\\TestFramework_demo\\Data\\DataElement\\Project1_web', [], ['Web元素信息-百度首页.yaml', '接口元素信息-登录.yaml'])]
    # 第一个参数是传入的文件夹路径
    # 第二个参数是当前文件下文件夹的路径，因为当前文件夹下没有文件夹，所以为空
    # 第三个参数是列表，是当前文件夹下所有文件
    path_lists = [path_list for path_list in os.walk(pic_path)]
    # 遍历列表中所有的元素，参数类型为元组
    # 举例：('E:\\PyCharm2017\\TestFramework_demo\\Data\\DataElement\\Project1_web', [], ['Web元素信息-百度首页.yaml', '接口元素信息-登录.yaml'])
    for path_tup in path_lists:
        # 遍历元组中所有的元素
        # 举例：
        # 'E:\\PyCharm2017\\TestFramework_demo\\Data\\DataElement\\Project1_web'
        # []
        # ['Web元素信息-百度首页.yaml', '接口元素信息-登录.yaml']
        for file_path in path_tup:
            # 判断元素是否为字符串
            # 举例：'E:\\PyCharm2017\\TestFramework_demo\\Data\\DataElement\\Project1_web' 是字符串，将它赋值给value
            # 这样value就是文件夹的路径
            if isinstance(file_path, str):
                value = file_path
            # 判断元素是否是列表
            # 举例：['Web元素信息-百度首页.yaml', '接口元素信息-登录.yaml']
            elif isinstance(file_path, list):
                # 遍历这个列表
                # 举例：
                # Web元素信息-百度首页.yaml
                # 接口元素信息-登录.yaml
                for file_name in file_path:
                    # 此时，file_name就是文件名，将文件名当作字典的key
                    # 将拼接后的路径当作字典的value
                    # 举例：E:\\PyCharm2017\\TestFramework_demo\\Data\\DataElement\\Project1_web\\Web元素信息-百度首页.yaml
                    path[file_name] = os.path.join(value, file_name)
    return path


def is_file_exist(file_path, YamlName):
    '''检查字典中获取的文件名称获取全路径后是否存在'''
    abs_path = file_path.get(YamlName)
    if not abs_path:
        raise FileNotFoundError('文件：{} 不存在，检查文件名 或者配置文件TEST_PROJECT设置 或者配置文件DATA_DRIVER_TYPE设置'.format(YamlName))
    return abs_path


class DataBase:
    '''逻辑层数据读取'''
    def __init__(self, YamlName=None):
        self.gm = GlobalManager()
        self.YamlName = YamlName
        # 读取配置文件的路径
        self.config = read_config_ini(BP.Config_File)
        self.run_config = self.config['项目运行设置']
        # 通过init_file_path获取文件夹下所有数据文件的路径
        self.api_path = init_file_path(os.path.join(BP.Data_Element_Dir, self.run_config['TEST_PROJECT']))
        # 因为客户端的数据是图片，不是数据文件，所以判读自动化测试类型是web还是客户端
        if not self.run_config['AUTO_TYPE'] == 'CLIENT':
            self.abs_path = is_file_exist(self.api_path, self.YamlName)

    def get_element(self, Change_Data=None):
        if Change_Data:
            return yaml_template(self.abs_path, Change_Data)
        else:
            return read_yaml(self.abs_path)


class DataDriver:
    def __init__(self):
        self.gm = GlobalManager()
        self.config = read_config_ini(BP.Config_File)

    def get_case_data(self, fileName):
        '''获取数据驱动文件'''
        data_type = self.config['项目运行设置']['DATA_DRIVER_TYPE']
        abs_path = init_file_path(os.path.join(BP.Data_Driver_Dir, data_type, self.config['项目运行设置']['TEST_PROJECT']))
        data_path = is_file_exist(abs_path, fileName)
        if data_type == 'YamlDriver':
            return read_yaml(data_path)
        elif data_type == 'ExcelDriver':
            return Excel(data_path).dict_data()
        else:
            print('请检查配置文件中DATA_DRIVER_TYPE的设置：{}'.format(data_type))




if __name__ == '__main__':
    dd = DataDriver()
    print(hasattr(dd, 'gm'))
