# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class SpiderCtripPipeline(object):
    def process_item(self, item, spider):
        with open('save.json', 'a') as f:
            f.write(json.dumps(dict(item)))
        return item
