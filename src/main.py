from classes import JSONSaver, SuperJobAPI, HeadHunterAPI
from utils import get_vacancies_by_salary, sort_from_minimum_salary, get_top_vacancies


# Создание экземпляра класса для работы с API сайтов с вакансиями
def main():
    def user_interaction():
        print("Приветствуем, Вас")
        search_query = input("Введите поисковый запрос: ")
        salary_min = int(input("Укажите минимально допустимый порог зарплаты "))
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))

        # Создание экземпляра класса для работы с API сайтов с вакансиями
        hh_api = HeadHunterAPI()
        sj_api = SuperJobAPI()

        # Получение вакансий с разных платформ
        hh_vacancies = hh_api.get_vacancies(search_query)
        sj_vacancies = sj_api.get_vacancies(search_query)

        # Сохранение информации о вакансиях в файл
        json_saver_hh = JSONSaver(search_query, "HH")
        json_saver_hh.add_vacancy(hh_vacancies)

        json_saver_sj = JSONSaver(search_query, "SJ")
        json_saver_sj.add_vacancy(sj_vacancies)

        # Отбор данных по вакансиям и создания списка вакансий
        vacansies_hh = json_saver_hh.select()
        vacansies_sj = json_saver_sj.select()

        # Сортировка вакансий по минимально допустимой зарплате
        sort_vacansies_hh = get_vacancies_by_salary(vacansies_hh, salary_min)
        sort_vacansies_sj = get_vacancies_by_salary(vacansies_sj, salary_min)

        # Сортировка списка вакансий по минимальной зарплате в убывающем порядке
        sort_vacansies_hh = sort_from_minimum_salary(sort_vacansies_hh, True)
        sort_vacansies_sj = sort_from_minimum_salary(sort_vacansies_sj, True)

        # Отбор
        top_vacansies_hh = get_top_vacancies(sort_vacansies_hh, top_n)
        top_vacansies_sj = get_top_vacancies(sort_vacansies_sj, top_n)

        print("\n\n", "Вывод вакансий с HeadHunter", "\n\n")
        for vacancy in top_vacansies_hh:
            print(vacancy)
            print("\n", "=" * 100, "\n")

        print("\n\n", "Вывод вакансий с SuperJob", "\n\n")
        for vacancy in top_vacansies_sj:
            print(vacancy)
            print("\n", "=" * 100, "\n")

    user_interaction()


if __name__ == "__main__":
    main()