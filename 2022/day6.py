from argparse import ArgumentParser

from utils import read_input


def read_datastream(inputfile):
    return read_input(inputfile).strip()

def chunks(datastream, n):
    for i in range(0, len(datastream) - (n - 1)):
        characters_received_so_far = i + n
        yield datastream[i: i + n], characters_received_so_far

def first_marker(datastream, n):
    for chunk, received_so_far in chunks(datastream, n):
        # print(chunk, received_so_far)
        if len(set(chunk)) == n:
            return received_so_far

def main(inputfile, n):
    datastream = read_datastream(inputfile)
    # print(datastream)
    return first_marker(datastream, n)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    parser.add_argument("n", type=int)
    args = parser.parse_args()   
    print(main(args.inputfile, args.n))
