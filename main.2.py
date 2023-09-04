import requests
from bs4 import BeautifulSoup
import fake_headers
import json

headers_gen = fake_headers.Headers(browser='chrome', os='win')
parsing = int(input('Сколько страниц парсить? '))
for page in range(parsing):
    response = requests.get(
        f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page"
        f"={page}", headers=headers_gen.generate())
    html_data = response.text
    hh_main = BeautifulSoup(html_data, 'lxml')
    job_list = hh_main.find('div', id='a11y-main-content')
    city = job_list.find_all_next('div', class_='bloko-text')
    vacancy = job_list.find_all('div',
                                class_='vacancy-serp-item-body__main-info')

    teg_a = []
    teg_span = []
    teg_div = []
    for item in vacancy:
        teg_a.append(item.find('a', class_='serp-item__title'))
        teg_span.append(item.find('span', class_='bloko-header-section-2'))
        teg_div.append(item.find('div', class_='bloko-text'))

    list_link = []
    list_salary = []
    list_company = []
    list_city = []
    for a in teg_a:
        list_link.append(a['href'])
    for span in teg_span:
        if span is None:
            list_salary.append('Не указано')
        elif span.text[-1] == '$':
            list_salary.append(span.text.replace('\u202f', ''))
        else:
            list_salary.append(span.text.replace('\u202f000', ''))
    for div in teg_div:
        list_company.append(div.text.replace('\xa0', ''))
    for item in city:
        if 'Москва' in item or 'Санкт-Петербург' in item:
            list_city.append(item.text.split()[0])

    list_dict = []
    for city, link, salary, company in zip(list_city, list_link, list_salary,
                                           list_company):
        if salary[-1] == '$':
            dict_job = {
                f"['link':{link}, 'salary':{salary}, 'company':{company},"
                f"'city':{city}]"
            }
            for i in dict_job:
                list_dict.append(i)

    with open('File information2.json', 'a', encoding='utf-8',
              newline="") as file:
        json.dump(list_dict, file, indent=2, ensure_ascii=False)
        file.write(',\n')
