from argparse import ArgumentParser

from utils import read_as_list


def read_input(inputfile):
    return read_as_list(inputfile)


def convert_assignment_pair_ranges(input):
    pairs = []
    for line in input:
        elf1, elf2 = [elf.split("-") for elf in line.split(",")]

        elf1_range = list(range(int(elf1[0]), int(elf1[1]) + 1))
        elf2_range = list(range(int(elf2[0]), int(elf2[1]) + 1))
        pairs.append((elf1_range, elf2_range))
    return pairs


def assignments_in_common(elf1, elf2):
    elf1 = set(elf1)
    elf2 = set(elf2)
    return elf1 & elf2


def fully_contained(elf1, elf2):
    common = assignments_in_common(elf1, elf2)
    return common == set(elf1) or common == set(elf2)


def overlap(elf1, elf2):
    common = assignments_in_common(elf1, elf2)
    return bool(common)


def total_fully_contained(assigment_pairs):
    return sum(1 for pair in assigment_pairs if fully_contained(*pair))


def total_overlap(assigment_pairs):
    return sum(1 for pair in assigment_pairs if overlap(*pair))


def main(inputfile):
    input = read_input(inputfile)
    pair_ranges = convert_assignment_pair_ranges(input)
    print(total_fully_contained(pair_ranges))
    print(total_overlap(pair_ranges))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    main(args.inputfile)
