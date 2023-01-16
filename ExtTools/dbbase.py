# encoding:utf-8

import pymysql
import sqlite3

class MysqlHelp:
    """MySQL数据库封装类"""

    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.db = database
        self.connection = None

    def create_connection(self):
        """创建连接"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port,
            database=self.db,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def mysql_db_select(self, sql):
        """查"""
        try:
            # 执行上面的方法，创建连接
            self.create_connection()
            with self.connection.cursor() as cursor:
                # 执行sql语句
                count = cursor.execute(sql)
                print('受影响条数：{}'.format(count))
                # 返回查询的结果
                result_set = cursor.fetchall()
            return result_set
        except Exception as e:
            print('查询错误...', e)
        finally:
            self.connection.close()

    def mysql_db_operate(self, sql):
        """增删改"""
        try:
            # 创建连接
            self.create_connection()
            # 创建游标
            with self.connection.cursor() as cursor:
                # 执行sql语句
                count = cursor.execute(sql)
                print('受影响条数：{}'.format(count))
                # 提交事务
                self.connection.commit()
        except Exception as e:
            # 事务回滚
            self.connection.rollback()
        finally:
            self.connection.close()

class Sqlite3Tools:
    """Sqlite3数据库封装类"""

    def __init__(self, database):
        self.database = database
        self.connection = None

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_connection(self):
        """创建连接"""
        self.connection = sqlite3.connect(self.database)
        # 返回的数据是列表套元组的形式，通过上面的方法dict_factory，将元组转化为字典
        self.connection.row_factory = self.dict_factory

    def sqlite3_db_select(self, sql):
        """数据库查询"""
        try:
            # 创建连接
            self.create_connection()
            # 创建游标并执行sql语句
            cur = self.connection.cursor().execute(sql)
            # 获取查询结果
            result_set = cur.fetchall()
            return result_set
        except Exception as e:
            print('查询错误...', e)
        finally:
            self.connection.close()

    def sqlite3_db_operate(self, sql):
        """增删改"""
        try:
            # 创建连接
            self.create_connection()
            # 创建游标并执行sql语句
            self.connection.cursor().execute(sql)
            # 提交事务
            self.connection.commit()
        except Exception as e:
            # 事务回滚
            self.connection.rollback()
            print(e)
        finally:
            # 关闭连接
            self.connection.close()




if __name__ == '__main__':
    from Base.BasePath import BasePath as BP
    from Base.utils import read_config_ini
    config = read_config_ini(BP.Config_File)['数据库连接配置']
    mysql = MysqlHelp(
        host=config['host'],
        user=config['user'],
        password=config['psw'],
        port=3306,
        database=config['database']
    )
    sql = 'select * from user'
    print(mysql.mysql_db_select(sql))


