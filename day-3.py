def solve():
    wire = open("day-3-input.txt").readlines()
    wire_one = walkLine(wire[0])
    wire_two = walkLine(wire[1])

    intersections = set(wire_one) & set(wire_two)
    nearest = min(intersections, key=lambda x: abs(x[0]) + abs(x[1]))
    d = abs(nearest[0]) + abs(nearest[1])
    print("PartOne - distance = " + str(d))

    nearest = min(intersections, key=lambda x: getIndicesOfPoint(wire_one, wire_two, x))
    d = getIndicesOfPoint(wire_one, wire_two, nearest)

    print("PartTwo - distance = " + str(d))


def getIndicesOfPoint(wire_one, wire_two, x):
    w1 = wire_one.index(x)
    w2 = wire_two.index(x)
    return w1 + w2 + 2


def walkLine(input):
    direction = {'R':(1, 0), 'L':(-1, 0), 'U':(0, 1), 'D':(0, -1)}
    x, y = 0, 0
    steps = []
    for i in input.split(","):
        for _ in range(int(i[1:])):
            x += direction[i[0]][0]
            y += direction[i[0]][1]
            steps.append((x, y))

    return steps


solve()