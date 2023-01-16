# encoding: utf-8
'../../Reports/ALLURE/Result'
import yaml

'../../Reports/ALLURE/Report'

data = {
    'date': '${date}',
    'pri': '${priority}',
    'name': '${name}',
    'begin': '${start_time}',
    'end': '${end_time}',
    'type': 'custom',
    'private': '1'
}
with open(r'E:\PyCharm2017\TestFramework_demo\Data\DataElement\chandao\p01_http_cd\03仪表盘页面接口信息.yaml', 'r') as f:
    yaml_data = yaml.load(f, Loader=yaml.Loader)
yaml_data['add_backlog']['data']['private'] = '1'
with open(r'E:\PyCharm2017\TestFramework_demo\Data\DataElement\chandao\p01_http_cd\03仪表盘页面接口信息.yaml', 'w') as b:
    yaml.dump(data=yaml_data, stream=b, allow_unicode=True)