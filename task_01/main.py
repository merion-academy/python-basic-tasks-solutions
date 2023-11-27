# Самостоятельная работа №1

# Задача №1. Куб
def make_cube(n):
    return n ** 3


# Задача №2. Повторение
def repeat(value):
    if isinstance(value, str):
        return value * 3
    return str(value) * 2


# Задача №3. Возведение в степень
def create_powers(
    *numbers,
    power=2,
):
    return [num ** power for num in numbers]


# Задача №4. Разворот числа
def reverse_number(number):
    result = 0

    while number > 0:
        remainder = number % 10
        result = result * 10 + remainder
        number //= 10

    return result


# Задача №5*. Рекурсия (задача со звёздочкой)
def fac(n):
    if n < 2:
        return n

    return fac(n - 1) * n


if __name__ == "__main__":
    print()
    print("make cube:")
    print("3:", make_cube(3))
    print("5:", make_cube(5))
    print("10:", make_cube(10))

    print()
    print("repeat:")
    print("str abc:", repeat("abc"))
    print("int 123:", repeat(123))
    print("str abc123:", repeat("abc123"))
    print("int 2:", repeat(2))
    print("str 123:", repeat("123"))

    print()
    print("create_powers:")
    print("powers ^2 for [1, 2, 3]:", create_powers(1, 2, 3, power=2))
    print("powers ^3 for [3, 4, 5]:", create_powers(3, 4, 5, power=3))

    print()
    print("reverse_number:")
    print("num 12345:", reverse_number(12345))
    print("num 111:", reverse_number(111))
    print("num 987:", reverse_number(987))

    print()
    print("factorial:")
    print("fac(1):", fac(1))
    print("fac(3):", fac(3))
    print("fac(5):", fac(5))
    print("fac(10):", fac(10))
