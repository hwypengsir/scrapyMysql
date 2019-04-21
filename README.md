��ν���ȡ����д�����ݿ⣿

���ݿ�����
```
create database  scrapyMysql;
use scrapyMysql;
CREATE TABLE `mingyan` (
  `tag` varchar(10) DEFAULT NULL,
  `cont` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
Զ�˷���������Զ�̵�¼
[����Զ�˵�¼](http://127.0.0.1/wp/?p=2051)

1.�����ڱ��ض�

`scrapy startproject scrapyMysql`

��Ŀ�ṹ
```
D:\SCRAPYMYSQL
��  scrapinghub.yml
��  scrapy.cfg
��  setup.py
��
����build
��  ����bdist.win-amd64
��  ����lib
��      ����scrapyMysql
��          ��  items.py
��          ��  middlewares.py
��          ��  pipelines.py
��          ��  settings.py
��          ��  __init__.py
��          ��
��          ����spiders
��                  inputMysql.py
��                  __init__.py
��
����project.egg-info
��      dependency_links.txt
��      entry_points.txt
��      PKG-INFO
��      SOURCES.txt
��      top_level.txt
��
����scrapyMysql
    ��  items.py
    ��  middlewares.py
    ��  pipelines.py
    ��  settings.py
    ��  __init__.py
    ��
    ����spiders
    ��  ��  inputMysql.py
    ��  ��  __init__.py
    ��  ��
    ��  ����__pycache__
    ��          inputMysql.cpython-37.pyc
    ��          __init__.cpython-37.pyc
    ��
    ����__pycache__
            items.cpython-37.pyc
            pipelines.cpython-37.pyc
            settings.cpython-37.pyc
            __init__.cpython-37.pyc

```

`cd  scrapyMysql`

�ֶ��ļ�
vi  scrapyMysql\items.py
```
import scrapy

class ScrapymysqlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tag = scrapy.Field()  # ��ǩ�ֶ�
    cont = scrapy.Field()  # ��������
    pass
```

�洢�ļ�

```
import pymysql.cursors
class MySQLPipeline(object):
    def __init__(self):
        # �������ݿ�
        self.connect = pymysql.connect(
            host='127.0.0.1',  # ���ݿ��ַ  
            port=3306,  # ���ݿ�˿�
            db='scrapyMysql',  # ���ݿ���
            user='root',  # ���ݿ��û���
            passwd='root',  # ���ݿ�����
            charset='utf8',  # ���뷽ʽ
            use_unicode=True)
        # ͨ��cursorִ����ɾ���
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into mingyan(tag, cont)
            value (%s, %s)""",  # ����python����mysql֪ʶ������Ϥ���
            (item['tag'],  # item���涨����ֶκͱ��ֶζ�Ӧ
             item['cont'],))
        # �ύsql���
        self.connect.commit()
        return item  # ����ʵ�ַ���
```

֩���ļ�

vi  scrapyMysql\spiders

```
# -*- coding: utf-8 -*-
import scrapy
from scrapyMysql.items import ScrapymysqlItem  # ����item


class InputmysqlSpider(scrapy.Spider):
    name = "inputMysql"
    allowed_domains = ["lab.scrapyd.cn"]
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')

        item = ScrapymysqlItem()  # ʵ����item��

        for v in mingyan:  # ѭ����ȡÿһ����������ģ��������ݡ����ߡ���ǩ
            item['cont'] = v.css('.text::text').extract_first()  # ��ȡ����
            tags = v.css('.tags .tag::text').extract()  # ��ȡ��ǩ
            item['tag'] = ','.join(tags)  # ����ת��Ϊ�ַ���
            yield item  # ��ȡ���������ύ��pipline����

        next_page = response.css('li.next a::attr(href)').extract_first()  # cssѡ������ȡ��һҳ����
        if next_page is not None:  # �ж��Ƿ������һҳ
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  # �ύ��parse����ץȡ��һҳ
```

ȫ������
vi  scrapyMysql\settings.py
```
BOT_NAME = 'scrapyMysql'
SPIDER_MODULES = ['scrapyMysql.spiders']
NEWSPIDER_MODULE = 'scrapyMysql.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'scrapyMysql.pipelines.MySQLPipeline': 300,
}
```
���У����ĸ�Ŀ¼�����У�d:\scrapyMysql��
scrapy crawl inputMysql

2.������scrapinghub
2.1 ����requirements.txt

```
D:\SCRAPYMYSQL
��  requirements.txt
��  scrapinghub.yml
��  scrapy.cfg
��  setup.py
��
����build
��  ����bdist.win-amd64
��  ����lib
��      ����scrapyMysql
��          ��  items.py
��          ��  middlewares.py
��          ��  pipelines.py
��          ��  settings.py
��          ��  __init__.py
��          ��
��          ����spiders
��                  inputMysql.py
��                  __init__.py
��
����project.egg-info
��      dependency_links.txt
��      entry_points.txt
��      PKG-INFO
��      SOURCES.txt
��      top_level.txt
��
����scrapyMysql
    ��  items.py
    ��  middlewares.py
    ��  pipelines.py
    ��  settings.py
    ��  __init__.py
    ��
    ����spiders
    ��  ��  inputMysql.py
    ��  ��  __init__.py
    ��  ��
    ��  ����__pycache__
    ��          inputMysql.cpython-37.p
    ��          __init__.cpython-37.pyc
    ��
    ����__pycache__
            items.cpython-37.pyc
            pipelines.cpython-37.pyc
            settings.cpython-37.pyc
            __init__.cpython-37.pyc
```
2.2 requirements.txt
vi  requirements.txt

`
PyMySQL==0.9.
`
�鿴���İ汾
pip freeze |grep  "pymysql"  

2.3 scrapinghub.yml
vi scrapinghub.yml
```
project: 380804
requirements:
    file: requirements.txt
```

����
```
$ pip install shub
$ shub login
API key: xxxx
$ shub deploy xxxx
```