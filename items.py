# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
