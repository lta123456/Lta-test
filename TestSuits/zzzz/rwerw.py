# encoding:utf-8
from selenium import webdriver
import os
from Base.BasePath import BasePath as BP


driver = webdriver.Firefox(executable_path='/Driver/geckodriver.exe')

driver.get('https://www.baidu.com/')















# a = driver.find_element('xpath', ".//*[text()='音乐']")
# b = driver.find_element('id', 'my-interest')
# driver.maximize_window()
# time.sleep(1)
# # 被拖动元素的位置
# pyautogui.moveTo(a.location['x'] + 60, a.location['y'] + 180, duration=0.2)
# time.sleep(1)
# # 拖动到
# pyautogui.dragTo(b.location['x'] + 150, b.location['y'] + 250, duration=0.5)