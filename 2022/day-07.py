import sys

REQUIRED_SPACE = 30000000
FILESYSTEM_CAPACITY = 70000000


class File:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.children = []


def parse_input(input):
    cd = []
    root = File()
    root.name = "/"
    cd.append(root)

    for line in input:
        if line[0] == '$':
            if line[2] == 'c':
                # assume cd
                if line[5] == '.':
                    cd.pop()
                else:
                    # cd to specific dir
                    target_filename = line[5:]
                    target_file = next(x for x in cd[-1].children if x.name == target_filename)
                    cd.append(target_file)
        else:
            # assume printing directory
            new_file = File()
            if line.startswith("dir "):
                new_file.name = line[4:]
            else:
                size, filename = line.split(' ')
                new_file.name = filename
                new_file.size = int(size)
            cd[-1].children.append(new_file)
    return root


def get_dir_size(dir):
    size = 0
    for file in dir.children:
        if file.size > 0:
            size += file.size
        else:
            size += get_dir_size(file)
    return size


def solve():
    input = open("day-07-input.txt").read().splitlines()
    root = parse_input(input[1:])

    total_sizes = 0
    dirs_to_check = [root]
    while len(dirs_to_check) > 0:
        cd = dirs_to_check.pop()
        for child in cd.children:
            if child.size == 0:
                dirs_to_check.append(child)
        size = get_dir_size(cd)
        if size <= 100000:
            total_sizes += size
    print("Part one = " + str(total_sizes))

    root_size = get_dir_size(root)
    target_size_to_delete = REQUIRED_SPACE - (FILESYSTEM_CAPACITY - root_size)
    print(target_size_to_delete)

    dirs_to_check = [root]
    current_best_size = sys.maxsize
    while len(dirs_to_check) > 0:
        cd = dirs_to_check.pop()
        for child in cd.children:
            if child.size == 0:
                dirs_to_check.append(child)
        size = get_dir_size(cd)
        if (size >= target_size_to_delete) and (size - target_size_to_delete) < (current_best_size - target_size_to_delete):
            current_best_size = size
    print("Part two = " + str(current_best_size))


solve()
