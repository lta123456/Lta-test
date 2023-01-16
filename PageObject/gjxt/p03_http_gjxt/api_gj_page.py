# encoding: utf-8
import re
import time

from ExtTools.dbbase import MysqlHelp
from Base.baseAutoHttp import ApiBase
from Base.baseLogger import Logger
from PageObject.gjxt.p03_http_gjxt.api_login_page import LoginPage

logger = Logger('api_gj_page.py').getLogger()


class ApiGj(ApiBase):

    def __init__(self):
        super().__init__('02稿件管理接口信息.yaml')

    def add_gj(self, title, content):
        """稿件新增"""
        change_data = {
            "_15_title": title,
            "_15_content": content
        }
        res = self.request_base('add_gj_api', change_data=change_data)
        return res.text

    def assert_add_gj(self, title):
        """【断言】：稿件新增页面断言"""
        res_info = self.select_gj(title)
        assert res_info[1] == title, logger.error('【断言】：稿件新增页面断言失败! 名称错误!')
        assert res_info[3] == '不批准', logger.error('【断言】：稿件新增页面断言失败! 状态错误!')
        logger.info('【断言】：稿件系统新增稿件页面断言成功!')

    def assert_add_gj_db(self, title, content):
        """【断言】：稿件新增数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select title, content, approved from journalarticle order by modifiedDate desc')
        assert res[0]['title'] == title, logger.error('【断言】：稿件新增数据库断言失败! 稿件名称错误!')
        assert re.findall('<!\[CDATA\[(.*?)]]>', res[0]['content'])[0] == content, logger.error('【断言】：稿件新增数据库断言失败! 稿件内容错误!')
        assert res[0]['approved'] == 0, logger.error('【断言】：稿件新增数据库断言失败! 稿件状态错误!')
        print(res[0])
        logger.info('【断言】：稿件新增数据库断言成功!')

        db.mysql_db_operate('delete from journalarticle where title = "{}"'.format(title))
        logger.info('【断言】：稿件新增测试用例数据清除成功!')

    def del_gj(self, title=''):
        """删除稿件"""
        self.id = self.select_gj(title)[0]
        change_data = {
            '_15_deleteArticleIds': self.id+'_version_1.0',
            '_15_rowIds': self.id+'_version_1.0',
        }
        res = self.request_base('del_gj', change_data=change_data)
        return res.text

    def assert_del_gj(self):
        """【断言】：删除稿件"""
        assert self.select_gj(self.id) == [], logger.error('【断言】：稿件删除页面断言失败!')
        logger.info('【断言】：稿件删除页面断言成功!')

    def assert_del_gj_db(self):
        """【断言】：删除稿件数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select count(*) as "总数" from journalarticle where articleId = "{}"'.format(self.id))[0]
        assert res['总数'] == 0, logger.error('【断言】：稿件删除数据库断言失败!')
        logger.info('【断言】：稿件删除数据库断言成功!')

    def alter_gj(self, old_title, new_title, content):
        """修改稿件"""
        self.id = self.select_gj(old_title)[0]
        change_data = {
            '_15_articleId': self.id,
            '_15_content': content,
            '_15_deleteArticleIds': self.id+'_version_1.0',
            '_15_expireArticleIds': self.id+'_version_1.0',
            '_15_title': new_title
        }
        res = self.request_base('alter_gj', change_data=change_data)
        return res.text

    def assert_alter_gj(self, title):
        """【断言】：修改稿件页面断言"""
        res = self.select_gj(self.id)
        assert res[1] == title, logger.error('【断言】：修改稿件页面断言失败! 名称错误')
        assert res[3] == '不批准', logger.error('【断言】：修改稿件页面断言失败! 状态错误')
        logger.info('修改稿件页面断言成功!')

    def assert_alter_gj_db(self, title, content):
        """【断言】：修改稿件数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select title, content, approved from journalarticle order by modifiedDate desc')
        assert res[0]['title'] == title, logger.error('【断言】：稿件新增数据库断言失败! 稿件名称错误!')
        assert re.findall('<!\[CDATA\[(.*?)]]>', res[0]['content'])[0] == content, logger.error('【断言】：稿件新增数据库断言失败! 稿件内容错误!')
        assert res[0]['approved'] == 0, logger.error('【断言】：稿件新增数据库断言失败! 稿件状态错误!')
        logger.info('【断言】：稿件新增数据库断言成功!')

        db.mysql_db_operate('delete from journalarticle where title = "{}"'.format(title))
        logger.info('【断言】：稿件新增测试用例数据清除成功!')

    def fff(self, aaa):
        print(aaa)

    def select_gj(self, title=''):
        """查询稿件"""
        change_data = {
            "title": title
        }
        res = self.request_base('select_api', change_data=change_data)
        re_info = re.findall('_15_version=1.0">(.*?)</a>', res.text)[:7]
        return re_info

    def assert_select_gj(self, res, title):
        """【断言】：查询稿件"""
        assert res[1] == title, logger.error('【断言】：稿件查询页面断言失败!')
        logger.info('【断言】：稿件查询页面断言成功!')

    def assert_select_gj_db(self, title):
        """【断言】：查询稿件数据库断言"""
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(
            host=dbInfo['host'],
            user=dbInfo['user'],
            password=dbInfo['psw'],
            port=dbInfo['port'],
            database=dbInfo['database']
        )
        res = db.mysql_db_select('select count(*) as "总数" from journalarticle where title = "{}"'.format(title))
        assert res[0]['总数'] >= 1, logger.error('稿件查询数据库断言失败!')
        logger.info('稿件查询数据库断言成功!')

        db.mysql_db_operate('delete from journalarticle where title = "{}"'.format(title))
        logger.info('稿件清除成功!')






if __name__ == '__main__':
    lg = LoginPage()
    a = ApiGj()
    lg.login('test01', '1111')
    a.add_gj('查询', 'eeee')
    res = a.select_gj('查询')
    a.assert_select_gj(res, '查询')
    time.sleep(10)
    a.assert_select_gj_db('查询')









