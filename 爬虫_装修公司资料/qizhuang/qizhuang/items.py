# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QizhuangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    company_url = scrapy.Field()
    city_name = scrapy.Field()
    city_md = scrapy.Field()
    company_name = scrapy.Field()
    company_add = scrapy.Field()
    tel = scrapy.Field()
    phone = scrapy.Field()
    # 1.城市
    # 2.市辖区（宝安区）
    # 3.公司名
    # 4.公司地址
    # 5.联系人
    # 6.联系电话
    # 7.手机
    # pass
