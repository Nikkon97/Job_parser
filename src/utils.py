def get_vacancies_by_salary(list_vacancies: list, salary_from: int, salary_to: int = 0):
    """Функция принимает список вакансий.
     Функция возвращает список профессий с заданным параметром зарплат.
     Если минимальная зарплата в вакансии больше минимальной, переданной в параметр и
     максимальная зарплата в вакансии больше максимальной переданной в параметре,
     то данная вакансия добавляется в возвращаемый список.
     Максимальная зарплата по умолчанию равна '0'
    """
    new_list = []
    for data in list_vacancies:
        if data._salary_to and data._salary_from:
            if data._salary_from >= salary_from and data._salary_to >= salary_to:
                new_list.append(data)
                continue
        if data._salary_from and salary_to == 0:
            if data._salary_from >= salary_from:
                new_list.append(data)
    return new_list


def sort_from_minimum_salary(data: list, reverse_data=False):
    """Функция принимает список вакансий.
     Функция сортировки по минимальной зарплате, если она не указана, то вакансия пишется в начале списка
     и далее по возрастанию минимальной зарплаты.
     Второй аргумент по умолчанию False, если задать True, то вывод будет обратный
     """
    data = sorted(data, reverse=reverse_data)
    return data


def get_top_vacancies(data_list: list, top_n: int = 1):
    """Функция принимает отсортированный список вакансий и возвращает n-ое количество первых вакансий из списка
     По умолчанию возвращает один элемент списка"""
    new_list_data = data_list[0:top_n]
    return new_list_data