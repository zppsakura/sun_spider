# -*- coding: utf-8 -*-
import scrapy
from sun_spider.items import SunSpiderItem


class SunspiderSpider(scrapy.Spider):
    name = 'sunSpider'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/report?page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        links = response.xpath('//td[@class="txt18"]/a[1]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

        if self.offset <= 150:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        print(response)
        item = SunSpiderItem()
        url = response.url
        title = response.xpath('//span[@class="niae2_top"]/text()').extract()[0]
        content = ''.join(response.xpath('//td[@class="txt16_3"]/text()').extract()).strip().replace("\t", "").replace("\xa0", "")
        if content == '':
            content = ''.join(response.xpath('//div[@class="contentext"]/text()').extract()).strip().replace("\t", "").replace("\xa0", "")
        item['url'] = url
        item['title'] = title.strip()
        item['content'] = content
        yield item








