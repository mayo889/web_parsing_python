# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    status = scrapy.Field()
    follow_id = scrapy.Field()
    follow_username = scrapy.Field()
    follow_pic_url = scrapy.Field()
    # follow_data = scrapy.Field()
