# encoding: utf-8
import jaydebeapi
import os
from Base.BasePath import BasePath as BP
from Base.baseYaml import read_yaml

tools_path = os.path.join(BP.EXTS_PATH, 'JDBC')

class JDBC:

    def __init__(self, dbtype, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.database = database
        self.url, self.driver, self.jar_path = self.get_db_info(dbtype)
        self.connection = None

    def get_db_info(self, dbtype):
        """获取url"""
        dbinfo = read_yaml(os.path.join(tools_path, 'dbInfo.yaml'))
        url = None
        if dbtype == 'sqlite':
            url = dbinfo[dbtype]['url模板'].format(dbPATH=self.database)
        else:
            if dbtype in dbinfo.keys():
                url = dbinfo[dbtype]['url模板'].format(IP=self.host, PORT=self.port, DATABASE=self.database)
            else:
                print('暂不支持此数据库!!!')
        driverClass = dbinfo[dbtype]['类名']
        jar_path = os.path.join(tools_path, 'jarfile', dbinfo[dbtype]['添加文件'])
        return url, driverClass, jar_path

    def create_connection(self):
        """创建链接"""
        self.connection = jaydebeapi.connect(
            jclassname=self.driver,
            url=self.url,
            driver_args=[self.user, self.password],
            jars=self.jar_path
        )

    def select(self, sql):
        """查"""
        try:
            self.create_connection()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
                print('查询到的条数：{}'.format(len(res)))
            return res
        except Exception as e:
            print('查询失败!!!', e)
        finally:
            self.connection.close()

    def operate(self, sql):
        """增删改"""
        try:
            self.create_connection()
            self.connection.jconn.setAutoCommit(False)
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print('操作失败!!!', e)
            self.connection.rollback()
        finally:
            self.connection.close()



if __name__ == '__main__':
    j = JDBC(
        dbtype='mysql',
        host='localhost',
        user='root',
        password='l2002072800.',
        port='3306',
        database='test01'
    )
    j.operate('update test01 set name = "test03" where id in("13")')
    print(j.select('select * from test01'))