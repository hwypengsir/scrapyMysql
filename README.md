如何将爬取内容写入数据库？

数据库设置
```
create database  scrapyMysql;
use scrapyMysql;
CREATE TABLE `mingyan` (
  `tag` varchar(10) DEFAULT NULL,
  `cont` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
远端服务器开启远程登录
[开启远端登录](http://127.0.0.1/wp/?p=2051)

1.部署在本地端

`scrapy startproject scrapyMysql`

项目结构
```
D:\SCRAPYMYSQL
│  scrapinghub.yml
│  scrapy.cfg
│  setup.py
│
├─build
│  ├─bdist.win-amd64
│  └─lib
│      └─scrapyMysql
│          │  items.py
│          │  middlewares.py
│          │  pipelines.py
│          │  settings.py
│          │  __init__.py
│          │
│          └─spiders
│                  inputMysql.py
│                  __init__.py
│
├─project.egg-info
│      dependency_links.txt
│      entry_points.txt
│      PKG-INFO
│      SOURCES.txt
│      top_level.txt
│
└─scrapyMysql
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  inputMysql.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          inputMysql.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    └─__pycache__
            items.cpython-37.pyc
            pipelines.cpython-37.pyc
            settings.cpython-37.pyc
            __init__.cpython-37.pyc

```

`cd  scrapyMysql`

字段文件
vi  scrapyMysql\items.py
```
import scrapy

class ScrapymysqlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tag = scrapy.Field()  # 标签字段
    cont = scrapy.Field()  # 名言内容
    pass
```

存储文件

```
import pymysql.cursors
class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址  
            port=3306,  # 数据库端口
            db='scrapyMysql',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into mingyan(tag, cont)
            value (%s, %s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['tag'],  # item里面定义的字段和表字段对应
             item['cont'],))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回
```

蜘蛛文件

vi  scrapyMysql\spiders

```
# -*- coding: utf-8 -*-
import scrapy
from scrapyMysql.items import ScrapymysqlItem  # 引入item


class InputmysqlSpider(scrapy.Spider):
    name = "inputMysql"
    allowed_domains = ["lab.scrapyd.cn"]
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')

        item = ScrapymysqlItem()  # 实例化item类

        for v in mingyan:  # 循环获取每一条名言里面的：名言内容、作者、标签
            item['cont'] = v.css('.text::text').extract_first()  # 提取名言
            tags = v.css('.tags .tag::text').extract()  # 提取标签
            item['tag'] = ','.join(tags)  # 数组转换为字符串
            yield item  # 把取到的数据提交给pipline处理

        next_page = response.css('li.next a::attr(href)').extract_first()  # css选择器提取下一页链接
        if next_page is not None:  # 判断是否存在下一页
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  # 提交给parse继续抓取下一页
```

全局配置
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
运行（在哪个目录中运行？d:\scrapyMysql）
scrapy crawl inputMysql

2.部署在scrapinghub
2.1 增加requirements.txt

```
D:\SCRAPYMYSQL
│  requirements.txt
│  scrapinghub.yml
│  scrapy.cfg
│  setup.py
│
├─build
│  ├─bdist.win-amd64
│  └─lib
│      └─scrapyMysql
│          │  items.py
│          │  middlewares.py
│          │  pipelines.py
│          │  settings.py
│          │  __init__.py
│          │
│          └─spiders
│                  inputMysql.py
│                  __init__.py
│
├─project.egg-info
│      dependency_links.txt
│      entry_points.txt
│      PKG-INFO
│      SOURCES.txt
│      top_level.txt
│
└─scrapyMysql
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  inputMysql.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          inputMysql.cpython-37.p
    │          __init__.cpython-37.pyc
    │
    └─__pycache__
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
查看包的版本
pip freeze |grep  "pymysql"  

2.3 scrapinghub.yml
vi scrapinghub.yml
```
project: 380804
requirements:
    file: requirements.txt
```

部署
```
$ pip install shub
$ shub login
API key: xxxx
$ shub deploy xxxx
```
