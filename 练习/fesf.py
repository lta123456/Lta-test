# encoding:utf-8
import re
import os
import time

from ExtTools.dbbase import Sqlite3Tools, MysqlHelp
from Base.baseExcel import Excel
from selenium import webdriver
from Base.utils import read_config_ini
from Base.BasePath import BasePath as BP
from Base.baseYaml import read_yaml

config = read_config_ini(BP.Config_File)
dbInfo = config['数据库连接配置']
db = MysqlHelp(
    host=dbInfo['host'],
    user=dbInfo['user'],
    password=dbInfo['psw'],
    port=dbInfo['port'],
    database=dbInfo['database'],
)


res = db.mysql_db_select('select * from dlfileentry order by createDate desc')
print(res)



# file_path = os.path.join(BP.Data_Temp_Dir, 'upload_file.txt')
# print(file_path)
# print(r'E:\PyCharm2017\TestFramework_demo\Data\Temp\upload_file.txt')
#
# driver = webdriver.Ie(r'E:\PyCharm2017\TestFramework_demo\Driver\IEDriverServer.exe')
#
#
# login = read_yaml(r'E:\PyCharm2017\TestFramework_demo\Data\DataElement\p02_web_gjxt\01登录页面元素信息.yaml')
# driver.get('http://127.0.0.1/web/guest/home')
# data = login['login']
#
# driver.find_element(data['password_input'][0], data['password_input'][1]).send_keys('1111')
# driver.find_element(data['login_btn'][0], data['login_btn'][1]).click()
# time.sleep(2)
#
# driver.find_element('xpath', './/span[text()="文档上传下载"]').click()
# time.sleep(1)
# driver.find_element('xpath', './/ul[@class="lfr-component"]/li[2]/a').click()
# time.sleep(1)
# a = driver.find_element('xpath', './/div[@class="results-grid"]/table/tbody/tr/td[@class="col-1"]/a').get_attribute('href')
# print(a)

