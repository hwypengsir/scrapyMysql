

import scrapy
from scrapyMysql.items import ScrapymysqlItem  


class InputmysqlSpider(scrapy.Spider):
    name = "inputMysql"
    allowed_domains = ["lab.scrapyd.cn"]
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyan = response.css('div.quote')

        item = ScrapymysqlItem()  

        for v in mingyan:  
            item['cont'] = v.css('.text::text').extract_first()  
            tags = v.css('.tags .tag::text').extract()  
            item['tag'] = ','.join(tags)  
            yield item  

        next_page = response.css('li.next a::attr(href)').extract_first()  
        if next_page is not None:  
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  
