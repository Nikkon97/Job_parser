import json
from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    def get_request(self):
        pass


class HeadHunterAPI(Engine):
    def get_request(self, keyword, page):
        headers = {
            "User - Agent": "TestApp/1.0(test@example.com)"
        }
        params = {
            "text": keyword,
            "page": page,
            "per_page": 100,

        }
        return requests.get("https://api.hh.ru/vacancies", params=params, headers=headers).json()["items"]

    def get_vacancies(self, keyword, count=1000):
        pages = 1
        response = []
        for page in range(pages):
            print(f"Парсинг страницы {page + 1}", end=": ")
            values = self.get_request(keyword, page)
            print(f"Найдено {len(values)} вакансий.")
            response.extend(values)

        return response


class Vacancy:
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'currency', 'employer', 'link', 'salary_sort_min', 'salary_sort_max')

    def __init__(self, title, salary_min, salary_max, currency, employer, link):
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link

        self.salary_sort_min = salary_min
        self.salary_sort_max = salary_max
        if currency and currency == 'USD':
            self.salary_sort_min = self.salary_sort_min * 83 if self.salary_sort_min else None
            self.salary_sort_max = self.salary_sort_max * 83 if self.salary_sort_max else None

    def __str__(self):
        salary_min = f'От {self.salary_min}' if self.salary_min else ''
        salary_max = f'До {self.salary_max}' if self.salary_max else ''
        currency = self.currency if self.currency else ''
        if self.salary_min is None and self.salary_max is None:
            salary_min = "Не указана"
        return f"{self.employer}: {self.title} \n{salary_min} {salary_max} {currency} \nURL: {self.link}"

    def __gt__(self, other):
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class JSONSaver:
    def __init__(self, keyword):
        self.__filename = f'{keyword.title()}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.__filename, 'r', encoding="utf-8") as file:
            data = json.load(file)

        vacancies = []
        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(
                Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'],
                        row['alternate_url']))
        return vacancies
