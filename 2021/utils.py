from pathlib import Path

def read_input(path, convert=None):
    lines = path.read_text().strip().split("\n")
    if convert:
        lines = [convert(line) for line in lines]
    return lines
