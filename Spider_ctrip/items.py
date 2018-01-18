# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderCtripItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hotel_id = scrapy.Field()
    hotel_name = scrapy.Field()
    pass


class SpiderHotelCommentItem(scrapy.Item):
    comment = scrapy.Field()
    pass
