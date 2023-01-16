# encoding:utf-8
import yaml
import os
from string import Template


def read_yaml(YamlPath):
    if not os.path.isfile(YamlPath):
        raise FileNotFoundError("文件路径错误，请检查")
    with open(YamlPath, 'r', encoding='utf-8') as f:
        cfg = f.read()
    YamlData = yaml.load(cfg, Loader=yaml.FullLoader)
    return YamlData


def yaml_template(YamlPath, Change_data):
    if not os.path.isfile(YamlPath):
        raise FileNotFoundError("文件路径错误，请检查")
    if not isinstance(Change_data, dict):
        raise TypeError('传入的数据类型错误，必须为字典，请检查：{}'.format(Change_data))
    with open(YamlPath, 'r') as f:
        cfg = f.read()
        YamlData = Template(cfg).safe_substitute(Change_data)
        return yaml.load(YamlData, Loader=yaml.FullLoader)


def write_yaml(YamlPath, data):
    with open(YamlPath, 'w') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# yaml里引用yaml文件
class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


def yaml_read_yaml(yaml_path):
    """
    yaml文件里引用yaml文件
    格式：  c: !include 需要引用的yaml文件路径
    :param yaml_path: yaml文件路径
    :return: 读取的数据
    """
    with open(yaml_path, 'r') as f:
        return yaml.load(f, Loader)


if __name__ == '__main__':
    print(yaml_read_yaml(r'E:\PyCharm2017\TestFramework_demo\a.yaml'))
    # with open(r'E:\PyCharm2017\TestFramework_demo\a.yaml', 'r') as f:
    #     data = yaml.load(f)
    #     print(data)
