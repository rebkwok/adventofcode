import pytest

from day1 import calories_per_elf, sum_per_elf, max_calories, max_top_3
from day2 import total_score, total_score_by_outcome

# day 1
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


# day 2
@pytest.mark.parametrize(
    "input_rounds,expected",
    [
        ((("A", "Y"), ("B", "X"), ("C", "Z")), 15),
        ((("A", "X"), ("B", "Y"), ("C", "Z")), (3 + 1) + (3 + 2) + (3 + 3)), # all draws
    ]
)
def test_total_rock_paper_scissors_score(input_rounds, expected):
    assert total_score(input_rounds) == expected


@pytest.mark.parametrize(
    "input_rounds,expected",
    [
        ((("A", "Y"), ("B", "X"), ("C", "Z")), 12),
        ((("A", "Y"), ("B", "Y"), ("C", "Y")), (3 + 1) + (3 + 2) + (3 + 3)), # all draws
    ]
)
def test_total_rock_paper_scissors_score_by_outcome_strategy(input_rounds,expected):
    assert total_score_by_outcome(input_rounds) == expected
