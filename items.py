# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    address = scrapy.Field()
    rent = scrapy.Field()
    rentWay = scrapy.Field()
    toward = scrapy.Field()
    feature = scrapy.Field()
    acreage = scrapy.Field()
    layout = scrapy.Field()
    introduction = scrapy.Field()
    picture = scrapy.Field()