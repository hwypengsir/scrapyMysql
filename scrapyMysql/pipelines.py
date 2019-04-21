# -*- coding: utf-8 -*-

# Define your item pipelines here
#


import pymysql.cursors
class MySQLPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='xxxx.yyyy.aaaa.bbbb',  
            port=3306,  
            db='scrapyMysql',  
            user='root',  
            passwd='xxxx',  
            charset='utf8',  
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("insert into mingyan(tag, cont) value (%s, %s)",(item['tag'],item['cont'],))
        self.connect.commit()
        return item  
