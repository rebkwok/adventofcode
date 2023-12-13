import math
from pathlib import Path
import sys
from utils import read_input_filelines


def parse_games(lines):
    assert len(lines) == 2
    time = [int(t) for t in lines[0].split()[1:]]
    distance = [int(d) for d in lines[1].split()[1:]]
    return list(zip(time, distance))


def run(button_time, game_time):
    travel_time = game_time - button_time
    speed = button_time
    distance = speed * travel_time
    return distance


def part1(lines):
    games = parse_games(lines)

    game_total_winning_moves = []

    for i, game in enumerate(games):
        print(f"Game {i}")
        game_time, record = game
        possible_moves = game_time + 1
        median_time = game_time // 2

        print(f"Game time: {possible_moves}")
        if possible_moves % 2 == 0:
            print(f"Max: {median_time}, {median_time + 1}")
            winning_moves = 2
        else:
            print(f"Max: {median_time}")
            winning_moves = 1
        
        max_distance = run(median_time, game_time)
        assert max_distance > record

        test_time = median_time - 1
        while True:
            if run(test_time, game_time) > record:
                winning_moves += 2
                test_time -= 1
            else:
                break
        
        game_total_winning_moves.append(winning_moves)
    
    print(math.prod(game_total_winning_moves))


# def part2(lines):
#     print(lines)


if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
