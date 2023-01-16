# encoding:utf-8
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from Base.baseData import DataBase
from Base.baseLogger import Logger

logger = Logger('baseAutoWeb.py').getLogger()

class WebBase(DataBase):
    '''Web自动化基类'''
    def __init__(self, YamlName):
        super().__init__(YamlName=YamlName)
        self.driver = self.gm.get_value('driver')
        # 每隔0.5秒检测一次
        self.t = 0.5
        # 最大等待时间
        self.time = 10

    def get_locator_data(self, locator, change_Data=None):
        '''获取元素数据'''
        res = self.get_element(change_Data)
        items = locator.split('/')
        locator_data = tuple(res[items[0]][items[1]])
        return locator_data

    def fingElement(self, locator, change_Data=None):
        '''元素定位'''
        try:
            locator = self.get_locator_data(locator, change_Data)
            if isinstance(locator, list):
                locator = tuple(locator)
            if not isinstance(locator, tuple):
                logger.error('传入的参数类型错误，必须传列表或者元组类型：loc = ["id", "value1"]')
            logger.debug('正在定位元素信息：定位方式：{}，value值：{}'.format(locator[0], locator[1]))
            ele = WebDriverWait(self.driver, self.time, self.t).until(EC.presence_of_element_located(locator))
            logger.debug('元素信息定位成功：{}'.format(locator))
            return ele
        except Exception as e:
            logger.error('未定位到元素：{}'.format(locator))
            raise e

    def fingElements(self, locator, change_Data=None):
        '''元素定位'''
        try:
            locator = self.get_locator_data(locator, change_Data)
            if isinstance(locator, list):
                locator = tuple(locator)
            if not isinstance(locator, tuple):
                logger.error('传入的参数类型错误，必须传列表或者元组类型：loc = ["id", "value1"]')
            logger.debug('正在定位元素信息：定位方式：{}，value值：{}'.format(locator[0], locator[1]))
            ele = WebDriverWait(self.driver, self.time, self.t).until(EC.presence_of_all_elements_located(locator))
            logger.debug('元素信息定位成功：{}'.format(locator))
            return ele
        except Exception as e:
            logger.error('未定位到元素：{}'.format(locator))
            raise e

    def get_url(self, url):
        '''打开url'''
        self.driver.get(url)
        self.driver.maximize_window()
        logger.debug('浏览器请求访问地址：{}'.format(url))

    def click(self, locator, change_Data=None):
        '''元素点击'''
        try:
            ele = self.fingElement(locator, change_Data)
            ele.click()
            logger.debug('元素点击：{} 成功'.format(locator))
        except Exception as e:
            logger.error('元素点击：{} 失败'.format(locator))
            raise e

    def clear(self, locator, change_Data=None):
        '''清空输入框的文本'''
        try:
            ele = self.fingElement(locator, change_Data)
            ele.clear()
            logger.debug('清空输入框：{} 成功'.format(locator))
        except Exception as e:
            logger.error('清空输入框：{} 失败'.format(locator))
            raise e

    def sendkeys(self, locator, text, change_Data=None):
        '''输入文本'''
        try:
            ele = self.fingElement(locator, change_Data)
            ele.send_keys(text)
            logger.debug('输入文本 {} 成功'.format(text))
        except Exception as e:
            logger.error('输入文本 {} 失败'.format(text))
            raise e

    def get_title(self):
        '''获取页面title'''
        try:
            title = self.driver.title
            logger.debug('获取title {} 成功'.format(title))
            return title
        except Exception as e:
            logger.error('获取title 失败')
            return ''

    def get_text(self, locator, change_Data=None):
        '''获取文本'''
        try:
            content = self.fingElement(locator, change_Data).text
            logger.debug('获取文本 {} 成功'.format(content))
            return content
        except Exception as e:
            logger.error('获取文本 失败')
            return ''

    def get_attribute(self, locator, name, change_Data=None):
        '''获取属性'''
        try:
            ele = self.fingElement(locator, change_Data)
            attr = ele.get_attribute(name)
            logger.debug('获取属性 {} 成功'.format(name))
            return attr
        except Exception as e:
            logger.error('获取属性 失败')
            return ''

    def isSelected(self, locator, change_Data=None):
        '''判断元素是否被选中'''
        ele = self.fingElement(locator, change_Data)
        r = ele.is_selected()
        return r

    def is_title(self, _title):
        '''判断标题是否与预期相同'''
        try:
            result = WebDriverWait(self.driver, self.time, self.t).until(EC.title_is(_title))
            return result
        except:
            return False

    def is_title_contains(self, _title):
        '''判断标题是否包含预期目标'''
        try:
            result = WebDriverWait(self.driver, self.time, self.t).until(EC.title_contains(_title))
            return result
        except:
            return False

    def is_text_in_element(self, locator, _text, change_data=None):
        '''判断元素的文本值是否与预期的一致'''
        try:
            locator = self.get_locator_data(locator, change_data)
            result = WebDriverWait(self.driver, self.time, self.t).until(EC.text_to_be_present_in_element(locator, _text))
            return result
        except:
            return False

    def is_value_in_element(self, locator, _value, change_data=None):
        '''判断元素的value值是否符合预期目标'''
        try:
            locator = self.get_locator_data(locator, change_data)
            result = WebDriverWait(self.driver, self.time, self.t).until(EC.text_to_be_present_in_element_value(locator, _value))
            return result
        except:
            return False

    def is_alert(self):
        '''判读页面上是否有alert弹窗'''
        try:
            result = WebDriverWait(self.driver, self.time, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def mouse_move_to(self, locator, change_data=None):
        '''鼠标悬停'''
        ele = self.fingElement(locator, change_data)
        ActionChains(self.driver).move_to_element(ele).perform()
        logger.debug('鼠标在 {} 元素悬停')

    def mouse_drag_to(self, locator, x, y, change_data=None):
        '''鼠标拖拽'''
        ele = self.fingElement(locator, change_data)
        ActionChains(self.driver).drag_and_drop_by_offset(ele, x, y)
        logger.debug('鼠标在 {} 元素拖拽到 x:{}, y:{}'.format(locator, x, y))

    def js_focus_element(self, locator, change_data=None):
        '''滑动滚动条，直到指定的元素出现'''
        ele = self.fingElement(locator, change_data)
        self.driver.execute_script('arguments[0].scrollIntoView();', ele)
        logger.info('聚焦元素 {}'.format(locator))

    def js_scroll_end(self, x=0):
        '''滑动到底部'''
        js = 'window.scrollTo({},document.body.scrollHeight)'.format(x)
        self.driver.execute_script(js)
        logger.info('滑动滚动条到底部')

    def js_scroll_top(self):
        '''滑动到顶部'''
        js = 'window.scrollTo(0,0)'
        self.driver.execute_script(js)
        logger.info('滑动滚动条到顶部')

    def keyboard_send_keys_to(self, locator, text, change_data=None):
        '''模拟键盘输入'''
        ele = self.fingElement(locator, change_data)
        ActionChains(self.driver).send_keys_to_element(ele, text).perform()
        logger.info('键盘在 {} 位置输入：{}'.format(locator, text))

    def get_alert_text(self):
        '''获取弹窗文本'''
        time.sleep(1)
        confirm = self.driver.switch_to.alert
        logger.info('获取弹窗文本：{}'.format(confirm.text))
        return confirm.text

    def alert_accept(self):
        '''弹窗点击确定'''
        time.sleep(1)
        confirm = self.driver.switch_to.alert
        confirm.accept()
        logger.info('弹窗点击确定')

    def alert_dismiss(self):
        '''弹窗点击取消'''
        time.sleep(1)
        confirm = self.driver.switch_to.alert
        confirm.dismiss()
        logger.info('弹窗点击取消')

    def input_alert(self, text):
        '''弹窗输入文本'''
        time.sleep(1)
        prompt = self.driver.switch_to.alert
        prompt.send_keys(text)
        logger.info('弹窗输入文本值：{}'.format(text))

    def select_by_index(self, locator, index=0, change_data=None):
        '''通过索引选择下拉框值'''
        ele = self.fingElement(locator, change_data)
        Select(ele).select_by_index(index)
        logger.info("选择 {} 下拉框的下拉列表的下拉项索引：{}".format(locator, index))

    def select_by_value(self, locator, value, change_data=None):
        '''通过下拉项名称选择下拉项值'''
        ele = self.fingElement(locator, change_data)
        Select(ele).select_by_value(value)
        logger.info("选择 {} 下拉框的下拉列表的下拉项值：{}".format(locator, value))

    def select_by_text(self, locator, text, change_data=None):
        '''通过下拉项文本值选择下拉项值'''
        ele = self.fingElement(locator, change_data)
        Select(ele).select_by_visible_text(text)
        logger.info("选择 {} 下拉框的下拉列表的文本值：{}".format(locator, text))

    def switch_iframe(self, locator, change_data=None):
        '''切换iframe'''
        try:
            id_index_locator = self.get_locator_data(locator, change_data)
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, list) or isinstance(id_index_locator, tuple):
                ele = self.fingElement(locator)
                self.driver.switch_to.frame(ele)
            logger.info('iframe 切换为 {}'.format(id_index_locator))
        except Exception as e:
            logger.error('iframe 切换异常：{}，{}'.format(locator, e))
    def switch_iframe_out(self):
        '''切换iframe到最外层'''
        try:
            self.driver.switch_to.default_content()
            logger.info('iframe切换最外层成功')
        except Exception as e:
            logger.error('iframe切换到最外层失败  {}'.format(e))

    def switch_iframe_up(self):
        '''切换iframe到最外层'''
        try:
            self.driver.switch_to.parent_frame()
            logger.info('iframe切换到上一层成功')
        except Exception as e:
            logger.error('iframe切换到上一层失败 {}'.format(e))

    def get_handles(self):
        '''获取当前所有窗口'''
        try:
            handles = self.driver.window_handles
            logger.info('获取所有的handles：{}'.format(handles))
            return handles
        except Exception as e:
            logger.error('获取所有的handles失败 {}'.format(e))

    def switch_handle(self, index=-1):
        '''切换窗口'''
        try:
            handle_list = self.get_handles()
            self.driver.switch_to.window(handle_list[index])
            logger.info('切换handle成功：{}'.format(index))
        except Exception as e:
            logger.error('切换handle失败：{}'.format(e))


if __name__ == '__main__':
    c = WebBase('01登录页面元素信息.yaml')
    print(c.get_locator_data('login/username_input'))
    a = ['login', 'username_input']










