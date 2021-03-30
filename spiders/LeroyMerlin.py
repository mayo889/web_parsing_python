import scrapy
from scrapy.http import HtmlResponse
from lm_parser.items import LmParserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'LeroyMerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f"https://leroymerlin.ru/search/?q={query}"]

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='plp-item__info__title']")
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath("//div[@view-type='primary']//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response:HtmlResponse):
        loader = ItemLoader(item=LmParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_value('link', response.url)

        # в теге picture хранятся ссылки на фото в разных разрешениях для различных устройств
        # выберем разрешение 1200x1200
        loader.add_xpath('photos', "//picture[@slot='pictures']/img/@src")

        # отдельно сохраним названия и значения характеристик товара
        loader.add_xpath('list_term', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('list_definition', "//dd[@class='def-list__definition']/text()")

        yield loader.load_item()
