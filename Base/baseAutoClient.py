# encoding:utf-8
import os
import time
import pyautogui
import pyperclip
from Base.baseData import DataBase
from Base.utils import *
from Base.baseLogger import Logger
from Base.BasePath import BasePath as BP

logger = Logger('baseAutoClient.py').getLogger()

# 继承父类
class GuiBase(DataBase):
    def __init__(self):
        # 执行父类的__init__方法
        super().__init__()
        # 设置鼠标移动速度；0为立即执行
        self.duration = float(self.config['客户端自动化配置']['duration'])
        # 每次点击间隔
        self.interval = float(self.config['客户端自动化配置']['interval'])
        # 隐式等待时间
        self.minSearchTime = float(self.config['客户端自动化配置']['minSearchTime'])
        # 设置图片识别信任度
        self.confidence = float(self.config['客户端自动化配置']['confidence'])
        # 是否灰度匹配
        self.grayscale = bool(self.config['客户端自动化配置']['grayscale'])


    def _is_file_exist(self, file_name):
        '''封装判断文件是否存在方法'''
        # 通过父类BaseData中的self.api_path获取图片路径
        abs_path = self.api_path.get(file_name)
        # 判断路径是否存在
        if not abs_path:
            raise FileNotFoundError("文件：{}不存在，请检查文件名称或者配置文件")
        return abs_path

    def is_exist(self, file_name, searchTime=None):
        '''检查图片是否出现在屏幕'''
        pic_path = self._is_file_exist(file_name)
        if not searchTime:
            searchTime = self.minSearchTime
        # 获取坐标
        coordinates = pyautogui.locateOnScreen(pic_path, minSearchTime=searchTime, confidence=self.confidence, grayscale=self.grayscale)
        if coordinates:
            logger.debug('查找图片{}存在'.format(file_name))
            # 获取中心坐标
            return pyautogui.center(coordinates)
        else:
            logger.debug('查找对象{}不存在'.format(file_name))
            return None

    def _error_record(self, name, type):
        '''错误截图'''
        pyautogui.screenshot(os.path.join(BP.SCREENSHOT_Dir, name))
        logger.error('类型：{}，查找图片 {} 位置，当前图片无此内容，已截图'.format(type, name))
        raise pyautogui.ImageNotFoundException

    def click_pic(self, pic_name, clicks=1, button='left', isclick=True):
        '''图片点击'''
        pos_x_y = self.is_exist(pic_name)
        # 如果图片不存在，则截图
        if not pos_x_y:
            self._error_record(pic_name, 'click_pic')
        # 鼠标悬浮
        pyautogui.moveTo(*pos_x_y, duration=self.duration)
        # 点击
        if isclick:
            pyautogui.click(*pos_x_y, clicks=clicks, interval=self.interval, button=button, duration=self.duration)
            logger.debug('移动到图片：{} 位置{}，点击：{} 成功，点击次数：{}'.format(pic_name, pos_x_y, pic_name, clicks))
        else:
            logger.debug('移动到图片：{} 位置{}，未点击'.format(pic_name, pos_x_y))

    def rel_click_picture(self, pic_name, x=0, y=0, clicks=1, button='left', isclick=True):
        '''相对位置点击'''
        pos_x_y = self.is_exist(pic_name)
        # 如果图片不存在，则截图
        if not pos_x_y:
            self._error_record(pic_name, 'click_pic')
        pyautogui.moveTo(*pos_x_y, duration=self.duration)
        pyautogui.moveRel(x, y, duration=self.duration)
        if isclick:
            pyautogui.click(clicks=clicks, interval=self.interval, button=button, duration=self.duration)
            logger.debug('移动到图片：{} 偏移 x:{}，y:{}，点击：{} 成功，点击次数：{}'.format(pic_name, x, y, pic_name, clicks))
        else:
            logger.debug('移动到图片：{} 偏移 x:{}，y:{}，未点击'.format(pic_name, x, y))

    def click(self, x=None, y=None, clicks=1, button='left'):
        '''点击'''
        pyautogui.click(x, y, clicks=clicks, button=button, interval=self.interval, duration=self.duration)
        logger.debug('移动到 x:{}，y:{}，点击{}键 成功，点击次数：{}'.format(x, y, button, clicks))

    def rel_click(self, rel_x, rel_y, clicks=1, button='left'):
        '''相对位置点击'''
        pyautogui.move(rel_x, rel_y, duration=self.duration)
        pyautogui.click(clicks=clicks, button=button, interval=self.interval)
        logger.debug('鼠标在相对位置 x:{}，y:{}，点击{}键 成功，点击次数：{}'.format(rel_x, rel_y, button, clicks))

    def moveto(self, x, y, rel=False):
        '''鼠标移动，rel为True，则为相对位置移动'''
        if rel:
            pyautogui.moveRel(x, y, duration=self.duration)
            logger.debug('鼠标相对位置移动距离：x:{}, y:{}'.format(x, y))
        else:
            pyautogui.moveTo(x, y, duration=self.duration)
            logger.debug('鼠标移动到：x:{}, y:{}'.format(x, y))

    def dragto(self, x, y, button='left', rel=False):
        '''鼠标拖拽，rel为True，则为相对位置移动'''
        if rel:
            pyautogui.dragRel(x, y, button=button, duration=self.duration)
            logger.debug('鼠标相对位置拖拽：x:{}, y:{}'.format(x, y))
        else:
            pyautogui.dragTo(x, y, button=button, duration=self.duration)
            logger.debug('鼠标绝对位置拖拽：x:{}, y:{}'.format(x, y))

    def scroll(self, amount_to_scroll, moveToX=None, moveToY=None):
        '''鼠标的滑轮滚动'''
        pyautogui.scroll(clicks=amount_to_scroll, x=moveToX, y=moveToY)
        logger.debug('鼠标滑轮滚动 {} 距离'.format(amount_to_scroll))

    def type(self, *text):
        '''键盘输入长文本'''
        pyautogui.write(*text)
        logger.debug('文本框输入：{}'.format(text))

    def input_string(self, text, clear=True):
        '''输入中文'''
        pyperclip.copy(text)
        # 快捷键
        if clear:
            pyautogui.hotkey('ctrl', 'v')
            logger.debug('文本框输入：{}'.format(text))

    def press(self, key):
        pyautogui.press(key)
        logger.debug('按下键盘按键：{}'.format(key))

    def hotkey(self, *keys):
        '''键盘的组合键'''
        pyautogui.hotkey(*keys)
        logger.debug("执行快捷键：{}".format(keys))


if __name__ == '__main__':
    gui = GuiBase()
    gui.hotkey('ctrl', 'v')
    gui.type('fewafeawfwefwaf')



