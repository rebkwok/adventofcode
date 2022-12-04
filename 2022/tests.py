import pytest
from hypothesis import given
from hypothesis.strategies import text

from day1 import calories_per_elf, sum_per_elf, max_calories, max_top_3
from day2 import total_score, total_score_by_outcome
from day3 import (
    rucksacks, identify_common_compartment_item, get_priority, total_priorities,
    identify_common_item, total_badge_priorities
)
import day4


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


TEST_INPUT = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]

#day3
def test_rucksacks():
    # test we're reading the file as expected
    assert rucksacks("day3_test.txt") == TEST_INPUT


@pytest.mark.parametrize(
    "index,common",
    [
        (0, "p"),
        (1, "L"),
        (2, "P"),
        (3, "v"),
        (4, "t"),
        (5, "s")
    ]
)
def test_common_compartment_item(index, common):
    assert identify_common_compartment_item(TEST_INPUT[index]) == common


@pytest.mark.parametrize(
    "char,expected",
    [("a", 1), ("c", 3), ("A", 27), ("Z", 52)]
)
def test_get_priority(char, expected):
    assert get_priority(char) == expected


def test_total_priorities():
    assert total_priorities(TEST_INPUT) == 157


@pytest.mark.parametrize(
    "start,stop,common",
    [
        (0, 3, "r"),
        (3, 6, "Z"),
    ]
)
def test_common_item(start, stop, common):
    assert identify_common_item(*TEST_INPUT[start:stop]) == common


def test_total_badge_priorities():
    assert total_badge_priorities(TEST_INPUT) == 70


# day4

TEST_DAY4 = [
    "2-4,6-8", 
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8",
]

def test_read_assignment_pairs():
    # test we're reading the file as expected
    assert day4.read_input("day4_test.txt") == TEST_DAY4


def test_convert_assignment_pair_ranges():
    assert day4.convert_assignment_pair_ranges(TEST_DAY4) == [
        ([2, 3, 4], [6, 7, 8]),
        ([2, 3], [4, 5]),
        ([5, 6, 7], [7, 8, 9]),
        ([2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]),
        ([6], [4, 5, 6]),
        ([2, 3, 4, 5, 6], [4, 5, 6, 7, 8]),
    ]


@pytest.mark.parametrize(
    "input_pair,expected",
    [
        (([2, 3, 4], [6, 7, 8]), False),
        (([2, 3], [4, 5]), False),
        (([5, 6, 7], [7, 8, 9]), False),
        (([2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]), True),
        (([6], [4, 5, 6]), True),
        (([2, 3, 4, 5, 6], [4, 5, 6, 7, 8]), False),
    ]
)
def test_fully_contained(input_pair, expected):
    assert day4.fully_contained(*input_pair) is expected


def test_total_fully_contained():
    converted_input = [
        ([2, 3, 4], [6, 7, 8]),
        ([2, 3], [4, 5]),
        ([5, 6, 7], [7, 8, 9]),
        ([2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]),
        ([6], [4, 5, 6]),
        ([2, 3, 4, 5, 6], [4, 5, 6, 7, 8]),
    ]
    assert day4.total_fully_contained(converted_input) == 2


@pytest.mark.parametrize(
    "input_pair,expected",
    [
        (([2, 3, 4], [6, 7, 8]), False),
        (([2, 3], [4, 5]), False),
        (([5, 6, 7], [7, 8, 9]), True),
        (([2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]), True),
        (([6], [4, 5, 6]), True),
        (([2, 3, 4, 5, 6], [4, 5, 6, 7, 8]), True),
    ]
)
def test_overlap(input_pair, expected):
    assert day4.overlap(*input_pair) is expected


def test_total_overlap():
    converted_input = [
        ([2, 3, 4], [6, 7, 8]),
        ([2, 3], [4, 5]),
        ([5, 6, 7], [7, 8, 9]),
        ([2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]),
        ([6], [4, 5, 6]),
        ([2, 3, 4, 5, 6], [4, 5, 6, 7, 8]),
    ]
    assert day4.total_overlap(converted_input) == 4
