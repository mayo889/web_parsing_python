# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


# Пришлось добавить еще один пайплайн для добавления данных в базу данных, потому что обработку item в LmParserPipeline
# необходимо делать до скачивания фото в LmPhotosPipeline, так как названия каталогов берутся из готового item
class LmMongoDBPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_merlin

    def process_item(self, item, spider):
        # Название коллекции формируется из имени запроса
        query = spider.start_urls[0]
        query = query[query.find('?q=') + 3:]
        collection = self.mongo_base[query]
        collection.insert_one(item)
        return item


class LmParserPipeline:
    def process_item(self, item, spider):
        # Склеиваем названия и значения характеристик товара. Старые поля удаляем
        if item['list_term'] and item['list_definition']:
            item['features'] = dict(zip(item['list_term'], item['list_definition']))
            del item['list_term']
            del item['list_definition']

        return item


class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        # главная папка - имя запроса
        query = info.spider.start_urls[0]
        query = query[query.find('?q=') + 3:]

        # следующая папка - код товара (последние цифры в ссылке)
        link = item['link']
        folder = link[link.rfind('-') + 1:-1]

        # имя файла - номер фотографии
        number = [i + 1 for i, link in enumerate(item['photos']) if request.url == link]

        return f'{query}/{folder}/{number[0]}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]

        return item
