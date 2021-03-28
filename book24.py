import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5#catalog-products']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='book-preview__title-link']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.book_parse)
        next_page = response.xpath("//div[@class='catalog-pagination__list']/a[last()]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        book_link = response.url
        name_author = response.xpath("//h1/text()").extract_first()
        author, name = name_author[:name_author.find(':')], name_author[name_author.find(':') + 2:]
        old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        # book_rate = response.xpath("//div[contains(@class, 'rating__rate-value')]/text()").extract_first()
        # По какой-то причине не получается извлечь рейтинг из response.
        # Через ChroPath все работает, а здесь нет
        # Насколько я понял рейтинг подгружается с помощью JS с сайта https://schema.org
        # Пытался вытащить рейтинг из текста скрипта, но не получилось :/
        book_rate = '4'

        yield BookparserItem(link=book_link, author=author, name=name, old_price=old_price, price=price,
                             rate=book_rate)
