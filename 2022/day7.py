from argparse import ArgumentParser

from collections import deque

from utils import read_input, read_as_list


class Tree:

    def __init__(self, terminal_lines):
        self.parent_map = {"/": None}
        self.ancestors = {"/": set()}
        self.files = {}
        self.pwd = "/"
        self.counters = {}
        self.do_commands(terminal_lines)

    def cd(self, into_dir):
        if into_dir == "..":
            self.pwd = self.parent_map[self.pwd]
        else:
            if into_dir in self.parent_map:
                into_dir_count = self.counters.get(into_dir, 0)
                into_dir_count += 1
                self.counters[into_dir] = into_dir_count
                into_dir = f"{into_dir}_{into_dir_count}"
            # add the current dir to the parent map for the dir we're going into
            self.parent_map[into_dir] = self.pwd
            self.ancestors.setdefault(into_dir, set()).add(self.pwd)
            # and any parents of the current dir
            for ancestor in self.ancestors[self.pwd]:
                self.ancestors[into_dir].add(ancestor)
            self.pwd = into_dir
    
    def ls(self, ls_lines):
        for line in ls_lines:
            if not line.startswith("dir"):
                filesize, name = line.split(" ")
                if name in self.parent_map:
                    name_count = self.counters.get(name, 0)
                    name_count += 1
                    self.counters[name] = name_count
                    name = f"{name}_{name_count}"
                self.files[name] = int(filesize)
                self.parent_map[name] = self.pwd
                self.ancestors.setdefault(name, set()).add(self.pwd)
                for ancestor in self.ancestors[self.pwd]:
                    self.ancestors[name].add(ancestor)
    
    def parse_command_args(self, command_line):
        command_and_args = command_line.split(" ", 1)
        command = command_and_args[0]
        if len(command_and_args) == 1:
            args = None
        else:
            args = command_and_args[1]
        return command, args
    
    def do_commands(self, terminal_lines):
        ls_lines = []
        current_command = None
        assert terminal_lines[0] == "$ cd /"
        for line in terminal_lines[1:]:
            if line.startswith("$"):
                # a new command; if the current command is ls, we need to do ls with the 
                # stored ls lines
                if current_command == "ls":
                    self.ls(ls_lines)
                    ls_lines = []
                line = line.strip("$ ")
                command, args = self.parse_command_args(line)
                if command == "ls":
                    assert args is None
                else:
                    assert command == "cd"
                    self.cd(args)
            else:
                # last command is ls
                assert current_command == "ls"
                ls_lines.append(line)
            current_command = command
        
        # do the last ls
        if ls_lines:
            assert current_command == "ls"
            self.ls(ls_lines)

    def dir_sizes(self):
        directory_sizes = {}
        for filename, size in self.files.items():
            for ancestor in self.ancestors[filename]:
                ancestor_size = directory_sizes.get(ancestor, 0)
                ancestor_size += size
                directory_sizes[ancestor] = ancestor_size
        return directory_sizes


def terminal_lines(inputfile):
    return read_as_list(inputfile)


def total_size_lte(tree, n):
    return sum([val for val in tree.dir_sizes().values() if val <= n])


def smallest_dir_to_delete(tree):
    total_available = 70000000
    required_space = 30000000
    dir_sizes = tree.dir_sizes()
    total_filesystem_used = dir_sizes["/"]
    free_space = total_available - total_filesystem_used
    space_to_free_up = required_space - free_space
    possible_dirs = {
        k: v for k, v in dir_sizes.items() if v > space_to_free_up
    }
    return min(possible_dirs.values())


def main(inputfile):
    lines = terminal_lines(inputfile)
    tree = Tree(lines)
    return smallest_dir_to_delete(tree)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("inputfile")
    args = parser.parse_args()   
    print(main(args.inputfile))
