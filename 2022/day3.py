import string
from argparse import ArgumentParser

from utils import read_as_list


def rucksacks(inputfile):
    return read_as_list(inputfile)


def identify_common_item(*rucksacks):
    rucksacks = [set(rucksack) for rucksack in rucksacks]
    common = set.intersection(*rucksacks)
    assert len(common) == 1
    return common.pop()


def identify_common_compartment_item(rucksack):
    each_comp_count = int(len(rucksack) / 2)
    comp1, comp2 = rucksack[0:each_comp_count], rucksack[each_comp_count:]
    return identify_common_item(comp1, comp2)


def get_priority(char):
    all_priorities = string.ascii_lowercase + string.ascii_uppercase
    return all_priorities.index(char) + 1


def total_priorities(rucksacks):
    common_items = [identify_common_compartment_item(rucksack) for rucksack in rucksacks]
    return sum([get_priority(item) for item in common_items])


def groups(rucksacks):
    for i in range(0, len(rucksacks), 3):
        yield rucksacks[i:i+3]


def total_badge_priorities(rucksacks):
    return sum(get_priority(identify_common_item(*group)) for group in groups(rucksacks))


def main(inputfile):
    print(total_priorities(rucksacks(inputfile)))
    print(total_badge_priorities(rucksacks(inputfile)))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    main(args.inputfile)
