from argparse import ArgumentParser

from utils import read_as_list


def grid(inputfile):
    gridlines = read_as_list(inputfile)
    return [
        [ch for ch in row] for row in gridlines
    ]



def main(inputfile):
    ...


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    print(grid(args.inputfile))
