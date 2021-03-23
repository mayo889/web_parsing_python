from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pprint import pprint
from pymongo import MongoClient


# Убирает лишние пробелы в тексте
def transform_text(text):
    return ' '.join(text.replace('\n', '').split())


def authorization(login, password):
    elem = driver.find_element_by_name('login')
    elem.send_keys(login)
    elem.send_keys(Keys.ENTER)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'second-button'))
    )
    elem = driver.find_element_by_name('password')
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)


def get_letters_links():
    check = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'js-letter-list-item'))
    )

    links = set()
    check = []
    while True:
        letters = driver.find_elements_by_class_name('js-letter-list-item')
        links.update(set([letter.get_attribute('href') for letter in letters]))

        check = driver.find_elements_by_class_name('list-letter-spinner')
        if not check:
            actions = ActionChains(driver)
            actions.move_to_element(letters[-1])
            actions.perform()
        else:
            break

        time.sleep(1)

    return links


def parsing_letters(links):
    letters = []
    for link in links:
        letter = {}
        driver.get(link)
        topic = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h2'))
        )
        topic = topic.text
        # Классов letter-contact в письме 2 для отправителя и получателя, поэтому можно искать единственный элемент для
        # первого вхождения, так как отправитель всегда идет первый
        sender = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        date = driver.find_element_by_class_name('letter__date').text
        text = driver.find_element_by_class_name('letter__body').text

        letter['topic'] = topic
        letter['sender'] = sender
        letter['date'] = date
        letter['text'] = transform_text(text)

        letters.append(letter)

    return letters


def fill_db(letters_, result=False):
    client = MongoClient('localhost', 27017)
    db = client["letters_from_mail_ru"]
    letters = db.letters
    letters.delete_many({})
    letters.insert_many(letters_)

    if result:
        for letter in letters.find({}):
            pprint(letter)


def main():
    global driver

    with open('login.txt') as f:
        login = f.readline()
        password = f.readline()

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')

    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)
    driver.get("https://mail.ru/")

    authorization(login, password)

    links = get_letters_links()
    print(f"{'*' * 25}\nВсего писем найдено: {len(links)}\n{'*' * 25}\n")

    letters = parsing_letters(links)

    fill_db(letters, result=True)


if __name__ == "__main__":
    main()
