from argparse import ArgumentParser

from utils import read_input


def main(inputfile):
    ...


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    main(args.inputfile)
