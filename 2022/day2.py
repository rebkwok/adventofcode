from argparse import ArgumentParser

from utils import read_input


class Game:
    
    # Rock defeats Scissors, 
    # Scissors defeats Paper 
    # Paper defeats Rock. 
    # If both players choose the same shape, the round instead ends in a draw.
    # lose = 0
    # draw = 3
    # win = 6 + POINTS by shape

    # A = Rock
    # B = Paper
    # C = Scissors
    
    SHAPE_POINTS = {
        "X": 1,
        "Y": 2,
        "Z": 3,
        "A": 1,
        "B": 2,
        "C": 3,
    }

    OUTCOME_POINTS = {
        0: 3, # draw
        1: 6, # player 2 wins
        2: 0, # player 1 wins
    }

    SHAPE_MAPPING = {
        "A": 0,
        "B": 1,
        "C": 2,
        "X": 0,
        "Y": 1,
        "Z": 2
    }

    # part 2
    # X = lose
    # Y = draw
    # Z = win
    # pick the shape that results in:
    OUTCOMES = {
        "X": 2,
        "Y": 0,
        "Z": 1
    }

    def __init__(self, strategy):
        self.strategy = strategy

    def round(self, player1, player2):
        player1_converted = self.SHAPE_MAPPING[player1]
        player2_converted = self.SHAPE_MAPPING[player2]
        result = (player2_converted - player1_converted) % 3
        return self.SHAPE_POINTS[player2] + self.OUTCOME_POINTS[result]
    
    def play_strategy(self):
        # play each round as if X=A, Y=B, Z=C
        for round in self.strategy:
            yield self.round(*round)

    def play_outcome(self):
        for player1, required_outcome in self.strategy:
            player1_converted = self.SHAPE_MAPPING[player1]
            outcome = self.OUTCOMES[required_outcome]
            for shape in ["A", "B", "C"]:
                shape_value = self.SHAPE_MAPPING[shape]
                if (shape_value - player1_converted) % 3 == outcome:
                    player2 = shape
                    break

            yield self.round(player1, player2)


def parse_strategy(input_filename):
    input_as_string = read_input(input_filename)
    split = input_as_string.strip("\n").split("\n")
    return [
        tuple(val.split()) for val in split if val
    ]


def total_score(input_strategy):
    game = Game(input_strategy)
    rounds = list(game.play_strategy())
    return sum(rounds)


def total_score_by_outcome(input_strategy):
    game = Game(input_strategy)
    rounds = list(game.play_outcome())
    return sum(rounds)


def main(input_filename):
    strategy = parse_strategy(input_filename)
    print(f"Total by scores (pt1): {total_score(strategy)}")
    print(f"Total by outcome strategy(pt2): {total_score_by_outcome(strategy)}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    # parser.add_argument("-m1", "--max-1", dest="calculate_max", action="store_true")
    # parser.add_argument("-m3", "--max-3", dest="calculate_max_top_3", action="store_true")
    args = parser.parse_args()   
    main(args.inputfile)
