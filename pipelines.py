# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'book24':
            item['name'] = ' '.join(item['name'].replace('\n', '').split())
            item['price'] = ''.join(item['price'].split())
            if item['old_price']:
                item['old_price'] = ''.join(item['old_price'].split()[:-1])
        elif spider.name == 'labirint':
            if not item['price']:
                item['price'] = item['new_price']
                del item['new_price']

        item['old_price'], item['price'] = self.transform_prices(item['old_price'], item['price'])
        item['rate'] = float(item['rate'])
        item['currency'] = 'руб.'

        collection.insert_one(item)

        return item

    def transform_prices(self, old_price, price):
        if old_price:
            return int(old_price), int(price)
        else:
            return None, int(price)
