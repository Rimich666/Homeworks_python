"""
Домашнее задание №1
Функции и структуры данных
"""


def power_numbers(*numbers):
    """
    функция, которая принимает N целых чисел,
    и возвращает список квадратов этих чисел
    """
    return[i*i for i in numbers]

# filter types
ODD = "odd"
EVEN = "even"
PRIME = "prime"

import math
def odd(input_list):
    return list(filter(lambda i: bool(i%2),input_list))
def even(input_list):
    return list(filter(lambda i: not(bool(i % 2)), input_list))

def is_prime(i,list_div):
    """Возвращает Истина, если i - простое"""
    hi_div_i = math.ceil(math.sqrt(i))
    is_pr = True
    for d in list_div:
        if d > hi_div_i or d == i:
            break
        if not (bool(i % d)):
            is_pr = False
            break
    return is_pr

def create_list_divisors(hi_div):
    """Создает список простых делителей"""
    list_div = []
    for i in range(2,hi_div):
        if is_prime(i,list_div):
            list_div.append(i)
    return list_div

def prime(input_list):
    """Возвращает список простых чисел"""
    max_numb = max(input_list)
    hi_div = math.ceil(math.sqrt(max_numb)) + 1
    list_div = create_list_divisors(hi_div)
    output_list = []
    for i in input_list:
        if is_prime(i, list_div):
            output_list.append(i)
    return output_list

dict_func = {'odd':odd,'even':even,'prime':prime}

def filter_numbers(input_list,filter_type):
    """
    функция, которая на вход принимает список из целых чисел,
    и возвращает только чётные/нечётные/простые числа
    (выбор производится передачей дополнительного аргумента)
    """
    return dict_func[filter_type](input_list)



list_power = power_numbers(1,2,3,4,5)
print(f"Список квадратов: {list_power}")

import random
max_number = 100000
num_count = 1500
list_int = [random.randint(1, max_number) for _ in range(0,num_count)]
print(f"Исходный список: {list_int}")

list_odd = filter_numbers(list_int,ODD)
print(f"Список нечетных: {list_odd}")

list_even = filter_numbers(list_int,EVEN)
print(f"Список четных: {list_even}")

list_prime = filter_numbers(list_int,PRIME)
print(f"Список простых чисел: {list_prime}")