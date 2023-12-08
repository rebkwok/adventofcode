import re
from utils import read_input_filelines


def isint(ch):
        try:
            int(ch)
            return True
        except ValueError:
            return False
    
def get_first_num(line):
        num = next(c for c in line if isint(c))
        return int(num)


def get_calibration_number(line):
    return get_first_num(line) * 10 + get_first_num(reversed(line))


def part1():
    lines = read_input_filelines(1, "input.txt")

    calibration_numbers = [
        get_calibration_number(line) for line in lines
    ]
    print(sum(calibration_numbers))


NUMBER_MAP = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

FIRST_NUMBER_RE = re.compile(rf".*?(\d|{'|'.join(NUMBER_MAP.keys())}).*")
LAST_NUMBER_RE = re.compile(rf".*(\d|{'|'.join(NUMBER_MAP.keys())}).*")


def get_number(line, regex):
    number = regex.findall(line)[0]
    return int(NUMBER_MAP.get(number, number))


def part2(lines):
    calibration_numbers = []
    for line in lines:
        first_num = get_number(line, FIRST_NUMBER_RE)
        last_num = get_number(line, LAST_NUMBER_RE)
        calibration_numbers.append(first_num * 10 + last_num)
    print(sum(calibration_numbers))


if __name__ == "__main__":
    part2(read_input_filelines(1, "input.txt"))
