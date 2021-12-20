def solve():
    input = open("day-17-input.txt").read()[15:].replace(", y=", "..").split("..")
    (x0, x1, y0, y1) = [int(x) for x in input]

    yvel_max = abs(y0 + 1)
    yvel_max = gauss_summation(yvel_max)
    print("Part one = " + str(yvel_max))

    yvel_min = y0

    valids = {}
    for y in range(yvel_min, yvel_max + 1):
        step = 0
        ypos = 0
        yvel = y
        steps = []
        while ypos >= y0:
            step += 1
            ypos += yvel
            yvel -= 1
            if y1 >= ypos >= y0:
                steps.append(step)
        if len(steps) > 0:
            valids[y] = steps

    xvel_min = 0
    xvel_max = x1

    for y in valids.keys():
        valid_x = set()
        for s in valids[y]:
            for x in range(xvel_min, xvel_max + 1):
                xpos = gauss_summation(x) - gauss_summation(x - s)
                if x1 >= xpos >= x0:
                    valid_x.add(x)
        valids[y] = valid_x

    count = sum([len(s) for s in valids.values()])
    print("Part two = " + str(count))


def gauss_summation(x):
    if x < 0:
        return 0
    return int((x * x + x) / 2)


solve()

