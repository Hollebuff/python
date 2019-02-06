# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhuangyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    company_url = scrapy.Field()
    city_name = scrapy.Field()
    city_md = scrapy.Field()
    company_name = scrapy.Field()
    company_add = scrapy.Field()
    tel = scrapy.Field()
    pass


