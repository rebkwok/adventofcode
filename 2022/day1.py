from argparse import ArgumentParser

from utils import read_input


def calories_per_elf(input_string):
    by_elf = input_string.strip("\n\n").split("\n\n")
    calories_by_elf = {
        i: record.split("\n") for i, record in enumerate(by_elf, start=1)
    }
    return {
        i: [int(cal) for cal in record] for i, record in calories_by_elf.items()
    }


def sum_per_elf(calories_by_elf):
    return {
        i: sum(cals) for i, cals in calories_by_elf.items()
    }


def max_calories(total_per_elf):
    return max(total_per_elf.values())


def max_top_3(total_per_elf):
    return sum(sorted(total_per_elf.values(), reverse=True)[0:3])


def main(input_filename, calulate_max=False, calculate_max_top_3=False):
    calories_string = read_input(input_filename)
    per_elf = calories_per_elf(calories_string)
    totals = sum_per_elf(per_elf)
    if calulate_max:
        print(f"max total for one elf: {max_calories(totals)}")
    if calculate_max_top_3:
        print(f"max total for top 3: {max_top_3(totals)}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    parser.add_argument("-m1", "--max-1", dest="calculate_max", action="store_true")
    parser.add_argument("-m3", "--max-3", dest="calculate_max_top_3", action="store_true")
    args = parser.parse_args()   
    main(args.inputfile, args.calculate_max, args.calculate_max_top_3)
