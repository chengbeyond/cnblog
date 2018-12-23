# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime


class CnblogsPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.today()
        item["spider"] = spider.name
        return item
