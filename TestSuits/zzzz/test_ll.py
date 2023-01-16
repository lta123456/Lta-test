# encoding:utf-8
import time

import pytest
from selenium import webdriver




class Test_login:

    def test_01(self):
        driver = webdriver.Edge(r'E:\PyCharm2017\TestFramework_demo\Driver\msedgedriver.exe')
        driver.get('http://127.0.0.1/web/guest/home')
        driver.find_element('name', '_58_login').send_keys('test01')
        driver.find_element('name', '_58_password').send_keys('1111')
        driver.find_element('xpath', './/input[@type="submit"]').click()
        time.sleep(2)
        driver.find_element('partial link text', '上传下载').click()


        # driver.find_element_by_id()   1
        # driver.find_element_by_name()  1
        # driver.find_element_by_class_name()  1
        # driver.find_element_by_xpath()  1
        # driver.find_element_by_css_selector()  1
        # driver.find_element_by_tag_name()  1
        # driver.find_element_by_link_text()  1
        # driver.find_element_by_partial_link_text()



