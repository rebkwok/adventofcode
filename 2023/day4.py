from pathlib import Path
import sys
from utils import read_input_filelines


def as_list(num_str):
    return [int(num) for num in num_str.split()]

def parse_card(line):
    numbers = line.split(": ")[-1]
    winning, mine = numbers.split(" | ")
    return as_list(winning), as_list(mine) 


def get_score(winning, mine):
    matched = set(winning) & set(mine)
    if not matched:
        return 0
    else:
        score = 1
        for _ in range(len(matched) - 1):
            score *= 2
        return score


def part1(lines):
    total = 0
    for line in lines:        
        score = get_score(*parse_card(line))
        total += score
    print(total)


def get_winning_count(winning, mine):
    matched = set(winning) & set(mine)
    return len(matched)

def get_new_cards(card_num, card_counts, winning_count):
    if not winning_count:
        return card_counts
    last_card = max(card_counts)
    for i in range(card_counts[card_num]):
        for i in range(1, winning_count + 1):
            if card_num + i <= last_card:
                card_counts[card_num + i] += 1
    return card_counts


def part2(lines):
    cards = {
        i: get_winning_count(*parse_card(line)) for i, line in enumerate(lines, start=1)
    }
    # start with 1 of each card
    card_counts = {
        card_num: 1 for card_num in cards 
    }
    for card_num in card_counts.keys():
        winning_count = cards[card_num]
        get_new_cards(card_num, card_counts, winning_count)

    print(sum(card_counts.values()))


if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
