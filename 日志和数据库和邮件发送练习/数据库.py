# encoding: utf-8
import pymysql


class MySQL:

    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = int(port)
        self.database = database
        self.connection = None

    def create_connection(self):
        """创建连接"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )