from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lm_parser.spiders.LeroyMerlin import LeroymerlinSpider
from lm_parser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('Введите поисковый запрос по сайту: ')
    query = 'шуроповерт+dexter'
    process.crawl(LeroymerlinSpider, query=query)

    process.start()
