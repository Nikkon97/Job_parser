# Job_parser

В данной работе решается задача парсинга с двух сайтов: headhunter и  superjob

В файле classes описаны класс для работы: 
  - ParentApiClass
  - HeadHunterAPI
  - SuperJobAPI
  - Vacancy
  - JSONSaver
  
В файле functions описаны функции:
  - get_vacancies_by_salary
  - sort_from_minimum_salary
  - get_top_vacancies
  
В файле global_variables указаны глобальные переменные, которые , при необходимости, можно изменить:
  - PRICE_EUR = 85 (указывает текущую стоимость евро по отношению к рублю)
  - PRICE_USD = 80 (указывает текущую стоимость доллара по отношению к рублю)
  - PAGE_COUNT = 10 (указывает на количестно запрашиваемых страниц данных с сайта)
  - VACANCY_COUNT = 100 (указывает на количестно выводимых вакансий на страницу сайта)
  - key_job в этой переменной необходимо указать свои данные, для работы с сайтом superjob
  
  В файле main написан основной код программы