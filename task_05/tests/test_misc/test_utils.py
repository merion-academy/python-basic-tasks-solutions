import pytest

from misc.utils import calculate_square, is_prime, calculate_average


@pytest.fixture(params=[2, 5, 10])
def input_num(request):
    return request.param


def test_calculate_square(input_num):
    result = calculate_square(input_num)
    assert result == input_num**2


@pytest.mark.parametrize(
    "input_numbers, expected_average",
    [
        ([1, 2, 3, 4, 5], 3),
        ([10, 20, 30, 40], 25),
    ],
)
def test_calculate_average(input_numbers, expected_average):
    result = calculate_average(input_numbers)
    assert result == expected_average


@pytest.mark.parametrize(
    "n, expected",
    [
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, False),
        (10, False),
        (11, True),
        (12, False),
    ],
)
def test_is_prime(n: int, expected: bool):
    assert is_prime(n) is expected
