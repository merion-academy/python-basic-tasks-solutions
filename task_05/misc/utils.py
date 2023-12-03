import math


def calculate_square(num):
    return num**2


def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average


def is_prime(n):
    """
    https://geekflare.com/prime-number-in-python/
    :param n:
    :return:
    """
    for i in range(2, int(math.sqrt(n)) + 1):
        if not (n % i):
            return False
    return True
