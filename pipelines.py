# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class InstaParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        collection = self.mongo_base[item['username']]
        collection.insert_one(item)

        return item


class InstaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['follow_pic_url']:
            try:
                yield scrapy.Request(item['follow_pic_url'])
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Первая папка это username пользователя, подписчиков и подписки которого ищем
        username = item['username']
        # Вторая папка это подписчики или подписки
        status = item['status']
        # Имя файла это имя подписчика или подписки
        name = item['follow_username']
        return f'{username}/{status}/{name}.jpg'

    def item_completed(self, results, item, info):
        if results and results[0][0]:
            item['follow_pic_url'] = results[0][1]

        return item
