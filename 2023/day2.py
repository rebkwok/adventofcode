import math
import re
from utils import read_input_filelines


REGEXES = {
    "red": re.compile(r"\s?(\d+) red"),
    "green": re.compile(r"\s?(\d+) green"),
    "blue": re.compile(r"\s?(\d+) blue")
}

def parse_game(game):
    game_id = int(re.findall("^Game (\d+): ", game)[0])
    subset_strings = game.split(": ")[-1].split("; ")
    subsets = []
    for subset_string in subset_strings:
        subset = {}
        for colour in ["red", "green", "blue"]:
            found = REGEXES[colour].findall(subset_string)
            subset[colour] = int(found[0]) if found else 0
        subsets.append(subset)
    return game_id, subsets


def game_valid(subsets, load):
    for subset in subsets:
        for col, count in subset.items():
            if count > load[col]:
                return False
    return True


def part1(lines):
    load = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    valid_ids = []
    for line in lines:
        game_id, subsets = parse_game(line)
        if game_valid(subsets, load):
            valid_ids.append(game_id)
    
    print(sum(valid_ids))


def min_load(subsets):
    return [
        max(subset[colour] for subset in subsets)
        for colour in ["red", "green", "blue"]
    ]


def part2(lines):
    game_powers = []
    for line in lines:
        _, subsets = parse_game(line)
        game_powers.append(math.prod(min_load(subsets)))

    print(sum(game_powers))

if __name__ == "__main__":
    lines = read_input_filelines(2, "input.txt")
    part2(lines)
