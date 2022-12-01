from pathlib import Path

input_path = Path(__file__).parent / "input"


def read_input_lines(input_filename):
    with open(input_path / input_filename) as infile:
        return infile.readlines()


def read_input(input_filename):
    with open(input_path / input_filename) as infile:
        return infile.read()
