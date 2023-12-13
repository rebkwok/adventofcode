from collections import Counter
from pathlib import Path
import sys
from utils import read_input_filelines

"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

"""

HAND_TYPE_SCORES = {
        (5,): 6,
        (1, 4): 5,
        (2, 3): 4,
        (1, 1, 3): 3,
        (1, 2, 2): 2,
        (1, 1, 1, 2): 1,
        (1, 1, 1, 1, 1): 0 
    }

CARD_SCORES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}

CARD_SCORES_WITH_J = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
}

def hand_type_score(hand):
    # 7 - 5 of a kind
    # 6 - 4 of a kind
    # 5 - full house
    # 4 - 3 of a kind
    # 3 - 2 pair
    # 2 - 1 pair
    # 1 - high card 
    counter = Counter(hand)
    count_values = tuple(sorted(counter.values()))
    return HAND_TYPE_SCORES[count_values]


def hand_type_score_with_jokers(hand):
    counter = Counter(hand)
    count_values = tuple(sorted(counter.values()))
    initial_score = HAND_TYPE_SCORES[count_values]
    j_count = counter.get("J", 0)
    
    if j_count > 0 and j_count != 5:
        # make j's the same as the highest count card
        # if equal highest count card, use the one with the highest value
        non_j = [c for c in hand if c != "J"]
        non_j_counter = Counter(non_j)
        highest_count_cards = [c for c, count in non_j_counter.items() if count == max(non_j_counter.values())]
        highest_count_cards = sorted(highest_count_cards, key=lambda x: CARD_SCORES[x], reverse=True)
        top_card = highest_count_cards[0]
        new_hand = [c if c != "J" else top_card for c in hand]
        new_counter = counter = Counter(new_hand)
        new_count_values = tuple(sorted(new_counter.values()))
        new_score = HAND_TYPE_SCORES[new_count_values]
        if new_score > initial_score:
            return new_score
    
    return initial_score


def parse_hands_and_bids(lines):
    for line in lines:
        hand, bid = line.split()
        hand = [c for c in hand]
        yield hand, int(bid)


def card_score_key(hand_and_bid):
    hand = hand_and_bid[0]
    return tuple(CARD_SCORES[c] for c in hand)


def card_score_key_with_jokers(hand_and_bid):
    hand = hand_and_bid[0]
    return tuple(CARD_SCORES_WITH_J[c] for c in hand)


def calculate(lines, hand_type_score_fn, card_score_fn):
    hands_by_type = {}
    for hand, bid in parse_hands_and_bids(lines):
        hands_by_type.setdefault(
            hand_type_score_fn(hand), list()
        ).append((hand, bid))
    
    ranked_bids = []
    # sort types low to high
    types = sorted(hands_by_type.keys())
    for type_ in types:
        hands_and_bids = hands_by_type[type_]
        if len(hands_and_bids) == 1:
            # add bid to ranks
            ranked_bids.append(hands_and_bids[0][1])
        else:
            # sort hands low to high by first matching card
            hands_and_bids = sorted(hands_and_bids, key=card_score_fn)
            ranked_bids.extend([hb[1] for hb in hands_and_bids])

    print(sum(i * bid for i, bid in enumerate(ranked_bids, start=1))) 


def part1(lines):
    return calculate(lines, hand_type_score, card_score_key)


def part2(lines):
    return calculate(lines, hand_type_score_with_jokers, card_score_key_with_jokers)


if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
