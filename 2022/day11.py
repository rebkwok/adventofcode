from argparse import ArgumentParser
import math
import re

from utils import read_as_list


class Game:
    def __init__(self, notes):
        self.initial = notes
        self._monkeys = None
        self.mod = 1

    @property
    def monkeys(self):
        if self._monkeys is None:
            self._monkeys = {}
            for i, index in enumerate(range(0, len(self.initial), 7)):
                monkey = self.initial[index: index + 7]
                items = [int(item) for item in monkey[1].strip().split("Starting items: ")[-1].split(",")]
                operation = monkey[2].strip().split("Operation: ")[-1].split("new = ")[-1]
                test_divisible_by = int(monkey[3].strip().split("Test: divisible by ")[-1])
                if_true = int(monkey[4].strip().split("If true: throw to monkey ")[-1])
                if_false = int(monkey[5].strip().split("If false: throw to monkey ")[-1])
                self._monkeys[i] = dict(
                    items=items,
                    item_count=0,
                    operation=operation,
                    test=(test_divisible_by, if_true, if_false)
                )
                self.mod *= test_divisible_by
            
        return self._monkeys

    def _test(self, x, divisible_by, if_true, if_false):
        if x % divisible_by == 0:
            return if_true
        return if_false

    def round(self):
        for monkey in self.monkeys.keys():
            rules = self.monkeys[monkey]
            for item in rules["items"]:
                self.monkeys[monkey]["item_count"] += 1
                old = item
                # old = self._reduce_m(old, rules["test"][0], rules["operation"])
                new = eval(rules["operation"])
                new = new % self.mod
                # new = new // 3
                throw_to_monkey = self._test(new, *rules["test"])
                self.monkeys[throw_to_monkey]["items"].append(new)
            self.monkeys[monkey]["items"] = []

    def play_rounds(self, number_of_rounds):
        for i in range(number_of_rounds):
            if i % 100 == 0:
                print(self.two_most_active())
            self.round()

    def two_most_active(self):
        counts = sorted([m["item_count"] for m in self.monkeys.values()], reverse=True)
        return counts[0] * counts[1]

    def test(self, rounds):
        self._monkeys = None
        self.play_rounds(rounds)
        print("done")
        print(self.two_most_active())


def notes(input_file):
    return read_as_list(input_file)


def main(inputfile):
    ...
    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    main(args.inputfile)
