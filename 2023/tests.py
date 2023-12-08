import pytest

from day5 import MappingRange, overlaps


@pytest.mark.parametrize(
    "seed_range,expected",
    [
        ((48, 54), True), # overlaps start only
        ((57, 67), True), # overlaps end only
        ((51, 58), True), # contained
        ((48, 62), True), # contains
        ((40, 50), False), # end is exclusive, doesn't overlap
        ((40, 51), True),  # overlaps by 1
        ((60, 70), False), # mapping end is exclusive, doesn't overlap
        ((59, 70), True), # overlaps by 1
    ]
)
def test_overlaps(seed_range, expected):
    mrange = MappingRange(destination_start=52, source_start=50, length=10)
    # range 50 51 52 53 54 55 56 57 58 59
    assert overlaps(seed_range, mrange) == expected
