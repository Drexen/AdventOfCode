dirs = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]


def solve():
    input = [line.strip() for line in open("day-11-input.txt").readlines()]

    part_one(input)
    part_two(input)


def part_one(input):
    while 1:
        output = step(input, get_num_adjacent_occupied, 4)
        if output == input:
            print("Part one = " + str(get_total_num_occupied(output)))
            break
        print(".")
        input = output


def part_two(input):
    while 1:
        output = step(input, get_num_visible_occupied, 5)
        if output == input:
            print("Part two = " + str(get_total_num_occupied(output)))
            break
        print(".")
        input = output


def step(input, get_num_occupied_func, social_tolerance_value):
    output = []
    for y in range(0, len(input)):
        line = ""
        for x in range(0, len(input[y])):
            num_adjacent = get_num_occupied_func((x, y), input)
            if input[y][x] == "L" and num_adjacent == 0:
                    line = line + "#"
            elif input[y][x] == "#" and num_adjacent >= social_tolerance_value:
                line = line + "L"
            else:
                line = line + input[y][x]
        output.append(line)
    return output


def get_num_adjacent_occupied(target, input):
    count = 0
    for y in range(target[1] - 1, target[1] + 2):
        for x in range(target[0] - 1, target[0] + 2):
            if 0 <= y < len(input) and 0 <= x < len(input[y]):
                if y != target[1] or x != target[0]:
                    if input[y][x] == "#":
                        count += 1
    return count


def get_num_visible_occupied(target, input):
    count = 0
    for d in dirs:
        count += 1 if is_occupied_chair_in_direction(target, d, input) else 0
    return count


def is_occupied_chair_in_direction(center, dir, input):
    target = tuple(map(sum, zip(center, dir)))
    if 0 <= target[1] < len(input) and 0 <= target[0] < len(input[target[1]]):
        cell = input[target[1]][target[0]]
        if cell == "#":
            return True
        elif cell == "L":
            return False
        else:
            return is_occupied_chair_in_direction(target, dir, input)
    else:
        return False


def get_total_num_occupied(input):
    count = 0
    for y in range(0, len(input)):
        for x in range(0, len(input[y])):
            if input[y][x] == "#":
                count += 1
    return count


solve()
