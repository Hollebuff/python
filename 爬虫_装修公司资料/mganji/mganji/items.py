# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MganjiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    company_url = scrapy.Field()
    city_name = scrapy.Field()
    company_add = scrapy.Field()
    company_name = scrapy.Field()
    linkman = scrapy.Field()
    tel = scrapy.Field()
    pass
