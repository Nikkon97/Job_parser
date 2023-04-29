def sort_by_salary_min(data):
    data = sorted(data, reverse=True)
    return data


def sort_by_salary_max(data):
    data = sorted(data, key=lambda x: (x.salary_sort_max is not None, x.salary_sort_max), reverse=False)
    return data
