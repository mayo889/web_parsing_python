import requests
from lxml import html
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient


def transform_text(text):
    return text.replace('\xa0', ' ')


def lenta():
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("//section[contains(@class, 'b-top7-for-main')]/div/div[contains(@class, 'item')]")
    flag = False
    for item in items:
        news = {}

        if not flag:
            flag = True
            link = item.xpath("./h2/a/@href")[0]
            date = item.xpath("./h2/a/time/@title")[0]
            text = item.xpath("./h2/a/text()")[0]
        else:
            link = item.xpath("./a/@href")[0]
            date = item.xpath("./a/time/@title")[0]
            text = item.xpath("./a/text()")[0]

        news['source'] = 'lenta.ru'
        news['text'] = transform_text(text)
        news['date'] = date
        news['link'] = main_link + link
        all_news.append(news)


def yandex():
    main_link = 'https://yandex.ru/news'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[contains(@class, 'news-top-flexible-stories')]"
                      "/div[contains( @ class, 'mg-grid__col')] / article")
    date = datetime.today().strftime('%Y-%m-%d')
    for item in items:
        news = {}

        link = item.xpath(".//a[@class='mg-card__link']/@href")[0]
        text = item.xpath(".//h2/text()")[0]
        source = item.xpath(".//a[@class='mg-card__source-link']/text()")[0]

        news['source'] = source
        news['text'] = transform_text(text)
        news['date'] = date
        news['link'] = link
        all_news.append(news)


def mail():
    main_link = 'https://news.mail.ru/'
    response = requests.get(main_link, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath("//div[@class='js-module']/ul/li[@class='list__item']")
    for item in items:
        news = {}
        link = item.xpath("./a/@href")[0]
        text = item.xpath("./a/text()")[0]

        response_2 = requests.get(link, headers=header)
        dom_2 = html.fromstring(response_2.text)
        items = dom_2.xpath("//div[contains(@class, 'breadcrumbs')]")
        date = items[0].xpath(".//span[contains(@class, 'breadcrumbs__text')]/@datetime")[0][:10]
        source = items[0].xpath(".//span[@class='link__text']/text()")[0]

        news['source'] = source
        news['text'] = transform_text(text)
        news['date'] = date
        news['link'] = link
        all_news.append(news)


def mongodb(result=False):
    client = MongoClient('localhost', 27017)
    db = client["news_from_net"]
    news = db.news
    news.delete_many({})
    news.insert_many(all_news)

    if result:
        for item in news.find({}):
            pprint(item)


def main():
    global header, all_news

    all_news = []
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    lenta()
    yandex()
    mail()

    mongodb(result=True)


if __name__ == "__main__":
    main()
