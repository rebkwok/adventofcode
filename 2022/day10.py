from argparse import ArgumentParser

from utils import read_as_list


def read_program(inputfile):
    return read_as_list(inputfile)


def iter_program_lines(program):
    for line in program:
        instr = line.split()
        if instr[0] == "noop":
            yield 0
        else:
            yield from [0, int(instr[1])]


def iter_program_instr(program):
    for line in program:
        instr = line.split()
        if instr[0] == "noop":
            yield [0]
        else:
            yield [0, int(instr[1])]


def run(inputfile):
    program = read_program(inputfile)
    cycle = 1
    x = 1
    strength = 0
    
    for addx in iter_program_lines(program):
        cycle += 1
        x += addx
        if cycle == 20 or ((cycle - 20) % 40 == 0):
            strength += (cycle * x) 
            print(f"Cycle {cycle}, X {x}, strength {strength}")
        if cycle == 220:
            break
    return strength


def draw(inputfile):
    program = read_program(inputfile)
    cycle = 1
    x = 1

    draw_chars = ""
    for addx in iter_program_instr(program):
        for i in range(len(addx)):
            position = (cycle - 1) % 40
            sprite_pos = [(x - 1) % 40, x % 40, (x + 1) % 40]
            sprite = ["." for i in range(40)]
            for pos in sprite_pos:
                sprite[pos] = "#"
            sprite = ''.join(sprite)
            # print (f"Sprite: {sprite}")
            char = "#" if position in sprite_pos else "."
            draw_chars += char
            cycle += 1
        x += addx[-1]

    for i in range(0, 40 * 6, 40):
        print(draw_chars[i:i+40])


def main(inputfile):
    ...


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    main(args.inputfile)
