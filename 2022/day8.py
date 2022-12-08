from argparse import ArgumentParser
import math

from utils import read_as_list


def heightmap(inputfile):
    # return x by y grid of tree heights, where x, y is the top left
    # 123 
    # 456
    # 789
    # becomes
    # [[1, 2, 3], [4, 5, 6], [7, 8, 8]] 
    # Find a tree by grid[row][col]
    input = read_as_list(inputfile)
    return [
        [int(ht) for ht in row] for row in input
    ]


def visible_outer_trees(heightmap):
    number_of_rows = len(heightmap[0])
    number_of_cols = len(heightmap)
    return (number_of_rows * 2) + ((number_of_cols - 2) * 2)
    

def visible_inner_trees(heightmap):
    number_of_rows = len(heightmap[0])
    number_of_cols = len(heightmap)

    row_range = [1, number_of_rows - 1]
    col_range = [1, number_of_cols - 1]
    visible_count = 0
    for row in range(*row_range):
        for col in range(*col_range):
            this_height = heightmap[row][col]
            # to left/right in same row
            if max(heightmap[row][0:col]) < this_height or max(heightmap[row][col + 1:]) < this_height:
                # visible in row, no need check col
                visible_count += 1
            else:
                # up/down in same col
                col_heights = [maprow[col] for maprow in heightmap]
                if max(col_heights[0:row]) < this_height or max(col_heights[row+1:]) < this_height:
                    # visible in col
                    visible_count += 1

    return visible_count


def _count_to_blocker(trees, this_height):
    count = 0
    while True:
        if not trees:
            break
        tree_ht = trees.pop()
        count += 1
        if tree_ht >= this_height:
            break
    return count

def scenic_score(heightmap, row, col):
    this_height = heightmap[row][col]
    lk_left = heightmap[row][0:col]
    lk_right = heightmap[row][col + 1:]
    lk_right.reverse()
    col_heights = [maprow[col] for maprow in heightmap]
    lk_up = col_heights[0:row]
    lk_down = col_heights[row+1:]
    lk_down.reverse()
    counts = [_count_to_blocker(trees, this_height) for trees in [lk_left, lk_right, lk_up, lk_down]]
    return math.prod(counts)

def highest_scenic_score(heightmap):
    number_of_rows = len(heightmap[0])
    number_of_cols = len(heightmap)

    row_range = [0, number_of_rows]
    col_range = [0, number_of_cols]
    highest_score = 0
    for row in range(*row_range):
        for col in range(*col_range):
            score = scenic_score(heightmap, row, col)
            if score > highest_score:
                highest_score = score
    return highest_score


def number_visible(heightmap):
    return visible_outer_trees(heightmap) + visible_inner_trees(heightmap)

def main(inputfile):
    htmap = heightmap(inputfile)
    return number_visible(htmap), highest_scenic_score(htmap)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    print(main(args.inputfile))
