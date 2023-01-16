# encoding:utf-8
from Base.baseAutoWeb import WebBase
from Base.baseLogger import Logger
from ExtTools.dbbase import MysqlHelp

logger = Logger('web_article_page.py').getLogger()

class GJPage(WebBase):

    def __init__(self):
        super().__init__('02稿件管理元素信息.yaml')

    def add_article(self, title, content=''):
        """稿件新增"""
        logger.info('-----------------------------------------稿件新增开始-----------------------------------------')
        # 点击新增稿件按钮
        self.click('article/add_gj_btn')
        # 输入标题
        self.sendkeys('article/gj_title_input', title)
        # 切换iframe
        self.switch_iframe('article/add_iframe')
        # 输入内容
        self.sendkeys('article/gj_content_input', content)
        # 退出iframe
        self.switch_iframe_out()
        # 点击保存并返回
        self.click('article/gj_commit_btn')
        # 测试
        logger.info('-----------------------------------------稿件新增结束-----------------------------------------')



    def assert_add_article(self, title, content):
        """【断言】：稿件新增"""
        # 断言提示信息
        assert self.get_text('article/assert_hint') == "您的请求执行成功。", logger.error('【断言】：新增成功后提示信息错误!')
        logger.info('【断言】：新增成功后提示信息正确!')
        self.sendkeys('article/select_input', title)
        self.click('article/select_btn')
        # 断言新增稿件标题
        assert self.get_text('article/assert_add_title') == title, logger.error('【断言】：新增成功后，新增稿件标题错误!')
        logger.info('【断言】：新增成功后，新增稿件标题正确!')
        # 断言新增稿件状态
        assert self.get_text('article/assert_add_state') == '不批准', logger.error('【断言】：新增成功后，新增稿件状态错误!')
        logger.info('【断言】：新增成功后，新增稿件状态正确!')

        # 断言新增稿件数据库
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('SELECT title, content, approved FROM journalarticle WHERE title = "{}"'.format(title))
        print(res)
        assert title == res[0]['title'], logger.error('【断言】：新增稿件标题，数据库断言失败!')
        logger.info('【断言】：新增稿件标题，数据库断言成功!')
        assert content in res[0]['content'], logger.error('【断言】：新增稿件内容，数据库断言失败!')
        logger.info('【断言】：新增稿件内容，数据库断言成功!')
        assert res[0]['approved'] == 0, logger.error('【断言】：新增稿件状态，数据库断言失败!')
        logger.info('【断言】：新增稿件状态，数据库断言成功!')

        db.mysql_db_operate('DELETE FROM journalarticle WHERE title = "{}"'.format(title))


    def del_gj(self, title):
        """稿件删除"""
        logger.info('-----------------------------------------稿件删除开始-----------------------------------------')
        self.sendkeys('del_gj/select_input', title)
        self.click('del_gj/select_btn')
        # 选中复选框
        self.click('del_gj/check_box')
        # 点击删除按钮
        self.click('del_gj/delete_btn')
        # 点击弹窗中的确定按钮
        self.is_alert().accept()
        logger.info('-----------------------------------------稿件删除完成-----------------------------------------')

    def assert_del_gj(self, title):
        """【断言】：删除稿件页面测试"""
        assert self.get_text('del_gj/first_gj_title') != title, logger.error('【断言】：稿件未删除成功!')
        logger.info('【断言】：稿件删除成功!')

        self.sendkeys('del_gj/select_input', title)
        self.click('del_gj/select_btn')
        assert self.get_text('del_gj/assert_select_is_null') == '文章未被发现。', logger.error('【断言】：删除稿件后，依旧能查询到!')
        logger.info('【断言】：删除稿件后，查询为空')

    def assert_db_del_gj(self, title):
        """【断言】：删除断言数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select count(*) as "总数" from journalarticle where title = "{}"'.format(title))
        assert res[0]['总数'] == 0, logger.error('【断言】：数据库中未删除成功!')
        logger.info('【断言】：数据库中删除成功!')

    def alter_gj(self, alter_title, alter_content):
        """修改稿件"""
        logger.info('-----------------------------------------稿件修改开始-----------------------------------------')
        self.click('alter_gj/select_btn')
        # 点击第一条稿件的编号，进入修改页面
        self.click('alter_gj/first_gj_number')
        self.clear('alter_gj/gj_title_input')
        self.sendkeys('alter_gj/gj_title_input', alter_title)
        # 切换iframe
        self.switch_iframe('alter_gj/gj_content_iframe')
        self.clear('alter_gj/gj_content_input')
        self.sendkeys('alter_gj/gj_content_input', alter_content)
        # 切出iframe
        self.switch_iframe_out()
        # 点击保存
        self.click('alter_gj/gj_commit_btn')
        logger.info('-----------------------------------------稿件修改结束-----------------------------------------')

    def assert_alter_gj(self, title):
        """【断言】：修改稿件页面测试"""
        assert self.get_text('alter_gj/first_gj_title') == title, logger.info('【断言】：修改稿件标题失败!')
        logger.info('【断言】：修改标题成功!')
        assert self.get_text('alter_gj/first_gj_state') == '不批准', logger.info('【断言】：修改后稿件状态异常!')
        logger.info('【断言】：修改后稿件状态正常!')

    def assert_alter_db_gj(self, title, content):
        """【断言】：修改稿件数据库测试"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('SELECT title, content, approved FROM journalarticle WHERE title = "{}"'.format(title))
        assert title == res[0]['title'], logger.error('【断言】：新增稿件标题，数据库断言失败!')
        logger.info('【断言】：新增稿件标题，数据库断言成功!')
        assert content in res[0]['content'], logger.error('【断言】：新增稿件内容，数据库断言失败!')
        logger.info('【断言】：新增稿件内容，数据库断言成功!')
        assert res[0]['approved'] == 0, logger.error('【断言】：新增稿件状态，数据库断言失败!')
        logger.info('【断言】：新增稿件状态，数据库断言成功!')

        db.mysql_db_operate('DELETE FROM journalarticle WHERE title = "{}"'.format(title))

    def select_gj(self, title):
        """查询稿件"""
        logger.info('-----------------------------------------稿件查询开始-----------------------------------------')
        self.sendkeys('select_gj/select_input', title)
        self.click('select_gj/select_btn')
        logger.info('-----------------------------------------稿件查询结束-----------------------------------------')

    def assert_select_gj(self, title):
        """【断言】：查询稿件页面验证"""
        assert self.get_text('select_gj/first_gj_title') == title, logger.error('【断言】：稿件页面查询失败!')
        logger.info('【断言】：稿件页面查询成功!')

    def assert_select_gj_db(self, title):
        """【断言】：查询稿件数据库验证"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('SELECT * FROM journalarticle WHERE title = "{}" order by modifiedDate desc'.format(title))
        assert self.get_text('select_gj/first_gj_number') == res[0]['articleId'], logger.error('【断言】：稿件查询稿件页面编号与数据库中的编号不一致!')
        logger.info('【断言】：稿件查询稿件页面编号与数据库中的编号一致!')
        assert self.get_text('select_gj/first_gj_title') == res[0]['title'], logger.error('【断言】：稿件查询稿件页面标题与数据库中的标题不一致!')
        logger.info('【断言】：稿件查询稿件页面编号与数据库中的标题一致!')

        # 删除稿件
        db.mysql_db_operate('DELETE FROM journalarticle where title = "{}"'.format(title))


if __name__ == '__main__':
    from selenium import webdriver
    from Base.baseContainer import GlobalManager
    from PageObject.p02_web_gjxt.web_login_page import LoginPage
    driver = webdriver.Ie(r'E:\PyCharm2017\TestFramework_demo\Driver\IEDriverServer.exe')
    gm = GlobalManager()
    gm.set_value('driver', driver)
    lg = LoginPage()

    gj = GJPage()
    lg.login('test01', '1111')
    gj.add_article('查询测试', '测试测试')
    gj.add_article('查询测试', '测试测试')
    gj.add_article('查询测试', '测试测试')
    gj.select_gj('查询测试')
    gj.assert_select_gj('查询测试')
    gj.assert_select_gj_db('查询测试')

