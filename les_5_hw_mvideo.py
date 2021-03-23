from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
import json
from pymongo import MongoClient


def transform_info(info):
    info.replace('\n', '').replace('\t', '')
    return json.loads(info)


def parsing():
    gallery = driver.find_elements_by_class_name('gallery-layout_products')
    gallery = gallery[0]

    items = gallery.find_elements_by_class_name('gallery-list-item')
    prev_len, cur_len = -1, 0
    while prev_len != cur_len:
        time.sleep(2)
        items = gallery.find_elements_by_class_name('gallery-list-item')
        rels = [int(item.get_attribute('rel')) for item in items]
        prev_len, cur_len = cur_len, len(rels)
        button = gallery.find_element_by_class_name('next-btn')
        button.click()

    all_info = []
    for item in items:
        info = item.find_element_by_class_name('fl-product-tile-title__link').get_attribute('data-product-info')
        all_info.append(transform_info(info))

    return all_info


def fill_db(all_info, result=False):
    client = MongoClient('localhost', 27017)
    db = client["products_from_mvideo"]
    products = db.products
    products.delete_many({})
    products.insert_many(all_info)

    if result:
        for product in products.find({}):
            pprint(product)


def main():
    global driver

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)
    driver.get("https://www.mvideo.ru/")

    all_info = parsing()
    print(f"{'*' * 25}\nВсего найдено товаров: {len(all_info)}\n{'*' * 25}\n")

    fill_db(all_info, result=True)


if __name__ == "__main__":
    main()
