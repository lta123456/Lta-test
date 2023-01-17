# encoding:utf-8
import sys
import os
import time
# 获取项目根路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根路径添加到环境变量中去
# 因为在运行项目的时候，有可能不是使用pycharm运行，比如cmd
# 如果项目根路径没有添加到环境变量中，则不能使用import导包
sys.path.append(PROJECT_ROOT)
import pytest
from Base.BasePath import BasePath as BP
from Base.utils import read_config_ini, file_all_del
from Base.baseContainer import GlobalManager
from Base.baseSendEmail import HandleEmail

config = read_config_ini(BP.Config_File)
gm = GlobalManager()
gm.set_value('CONFIG_INFO', config)
gm.set_value('DATA_DRIVER_PATH', os.path.join(BP.Data_Driver_Dir, config['项目运行设置']['DATA_DRIVER_TYPE']))

def run_main():
    '''运行入口'''
    run_config = gm.get_value('CONFIG_INFO')['项目运行设置']

    if run_config['TEST_CLASS']:
        test_case = os.path.join(BP.TEST_SUIT_DIR, run_config['TEST_PROJECT'], run_config['TEST_CASE_NAME']) + '::' + run_config['TEST_CLASS']
    else:
        if run_config['TEST_CASE_NAME']:
            test_case = os.path.join(BP.TEST_SUIT_DIR, run_config['TEST_PROJECT'], run_config['TEST_CASE_NAME'])
        else:
            test_case = os.path.join(BP.TEST_SUIT_DIR, run_config['TEST_PROJECT'])

    # 获取用例的位置
    if run_config['REPORT_TYPE'] == 'ALLURE':
        # 命令行生产allur测试报告数据
        pytest.main(['-v', '--alluredir={}'.format(BP.Allure_Result), test_case])
        # 生产测试报告
        os.system('allure generate {} -o {} --clean'.format(BP.Allure_Result, BP.Allure_Report))
        # 清空测试报告数据文件夹里的文件
        time.sleep(5)
        file_all_del(BP.Allure_Result)
    elif run_config['REPORT_TYPE'] == 'HTML':
        # html报告路径
        report_path = os.path.join(BP.HTML_Dir, 'auto_reports.html')
        # 命令行执行测试用例并创建测试报告
        pytest.main(['-v', '--html={}'.format(report_path), '--self-contained-html', test_case])
    elif run_config['REPORT_TYPE'] == 'XML':
        # xml报告路径
        report_path = os.path.join(BP.XML_Dir, 'auto_reports.xml')
        # 命令行执行测试用例并创建测试报告
        pytest.main(['-v', '--junitxml={}'.format(report_path), test_case])
    else:
        print('暂不支持此报告类型：{}'.format(run_config['REPORT_TYPE']))
    # 邮件发送
    if run_config['IS_EMAIL'] == 'yes':
        # 实例化邮件发送类
        el = HandleEmail()
        # 指定发送邮件的正文
        text = '本邮件由系统自动发出，无需回复！\n各位同事，大家好，以下附件为本次测试报告!'
        # 通过邮件发送的方法发送邮件
        el.send_public_email(text=text, filetpye=run_config['REPORT_TYPE'])
        # 发送成功后，打印
        print('邮件发送成功，测试报告类型：{}'.format(run_config['REPORT_TYPE']))
    else:
        print('不发送邮件')

if __name__ == '__main__':
    run_main()
