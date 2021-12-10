def solve():
    lines = [n for n in open("day-09-input.txt").readlines()]
    data = []
    for i, line in enumerate(lines):
        data.append([int(n) for n in line[:-1]])

    risk_level = 0
    low_points = []
    for y, line in enumerate(data):
        for x, cell in enumerate(data[y]):
            if is_cell_low_point(x, y, data):
                risk_level += 1 + data[y][x]
                low_points.append((x, y))

    print("Part one = " + str(risk_level))

    basin_sizes = []
    for low_point in low_points:
        basin = []
        working_set = [low_point]
        while len(working_set) > 0:
            (x, y) = working_set.pop()
            basin.append((x, y))
            bla(x - 1, y, working_set, basin, data)
            bla(x + 1, y, working_set, basin, data)
            bla(x, y - 1, working_set, basin, data)
            bla(x, y + 1, working_set, basin, data)
        basin_sizes.append(len(basin))

    basin_sizes.sort(reverse=True)
    part_two = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    print("Part two = " + str(part_two))


def bla(x, y, working_set, basin, data):
    if 0 <= x < len(data[0]) and 0 < y < len(data):
        if data[y][x] < 9 and (x, y) not in basin and (x, y) not in working_set:
            working_set.append((x, y))


def is_cell_low_point(x, y, data):
    target = data[y][x]
    if x - 1 >= 0:
        if target >= data[y][x - 1]:
            return False
    if x + 1 < len(data[0]):
        if target >= data[y][x + 1]:
            return False
    if y - 1 >= 0:
        if target >= data[y - 1][x]:
            return False
    if y + 1 < len(data):
        if target >= data[y + 1][x]:
            return False
    return True


solve()
