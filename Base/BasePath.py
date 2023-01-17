# encoding:utf-8
import os


class BasePath:
    # 获取项目的根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 配置文件夹的目录
    Config_Dir = os.path.join(project_root, 'Config')
    # 配置文件的目录
    Config_File = os.path.join(Config_Dir, 'config.ini')
    # 数据文件的目录
    Data_Dir = os.path.join(project_root, 'Data')
    Data_Driver_Dir = os.path.join(Data_Dir, 'DataDriver')
    Data_Element_Dir = os.path.join(Data_Dir, 'DataElement')
    Data_Temp_Dir = os.path.join(Data_Dir, 'Temp')
    # JDBC方式操作数据库文件
    EXTS_PATH = os.path.join(project_root, 'ExtTools')
    # 错误截图文件夹
    SCREENSHOT_Dir = os.path.join(Data_Temp_Dir, 'Scrennshots')
    # 错误截图名称
    SCREENSHOT_PIC = os.path.join(SCREENSHOT_Dir, 'error_pic.png')
    # 图形化勾选执行运行测试用例的文件
    TESTCASES = os.path.join(Data_Temp_Dir, 'testcases.yaml')
    # 图形化所有用例存放的文件
    TEMPCASES = os.path.join(Data_Temp_Dir, 'tempcases.yaml')
    # 浏览器驱动的路径
    Driver_Dir = os.path.join(project_root, 'Driver')
    # 日志文件的路径
    Log_Dir = os.path.join(project_root, 'Log')
    # 测试报告
    Allure_Dir = os.path.join(project_root, 'Reports', 'ALLURE')
    Allure_Report = os.path.join(Allure_Dir, 'Report')
    Allure_Result = os.path.join(Allure_Dir, 'Result')
    HTML_Dir = os.path.join(project_root, 'Reports', 'HTML')
    XML_Dir = os.path.join(project_root, 'Reports', 'XML')
    # 测试用例路径
    TEST_SUIT_DIR = os.path.join(project_root, 'TestSuits')


if __name__ == '__main__':
    print(BasePath.Config_File)
