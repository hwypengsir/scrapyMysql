# -*- coding: utf-8 -*-

# Define your item pipelines here
#


import pymysql.cursors
class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='104.160.39.49',  # 数据库地址
            port=3306,  # 数据库端口
            db='scrapyMysql',  # 数据库名
            user='root',  # 数据库用户名
            passwd='123456',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("insert into mingyan(tag, cont) value (%s, %s)",(item['tag'],item['cont'],))
        self.connect.commit()
        return item  
