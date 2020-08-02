# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SriAnnualItem(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()

class SriMidItem(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()