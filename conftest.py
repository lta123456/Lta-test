# encoding:utf-8
import base64
import time

import pytest
from io import BytesIO
from py.xml import html
from Base.utils import *
from Base.BasePath import BasePath as BP
from Base.baseContainer import GlobalManager
from Base.baseYaml import write_yaml
from Base.baseLogger import Logger

logger = Logger('conftest.py').getLogger()

config = read_config_ini(BP.Config_File)
gm = GlobalManager()
gm.set_value('CONFIG_INFO', config)
insert_js_html = False


# 钩子函数
def pytest_addoption(parser):
    '''添加命令行参数 --browser、--host'''
    parser.addoption(
        # 参数名称                     如果没有指定，则使用的默认值                    提示信息
        '--browser', action='store', default=config['WEB自动化配置']['browser'], help='browser option: firefox or chrome or ie'
    )
    # 添加host参数，设置默认测试环境地址
    parser.addoption(
        # 参数名称                  如果没有指定，则使用的默认值                    提示信息
        '--host', action='store', default=config['项目运行设置']['TEST_URL'], help='test host->http://10.11.1.171:8888'
    )

@pytest.fixture(scope='function')
def driver(request):
    try:
        from selenium import webdriver
        # 通过这个方法获取上面钩子函数获取的浏览器设置：firefox or chrome or ie
        name = request.config.getoption('--browser')
        # 先定义一个driver，不然后面的driver都是if那个作用域里的，无法存入全局变量管理器中
        _driver = None
        if name == 'ie':
            _driver = webdriver.Ie(executable_path=os.path.join(BP.Driver_Dir, 'IEDriverServer.exe'))
        elif name == 'firefox':
            _driver = webdriver.Firefox(executable_path=os.path.join(BP.Driver_Dir, 'geckodriver.exe'))
        elif name == 'chrome':
            _driver = webdriver.Chrome(executable_path=os.path.join(BP.Driver_Dir, 'chromedriver.exe'))
        elif name == 'edge':
            _driver = webdriver.Edge(executable_path=os.path.join(BP.Driver_Dir, 'msedgedriver.exe'))
        # chromeheadless: 无头浏览器，不显示浏览器页面执行
        elif name == 'chromeheadless':
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            # 增加一个参数--headless 无头浏览器
            chrome_options.add_argument('--headless')
            #                                                                                           使用设置
            _driver = webdriver.Chrome(executable_path=os.path.join(BP.Driver_Dir, 'chromedriver.exe'), chrome_options=chrome_options)
            # 设置浏览器大小，这样才能把元素都显示在界面上
            _driver.set_window_size(width=1920, height=1080)
        # _driver存入全局变量管理器
        gm.set_value('driver', _driver)
        _driver.implicitly_wait(5)
        logger.info('正在启动浏览器名称：{}'.format(name))
        def fn():
            logger.info('当全部用例执行完成之后：teardown quit driver!')
            _driver.quit()
        request.addfinalizer(fn)
        return _driver
    except ImportError:
        pytest.exit('未安装selenium库')
    except Exception as e:
        pytest.exit('启动webdriver错误：{}'.format(e))


def pytest_html_results_summary(prefix, summary, postfix):
    '''html测试报告 Summary(摘要)部分在此设置'''
    prefix.extend([html.p("自动化测试工程师：李泰昂"),
                   html.p('fewff')])

# 钩子函数，修改HTML报告的结果
# 修改结果的标题
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th("Description"))
    cells.pop()

# 钩子函数，修改HTML报告的结果
# 修改结果的内容
def pytest_html_results_table_row(report, cells):
    # 判断测试用例是否有注释
    if hasattr(report, 'description'):
        cells.insert(1, html.td(report.description))
        cells.pop()
    else:
        print("!!!!!!!!!!!!!!", report.longreprtext)


def _capture_screenshot_sel():
    """WEB自动化截图"""
    driver = gm.get_value('driver')
    if not driver:
        pytest.exit('driver 获取为空')
    # 截图并保存到指定的文件夹
    driver.get_screenshot_as_file(BP.SCREENSHOT_PIC)
    # 以base64方式返回
    return driver.get_screenshot_as_base64()

