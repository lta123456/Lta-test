# encoding: utf-8
import os
import jaydebeapi
from Base.BasePath import BasePath as BP
from Base.baseYaml import read_yaml

tools_path = os.path.join(BP.EXTS_PATH, 'JDBC')

class JdbcBase:
    """通过JBDC方式连接各种数据库"""

    def __init__(self, dbtype, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.database = database
        self.url, self.driver, self.jarFile = self.get_db_info(dbtype)
        self.connection = None

    def create_connection(self):
        """创建连接"""
        self.connection = jaydebeapi.connect(self.driver, self.url, [self.user, self.password], self.jarFile)

    def get_db_info(self, dbtype):
        dbinfo = read_yaml(os.path.join(tools_path, 'dbInfo.yaml'))
        url = None
        if dbtype == 'sqlite':
            url = dbinfo[dbtype]['url模板'].format(dbPATH=self.database)
        else:
            # 如果传入的数据库名称存在于yaml文件中的数据库
            if dbtype in dbinfo.keys():
                # 设置url
                url = dbinfo[dbtype]['url模板'].format(IP=self.host, PORT=self.port, DATABASE=self.database)
            else:
                print("暂不支持此数据库：{}".format(dbtype))
        # 获取yaml文件中的类名
        driverClass = dbinfo[dbtype]['类名']
        # 获取jar文件路径
        jarName = os.path.join(tools_path, 'jarfile', dbinfo[dbtype]['添加文件'])
        return url, driverClass, jarName

    def select(self, sql):
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


if __name__ == '__main__':
    j = JdbcBase(
        dbtype='mysql',
        host='localhost',
        user='root',
        password='l2002072800.',
        port='3306',
        database='test01'
    )
    print(j.select('select * from test01'))
