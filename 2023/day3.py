import math
from pathlib import Path
import sys
from utils import read_input_filelines


def adjacent_indices(r, c_start, c_end, rows, cols):
    # row above
    if r > 0:
        for i in range(c_start - 1, c_end + 2):
            if 0 <= i < cols:
                yield (r - 1, i)
    
    # left
    if c_start > 0:
        yield (r, c_start - 1)
    
    # right
    if c_end < cols - 1:
        yield (r, c_end + 1)
    
    # row below
    if r < rows - 1:
        for i in range(c_start - 1, c_end + 2):
            if 0 <= i < cols:
                yield (r + 1, i)


def is_part_number(grid, coords_to_test):
    for (r, c) in coords_to_test:
        ch = grid[r][c]
        if ch == ".":
            continue
        try:
            int(ch)
        except ValueError:
            return True
    return False


def numbers_in_line(line):
    num = ""
    start = None
    for i, ch in enumerate(line):
        try:
            int(ch)
            num += ch
            if start is None:
                start = i
        except ValueError:
            if num:
                found_num = int(num)
                yield found_num, start, i-1
                num = ""
                start = None
    if num:
        yield int(num), start, i


def part_numbers(lines):
    grid = [[ch for ch in line] for line in lines]

    numbers_with_coords = []
    for i, row in enumerate(lines):
        for number, col_start, col_end in numbers_in_line(row):
            numbers_with_coords.append((number, i, col_start, col_end))

    rows = len(grid)
    cols = len(grid[0])
    
    for number, row_index, col_start, col_end in numbers_with_coords:
        coords_to_test = adjacent_indices(row_index, col_start, col_end, rows, cols)
        if is_part_number(grid, coords_to_test):
            yield number, row_index, col_start, col_end


def part1(lines):
    count = 0
    for number, _, _, _ in part_numbers(lines):
        count += number
    print(count)


def part2(lines):
    print(lines)
    grid = [[ch for ch in line] for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    part_nums = part_numbers(lines)
    part_num_coords = {}
    for part_num, row_index, col_start, col_end in part_nums:
        for i in range(col_start, col_end + 1):
            part_num_coords[(row_index, i)] = part_num

    print(part_num_coords)
    gear_ratio_sum = 0
    for row_num, row in enumerate(grid):
        for col_index, ch in enumerate(row):
            if ch == "*":
                coords_to_test = adjacent_indices(row_num, col_index, col_index, rows, cols)
                adjacent_part_numbers = {
                    part_num_coords[coord] for coord in coords_to_test if 
                    coord in part_num_coords
                }
                if len(adjacent_part_numbers) == 2:
                    gear_ratio = math.prod(adjacent_part_numbers)
                    print(row_num, col_index, gear_ratio)
                    gear_ratio_sum += gear_ratio

    print(gear_ratio_sum)                 


if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
