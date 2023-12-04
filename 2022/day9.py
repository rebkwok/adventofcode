from argparse import ArgumentParser

from utils import read_as_list


def moves(inputfile):
    return read_as_list(inputfile)


class Simulate:

    direction_map = {
        "U": (0, 1),
        "D": (0, -1),
        "R": (1, 0),
        "L": (-1, 0)
    }

    def __init__(self, moves, number_of_knots):
        self.moves = moves
        self.visited = {(0, 0)}
        self.positions = {i: [0, 0] for i in range(number_of_knots)}
        self.tail_index = number_of_knots - 1

    def itermoves(self):
        for move in self.moves:
            direction, count = move.split()
            yield (direction, int(count))

    def move_head(self, direction, count):
        move_x, move_y = self.direction_map[direction]
        for i in range(count):
            self.positions[0][0] += move_x
            self.positions[0][1] += move_y
            yield       

    def move_tail(self, tail):
        head_position = self.positions[tail - 1]
        tail_position = self.positions[tail]
        x_diff = head_position[0] - tail_position[0]
        y_diff = head_position[1] - tail_position[1]
        diff = abs(x_diff) + abs(y_diff)
        # print(f"a) H {head_position}, T {tail_position}")
        if diff == 2:
            # tail needs to move ONLY if it's not on a diagonal
            if head_position[0] == tail_position[0]:
                #x same, move y
                move_num = 1 if y_diff > 0 else -1
                tail_position[1] += move_num
            elif head_position[1] == tail_position[1]:
                #y same, move x
                move_num = 1 if x_diff > 0 else -1
                tail_position[0] += move_num
        elif diff > 2:
            move_x = 1 if x_diff > 0 else -1
            move_y = 1 if y_diff > 0 else -1
            tail_position[0] += move_x
            tail_position[1] += move_y
        self.positions[tail] = tail_position
        # print(f"b) H {head_position}, T {tail_position}")

    def go(self):
        
        for direction, count in self.itermoves():
            print(direction, count)
            print(f"START: {self.positions}")
            for _ in self.move_head(direction, count):
                for tail in list(self.positions.keys())[1:]:
                    self.move_tail(tail)
                    self.visited.add(tuple(self.positions[self.tail_index]))
            print(f"END: {self.positions}")


def total_visited(sim):
    return len(sim.visited)


def main(inputfile):
    sim = Simulate(moves(inputfile))
    sim.go()
    return total_visited(sim)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    print(main(args.inputfile))
