# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def transform_price(price):
    return int(''.join(price.split()))


def transform_definition(text):
    text = ' '.join(text.replace('\n', '').split())
    try:
        return float(text)
    except Exception:
        return text


class LmParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(transform_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    list_term = scrapy.Field()
    list_definition = scrapy.Field(input_processor=MapCompose(transform_definition))
    features = scrapy.Field()
