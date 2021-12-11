from copy import deepcopy


def solve():
    lines = [n for n in open("day-11-input.txt").readlines()]
    data = []
    for line in lines:
        data.append([int(n) for n in line.strip('\n')])

    width = len(data[0])
    height = len(data)

    num_flashes = 0
    part_one_data = deepcopy(data)
    for _ in range(0, 100):
        num_flashes += step(width, height, part_one_data)
    print("Part one = " + str(num_flashes))

    part_two_data = deepcopy(data)
    num_steps = 0
    while True:
        num_steps += 1
        num_flashes = step(width, height, part_two_data)
        if num_flashes == 100:
            break
    print("Part two = " + str(num_steps))


def step(width, height, data):
    for y in range(0, height):
        for x in range(0, width):
            increment_cell(x, y, width, height, data)

    num_flashes = 0
    for y in range(0, height):
        for x in range(0, width):
            if data[y][x] > 9:
                data[y][x] = 0
                num_flashes += 1
    return num_flashes


def increment_cell(x, y, w, h, data):
    data[y][x] += 1
    if data[y][x] == 10:
        for a in range(-1, 2):
            for b in range(-1, 2):
                try_increment_cell(x + a, y + b, w, h, data)


def try_increment_cell(x, y, w, h, data):
    if 0 <= x < w and 0 <= y < h:
        increment_cell(x, y, w, h, data)


solve()
