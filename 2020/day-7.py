import re


def solve():
    lines = open("day-7-input.txt").readlines()

    data = {}
    for line in lines:
        d = parse_data(line)
        data[d[0]] = d[1]

    part_one(data)
    part_two(data)


def part_one(data):
    target = "shiny gold"

    solutions = set()
    working = {target}
    while len(working) > 0:
        current = set()
        for w in working:
            for outer_bag_key, outer_bag_contents in data.items():
                if w in outer_bag_contents:
                    if outer_bag_key not in solutions:
                        current.add(outer_bag_key)
                        solutions.add(outer_bag_key)
        working = current

    print("Part one = " + str(len(solutions)))


def part_two(data):
    target = "shiny gold"

    print("Part two = " + str(get_num_inner_bags(data, target)))


def get_num_inner_bags(data, target):
    return sum([(1 + get_num_inner_bags(data, bag_inner_name)) * bag_quantity
                for bag_inner_name, bag_quantity in data[target].items()])


def parse_data(input):
    split = input.split(" bags contain ")
    outer = split[0]

    contents = {}
    for match in re.findall(r'(\d+) (\w+ \w+)', split[1]):
        contents[match[1]] = int(match[0])

    return (outer, contents)


solve()
