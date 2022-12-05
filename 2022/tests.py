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
import day5


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


def test_read_starting_stacks_and_instructions():
    stacks, stack_count, instructions = day5.get_starting_stacks_and_instructions("day5_test.txt")
    assert stacks == [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]"
    ]
    assert stack_count == 3
    assert instructions == [
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]

    stacks, stack_count, _ = day5.get_starting_stacks_and_instructions("day5.txt")
    assert stack_count == 9
    assert stacks == [
        "                        [R] [J] [W]",
        "            [R] [N]     [T] [T] [C]",
        "[R]         [P] [G]     [J] [P] [T]",
        "[Q]     [C] [M] [V]     [F] [F] [H]",
        "[G] [P] [M] [S] [Z]     [Z] [C] [Q]",
        "[P] [C] [P] [Q] [J] [J] [P] [H] [Z]",
        "[C] [T] [H] [T] [H] [P] [G] [L] [V]",
        "[F] [W] [B] [L] [P] [D] [L] [N] [G]",
    ]


def test_parse_stacks():
    input = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]"
    ]
    # parsed stacks are bottom-to-top and L-to-R
    assert day5.parse_stacks(input, 3) == [
        ["Z", "N"], ["M", "C", "D"], ["P"]
    ]


def test_parse_instructions():
    instructions = [
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    assert list(day5.parse_instructions(instructions)) == [
        (1, 1, 0),
        (3, 0, 2),
        (2, 1, 0),
        (1, 0, 1)
    ]


def test_do_instructions_part1():
    parsed_stacks = [
        ["Z", "N"], ["M", "C", "D"], ["P"]
    ]
    instruction = [(1, 1, 0)]
    new_parsed_stacks = day5.do_instructions_part1(parsed_stacks, instruction)
    assert new_parsed_stacks == [["Z", "N", "D"], ["M", "C"], ["P"]] 

    instruction = [(3, 0, 2)]
    new_parsed_stacks = day5.do_instructions_part1(new_parsed_stacks, instruction)
    assert new_parsed_stacks == [[], ["M", "C"], ["P", "D", "N", "Z"]] 


def test_do_all_instructions_part1d():
    parsed_stacks = [["Z", "N"], ["M", "C", "D"], ["P"]]
    instructions = [
        (1, 1, 0),
        (3, 0, 2),
        (2, 1, 0),
        (1, 0, 1)
    ]
    assert day5.do_instructions_part1(parsed_stacks, instructions) == [
        ["C"], ["M"], ["P", "D", "N", "Z"]
    ]


def test_do_instructions_part2():
    parsed_stacks = [
        ["Z", "N"], ["M", "C", "D"], ["P"]
    ]
    instruction = [(1, 1, 0)]
    new_parsed_stacks = day5.do_instructions_part2(parsed_stacks, instruction)
    assert new_parsed_stacks == [["Z", "N", "D"], ["M", "C"], ["P"]] 

    instruction = [(3, 0, 2)]
    new_parsed_stacks = day5.do_instructions_part2(new_parsed_stacks, instruction)
    assert new_parsed_stacks == [[], ["M", "C"], ["P", "Z", "N", "D"]] 


def test_do_all_instructions_part2():
    parsed_stacks = [["Z", "N"], ["M", "C", "D"], ["P"]]
    instructions = [
        (1, 1, 0),
        (3, 0, 2),
        (2, 1, 0),
        (1, 0, 1)
    ]
    assert day5.do_instructions_part2(parsed_stacks, instructions) == [
        ["M"], ["C"], ["P", "Z", "N", "D"]
    ]


@pytest.mark.parametrize(
    "stacks,expected",
    [
        ([["C", "B"], ["C"], ["A", "B", "N"]], "BCN"),
        ([["C", "B"], [], ["A", "B", "N"], []], "BN")
    ]
)
def test_top_crates(stacks, expected):
    assert day5.top_crates(stacks) == expected


def test_day5():
    assert day5.main("day5_test.txt", part=1) == "CMZ"
    assert day5.main("day5_test.txt", part=2) == "MCD"
