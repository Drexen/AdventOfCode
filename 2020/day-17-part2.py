def solve():
    data = set()
    bounds = (0, 8)
    for y, line in enumerate(open("day-17-input.txt").readlines()):
        for x, value in enumerate(line):
            if value == "#":
                data.add((x, y, 0, 0))

    for _ in range(0, 6):
        bounds = (bounds[0] - 1, bounds[1] + 1)
        step(data, bounds)

    print("Part two = " + str(len(data)))


def step(data, bounds):
    dupe = set(data)
    for w in range(bounds[0], bounds[1]):
        for z in range(bounds[0], bounds[1]):
            for y in range(bounds[0], bounds[1]):
                for x in range(bounds[0], bounds[1]):
                    if step_cell((x, y, z, w), dupe):
                        data.add((x, y, z, w))
                    else:
                        data.discard((x, y, z, w))


def step_cell(pos, data):
    count = 0
    for w in range(pos[3] - 1, pos[3] + 2):
        for z in range(pos[2] - 1, pos[2] + 2):
            for y in range(pos[1] - 1, pos[1] + 2):
                for x in range(pos[0] - 1, pos[0] + 2):
                    if x != pos[0] or y != pos[1] or z != pos[2] or w != pos[3]:
                        if (x, y, z, w) in data:
                            count += 1

    if pos in data:
        return count == 2 or count == 3
    return count == 3


solve()
