from pathlib import Path

input_path = Path(__file__).parent / "input"


def read_as_list(input_filename):
    return read_input(input_filename).strip("\n").split("\n")


def read_input(input_filename):
    with open(input_path / input_filename) as infile:
        return infile.read()
