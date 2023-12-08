from pathlib import Path
import sys
from utils import read_input_filelines


def part1(lines):
    print(lines)


def part2(lines):
    print(lines)


if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
