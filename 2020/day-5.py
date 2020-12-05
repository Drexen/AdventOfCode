import sys


def solve():
    lines = open("day-5-input.txt").readlines()

    part_one(lines)
    part_two(lines)


def part_one(lines):
    _max = 0
    for line in lines:
        id = get_id(line)
        _max = max(_max, id)

    print("Part one = " + str(_max))


def part_two(lines):
    _min = sys.maxsize
    _max = 0
    _sum = 0
    for line in lines:
        id = get_id(line)
        _min = min(_min, id)
        _max = max(_max, id)
        _sum = _sum + id
    target_sum = sum(range(_min, _max + 1))

    print("Part two = " + str(target_sum - _sum))


def get_id(input):
    return int(input.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2)


solve()
