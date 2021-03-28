import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        book_link = response.url
        name_author = response.xpath("//h1/text()").extract_first()
        author, name = name_author[:name_author.find(':')], name_author[name_author.find(':') + 2:]
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        book_rate = response.xpath("//div[@id='rate']/text()").extract_first()

        yield BookparserItem(link=book_link, author=author, name=name, old_price=old_price, new_price=new_price,
                             price=price, rate=book_rate)
