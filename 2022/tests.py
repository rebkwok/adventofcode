import pytest

from day1 import calories_per_elf, sum_per_elf, max_calories, max_top_3


@pytest.mark.parametrize(
    "input_string,expected",
    [
        (
            "1\n2\n3\n\n5\n6\n\n7\n\n6\n1\n",
            {1: [1, 2, 3], 2: [5, 6], 3: [7], 4: [6, 1]}
        ),
        (
            "1\n2\n3\n\n5\n6\n\n7\n\n6\n1\n\n",
            {1: [1, 2, 3], 2: [5, 6], 3: [7], 4: [6, 1]}
        ),
        (
            "1\n2\n3\n\n5\n6\n\n7\n\n6\n1",
            {1: [1, 2, 3], 2: [5, 6], 3: [7], 4: [6, 1]}
        ),
    ]
)
def test_calories_per_elf(input_string, expected):
    per_elf = calories_per_elf(input_string)
    assert per_elf == expected


def test_sum_per_elf():
    assert sum_per_elf({1: [1, 2, 3], 2: [5, 6], 3: [7], 4: [6, 1]}) == {1: 6, 2: 11, 3: 7, 4: 7}


def test_max():
    assert max_calories({1: 6, 2: 11, 3: 7, 4: 7}) == 11


def test_max_top_3():
    assert max_top_3({1: 6, 2: 11, 3: 7, 4: 7}) == 25