def _capture_screenshot_pil():
    """客户端自动化截图"""
    try:
        from PIL import ImageGrab
        # 将BytesIO模块起一个名称
        output_buffer = BytesIO()
        # 将屏幕或剪贴板的内容复制到PIL图像存储器
        img = ImageGrab.grab()
        # 将此图像保存在给定的文件名下
        img.save(BP.SCREENSHOT_PIC)
        img.save(output_buffer, 'png')
        # 在内存中读取
        bytes_value = output_buffer.getvalue()
        # 关闭BytesIO模块
        output_buffer.close()
        # 返回截图
        return base64.b64encode(bytes_value).decode()
    except ImportError:
        pytest.exit('未安装PIL')

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    '''测试失败，自动截图'''
    # 和自定义前置后置中的yield差不多，分割，下面的是执行测试用例之后执行的
    outcome = yield
    # 导入pytest-html模块
    pytest_html = item.config.pluginmanager.getplugin('html')
    # 获取测试报告对象
    report = outcome.get_result()
    # 获取测试报告这个对象(report)里的extra属性
    # 获取调用结果的测试报告，返回一个report对象, report对象的属性包括when（steup, call, teardown三个值）、nodeid(测试用例的名字)、 outcome(用例的执行结果，passed,failed)
    extra = getattr(report, 'extra', [])
    # 上面的是固定写法

    # 判断当前测试用例是否处于执行或者前置阶段，处于的话，就生成测试报告
    if report.when == 'call' or report.when == 'setup':
        # 通过hasattr判断report对象是否有wasxfail这个属性
        # 判断是不是预期失败的测试用例
        xfail = hasattr(report, 'wasxfail')
        # 判断当前自动化是否是web或者客户端自动化测试，因为接口测试没有UI
        if config['项目运行设置']['AUTO_TYPE'] == 'WEB':
            # 使用自己定义的方法将截图结果存入变量中
            screen_img = _capture_screenshot_sel()
        elif config['项目运行设置']['AUTO_TYPE'] == 'CLIENT':
            screen_img = _capture_screenshot_pil()
        else:
            screen_img = None
        # 判断当前的测试是否失败
        if (report.skipped and xfail) or (report.failed and not xfail) and screen_img:
            # 图片的名称
            file_name = report.nodeid.replace("::", "_") + ".png"
            # 判断测试报告是否为HTML
            if config['项目运行设置']['REPORT_TYPE'] == 'HTML':
                # 判断截图是否存在
                if file_name:
                    # 将图片插入到html文本中
                    html = '<div><img src="Data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                           'onclick="lookimg(this.src)" align="right"/></div>' % screen_img
                    # 图片自适应
                    script = '''
                    <script>
                        function lookimg(str)
                        {
                            var newwin=window.open();
                            newwin.document.write("<img src="+str+" />");
                        }
                    </script>
                    '''
                    # 将html测试报告添加到附件对象中
                    extra.append(pytest_html.extras.html(html))
                    # 判断是否执行js代码
                    if not insert_js_html:
                        extra.append(pytest_html.extras.html(script))
            elif config['项目运行设置']['REPORT_TYPE'] == 'ALLURE':
                import allure
                # 在步骤中插入一个图片
                with allure.step('添加失败截图0'):
                    #                  图片                名称        类型
                    allure.attach.file(BP.SCREENSHOT_PIC, "失败截图", allure.attachment_type.PNG)
    # 将测试报告的描述信息换位用例的描述信息
    report.extra = extra
    report.description = str(item.function.__doc__)


# 钩子函数
# items：要运行的用例集
def pytest_collection_modifyitems(session, config, items):
    '''运行用例前，将用例收集起来写入到文件中'''
    # 存放用例
    testcases = {}
    # 将items这个用例集中所有的用例遍历
    for item in items:
        case_class_name = '::'.join(item.nodeid.split("::")[0:2])
        case_name = item.nodeid.split('::')[-1]
        # 如果测试用例没有类,赋值空
        if not testcases.get(case_class_name, None):
            testcases[case_class_name] = {}
        # 如果有，将用例数据记录到testcases字典中
        if not testcases[case_class_name].get('comment', None):
            testcases[case_class_name][case_name] = item.function.__doc__
    tempcases_path = BP.TEMPCASES
    # 通过yaml文件写入方法，写入数据
    write_yaml(tempcases_path, testcases)


if __name__ == '__main__':
    driver()