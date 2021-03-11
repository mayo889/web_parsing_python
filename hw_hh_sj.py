from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd

def get_salary(text, site):
    if len(text) == 0:
        return None, None, None
    dash = '—' if site == 'sj' else '-'
    value = re.findall(r'\s(\D+)$', text)[0]
    if text.find(dash) != -1:
        first, second = text[:text.find(dash)], text[text.find(dash) + 1:]
        mini = int(''.join(re.findall(r'\d+', first)))
        maxi = int(''.join(re.findall(r'\d+', second)))
    elif text.startswith('от'):
        mini = int(''.join(re.findall(r'\d+', text)))
        maxi = None
    elif text.startswith('до'):
        mini = None
        maxi = int(''.join(re.findall(r'\d+', text)))
    else:
        mini, maxi,value = None, None, None
    return mini, maxi, value

def sj():
    # https://russia.superjob.ru/vacancy/search/?keywords=python&page=1
    main_link = 'https://russia.superjob.ru'
    page = 1
    while True:
        params = {'keywords': search_text,
                  'page': page
                  }
        response = requests.get(main_link + '/vacancy/search/', params=params, headers=headers)
        if response.ok:
            soup = bs(response.text, 'html.parser')
            vacancy_list = soup.findAll('div', {'class': 'Fo44F QiY08 LvoDO'})
            for vacancy in vacancy_list:
                vacancy_dict = {}

                title = vacancy.find('div', {'class': 'jNMYr GPKTZ _1tH7S'})
                position, salary = title.children
                vacancy_dict['link'] = main_link + position.find('a')['href']
                vacancy_dict['position'] = position.getText()
                vacancy_dict['salary'] = salary.getText()
                vacancy_dict['min_salary'], vacancy_dict['max_salary'], vacancy_dict['value'] = \
                    get_salary(salary.getText(), 'sj')

                company, city = title.nextSibling.children
                vacancy_dict['company'] = company.getText()
                city = city.find('span', {'class': 'clLH5'}).nextSibling.getText()
                vacancy_dict['city'] = re.findall(r'^[^, ]+', city)[0]

                vacancies.append(vacancy_dict)

            if soup.find('a', {'class': 'f-test-link-Dalshe'}) == None:
                break
            page += 1

def hh():
    # https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python&page=0
    main_link = 'https://hh.ru/search/vacancy'
    page = 0
    while True:
        params = {'L_is_autosearch': 'false',
                  'clusters': 'true',
                  'enable_snippets': 'true',
                  'text': search_text,
                  'page': page
                  }
        response = requests.get(main_link, params=params, headers=headers)
        if response.ok:
            soup = bs(response.text, 'html.parser')
            vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item'})
            for vacancy in vacancy_list:
                vacancy_dict = {}

                title = vacancy.find('div', {'class': 'vacancy-serp-item__row_header'})
                position, salary = title.children
                vacancy_dict['link'] = position.find('a')['href']
                vacancy_dict['position'] = position.getText()
                vacancy_dict['company'] = vacancy.find('div',
                                                       {'class': 'vacancy-serp-item__meta-info-company'}).getText()
                vacancy_dict['city'] = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).next
                vacancy_dict['city'] = re.findall(r'^[^, ]+', vacancy_dict['city'])[0]
                vacancy_dict['salary'] = salary.getText()
                vacancy_dict['min_salary'], vacancy_dict['max_salary'], vacancy_dict['value'] = \
                    get_salary(salary.getText(), 'hh')

                vacancies.append(vacancy_dict)

            if soup.find('a', {'class': 'HH-Pager-Controls-Next'}) == None:
                break
            page += 1

def main():
    global search_text, vacancies, headers
    search_text = input('Введите должность: ')
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    vacancies = []
    sj()
    hh()

    pd.set_option('display.max_columns', 7)
    pd.set_option('display.width', 2000)

    pd_vacancies = pd.DataFrame(vacancies)
    pd_vacancies.drop(columns='salary', inplace=True)
    print(pd_vacancies)

if __name__ == "__main__":
    main()
