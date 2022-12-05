from argparse import ArgumentParser
import re

from utils import read_as_list


def get_starting_stacks_and_instructions(inputfile):
    input = read_as_list(inputfile)
    break_index = input.index("")
    starting_stacks = input[0:break_index - 1]
    stack_numbers = input[break_index - 1]
    stack_count = int(stack_numbers.strip().split(" ").pop() )  
    assert len(starting_stacks[0]) == (stack_count * 4) -1 
    instructions = input[break_index + 1:]
    return starting_stacks, stack_count, instructions


def parse_stacks(starting_stacks, stack_count):
    def row_list(row):
        for i in range(0, len(row), 4):
            yield row[i:i+4]
    
    stacks = [[] for i in range(stack_count)]
    for row in starting_stacks:
        # split row into list of right number of items
        row_as_list = list(row_list(row))
        for i, item in enumerate(row_as_list):
            item = re.match(r"\[(\w)\]", item, flags=re.X)
            if item:
                matched = item.groups(0)[0]
                stacks[i].insert(0, matched)
    return stacks


INSTRUCTION_REGEX = re.compile(
    r"move (?P<number_to_move>(\d+)) from (?P<from_stack>(\d+)) to (?P<to_stack>(\d+))"
)

def parse_instructions(instructions):
    for row in instructions:
        matches = INSTRUCTION_REGEX.match(row)
        yield (int(matches["number_to_move"]), int(matches["from_stack"]) - 1, int(matches["to_stack"]) - 1)


def do_instructions_part1(stacks, instructions):
    for number_to_move, from_stack, to_stack in instructions:
        for i in range(number_to_move):
            item = stacks[from_stack].pop()
            stacks[to_stack].append(item)
    return stacks


def do_instructions_part2(stacks, instructions):
    for number_to_move, from_stack, to_stack in instructions:
        items_to_move = []
        for i in range(number_to_move):
            items_to_move.append(stacks[from_stack].pop())
        items_to_move.reverse()
        stacks[to_stack].extend(items_to_move)
    return stacks


def top_crates(stacks):
    top = [stack[-1] for stack in stacks if stack]
    return "".join(top)


def main(inputfile, part):
    starting_stacks, stack_count, instructions = get_starting_stacks_and_instructions(inputfile)
    stacks = parse_stacks(starting_stacks, stack_count)
    parsed_instructions = parse_instructions(instructions)
    if part == 1:
        new_stacks = do_instructions_part1(stacks, parsed_instructions)
    elif part == 2:
        new_stacks = do_instructions_part2(stacks, parsed_instructions)
    return top_crates(new_stacks)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    parser.add_argument("--part", "-p", type=int)
    args = parser.parse_args()   
    print(main(args.inputfile, part=args.part))
