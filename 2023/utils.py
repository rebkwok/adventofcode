from pathlib import Path

base_path = Path(__file__).parent / "input"

def read_input_filelines(day, filename):
    filepath = base_path / f"day{day}" / filename
    text = filepath.read_text()
    return [
        line.strip() for line in text.strip().split("\n")
    ]
