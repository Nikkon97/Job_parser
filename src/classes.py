from abc import ABC, abstractmethod
from global_variables import PRICE_EUR, PRICE_USD, PAGE_COUNT, VACANCY_COUNT, key_job

import requests
import json


class ParentApiClass(ABC):
    """Родительский класс, для классов, которые работают с API"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class ParentJSONSaver(ABC):
    """Родительский класс для классов, работающих с данными о вакансиях """

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def select(self):
        pass


class HeadHunterAPI(ParentApiClass):
    """Класс для работы с API Head Hunter"""

    def get_request(self, key_word, page):
        """Метод делает запрос на https://api.hh.ru/vacancies и возвращает результат в формате json по ключу [items]"""
        params = {
            "text": key_word,
            "page": page,
            "per_page": VACANCY_COUNT,
        }
        try:
            return requests.get("https://api.hh.ru/vacancies", params=params).json()["items"]
        except requests.exceptions.ConnectionError as e:
            print(e)
            print("Ошибка при запросе. Ошибка соединения")

    def get_vacancies(self, key_word):
        """Функция получает список заданных вакансий по кодовому слову и возвращает его"""
        data_list = []
        for x in range(PAGE_COUNT):
            values = self.get_request(key_word, x)
            data_list.extend(values)
        return data_list


class SuperJobAPI(ParentApiClass):
    """Класс для взаимодействия с SuperJobAPI"""
    page_count = 2

    def get_request(self, key_word, page):
        auth_data = {'X-Api-App-Id': key_job}
        params = {
            "keyword": key_word,
            "page": page,
            "count": VACANCY_COUNT,
        }
        try:
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=auth_data, params=params).json()[
                "objects"]
        except requests.exceptions.ConnectionError as e:
            print(e)
            print("Ошибка при запросе. Ошибка соединения")
        return response

    def get_vacancies(self, key_word):
        """Функция получает список заданных вакансию по кодовому слову и возвращает его"""
        data_list = []
        for x in range(PAGE_COUNT):
            values = self.get_request(key_word, x)
            data_list.extend(values)
        return data_list


class Vacancy:
    """Класс вакансий"""

    def __init__(self, title, salary_from, salary_to, salary_currency, url, employer_name, address):
        self.__title = title
        self.__url = url
        self.__employer_name = employer_name
        self.__address = address
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._salary_currency = salary_currency

    def __str__(self):
        if self._salary_currency:
            self._salary_currency = f"Зарплата({self._salary_currency}) "
        else:
            self._salary_currency = "Зарплата не указана"
        if self._salary_from:
            self._salary_from = f"от: {self._salary_from}  "
        else:
            self._salary_from = ""
        if self._salary_to:
            self._salary_to = f"до: {self._salary_to}"
        else:
            self._salary_to = " "
        if not self.__address:
            self.__address = "Не указано"
        msg = f"{self.__employer_name}  :  {self.__title}\n" \
              f"URL вакансии: {self.__url} \n" \
              f"{self._salary_currency}{self._salary_from}{self._salary_to}\n" \
              f"Адрес работодателя: {self.__address}"
        return msg

    def __gt__(self, other):
        """Метод сравнения по минимальной зарплате"""
        if not other._salary_from:
            return True
        if not self._salary_from:
            return False
        return self._salary_from >= other._salary_from


class JSONSaver(ParentJSONSaver):
    """Класс для работы с данными о вакансиях"""

    def __init__(self, key_word: str, name_file: str):
        self.__filename = f"{key_word.title()}_{name_file.lower()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancy(self, data):
        """Добавляет вакансии в файл 'self.__filename'"""
        with open(self.__filename, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        """Функция создает экземпляры класса Vacancy с заданными полями.
         Если указана зарплата, то пересчитывает её в рубли(при необходимости)
         Возвращает список вакансий
         """
        vacansies_list = []
        salary_from, salary_to, salary_currency = None, None, None

        with open(self.__filename, "r", encoding="UTF-8") as file:
            data = json.load(file)

        if "hh" in self.filename:
            for row in data:
                if row["salary"] and row["salary"]["to"] and row["salary"]["from"]:
                    salary_from, salary_to, salary_currency = row["salary"]["from"], row["salary"]["to"], row["salary"][
                        "currency"]
                    if row["salary"]["currency"].upper() == "EUR":
                        salary_from = row["salary"]["from"] * PRICE_EUR
                        salary_to = row["salary"]["to"] * PRICE_EUR
                    if row["salary"]["currency"].upper() == "USD":
                        salary_from = row["salary"]["from"] * PRICE_USD
                        salary_to = row["salary"]["to"] * PRICE_USD
                    salary_currency = "RUB"

                vacansies_list.append(Vacancy(
                    row["name"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["alternate_url"],
                    row["employer"]["name"],
                    row["area"]["name"]))

        if "sj" in self.filename:
            for row in data:
                if row["currency"]:
                    salary_from, salary_to, salary_currency = row["payment_from"], row["payment_to"], row["currency"]

                    if row["currency"].upper() == "EUR":
                        salary_from = row["payment_from"] * PRICE_EUR
                        salary_to = row["payment_to"] * PRICE_EUR
                    if row["currency"].upper == "USD":
                        salary_from = row["payment_from"] * PRICE_USD
                        salary_to = row["payment_to"] * PRICE_USD
                    salary_currency = "RUB"

                vacansies_list.append(Vacancy(
                    row["profession"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["link"],
                    row["firm_name"],
                    row["address"]))

        return vacansies_list
