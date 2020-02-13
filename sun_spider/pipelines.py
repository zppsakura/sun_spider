# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from sun_spider.items import SunSpiderItem

class SunSpiderPipeline(object):
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod  # 初始化crawler的方法,scrapy创建spider的时候会调用，获取settings中的参数，并赋值给 __init__ 函数
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.sundb = self.client['sun']
        self.listcol = self.sundb['list']


    def process_item(self, item, spider):
        if isinstance(item, SunSpiderItem):
            self.listcol.update_one({'url': item['url'], 'title': item['title'], 'content': item['content']}, {
                '$set': dict(item)}, True)
        return item

    def close_spider(self, spider):
        self.client.close()
