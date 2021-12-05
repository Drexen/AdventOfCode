def solve():
    lines = [n for n in open("day-05-input.txt").readlines()]
    segments = []
    for line in lines:
        sides = line.split(" -> ")
        start = [int(n) for n in sides[0].split(",")]
        end = [int(n) for n in sides[1].split(",")]
        segments.append((start, end))

    part_one(segments)
    part_two(segments)


def part_one(segments):
    occurences = {}
    for (p0, p1) in segments:
        if p0[0] == p1[0]:
            for step in range(min(p0[1], p1[1]), max(p0[1], p1[1]) + 1):
                point = (p0[0], step)
                if point in occurences:
                    occurences[point] += 1
                else:
                    occurences[point] = 1
        elif p0[1] == p1[1]:
            for step in range(min(p0[0], p1[0]), max(p0[0], p1[0]) + 1):
                point = (step, p0[1])
                if point in occurences:
                    occurences[point] += 1
                else:
                    occurences[point] = 1

    two_overlaps = len([x for x in occurences.values() if x >= 2])
    print("Part one = " + str(two_overlaps))


def part_two(segments):
    occurences = {}
    for (p0, p1) in segments:

        xstep = max(min(p1[0] - p0[0], 1), -1)
        ystep = max(min(p1[1] - p0[1], 1), -1)

        xdiff = abs(p0[0] - p1[0])
        ydiff = abs(p0[1] - p1[1])

        for i in range(0, max(xdiff, ydiff) + 1):
            point = (p0[0] + (i * xstep), p0[1] + (i * ystep))
            if point in occurences:
                occurences[point] += 1
            else:
                occurences[point] = 1

    two_overlaps = len([x for x in occurences.values() if x >= 2])
    print("Part two = " + str(two_overlaps))


solve()
