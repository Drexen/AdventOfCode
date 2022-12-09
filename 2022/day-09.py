import numpy

DIRECTIONS = {
    'R': [1, 0],
    'L': [-1, 0],
    'D': [0, 1],
    'U': [0, -1]
}


def clamp(num):
    return max(min(num, 1), -1)


def simulate(input, rope_size):
    visited = set()
    visited.add((0, 0))
    rope = [[0, 0] for _ in range(0, rope_size)]
    for line in input:
        direction, magnitude = line.split(" ")
        for i in range(0, int(magnitude)):
            rope[0] = numpy.add(rope[0], DIRECTIONS[direction])
            for segment in range(1, rope_size):
                segment_delta = [rope[segment - 1][0] - rope[segment][0], rope[segment - 1][1] - rope[segment][1]]

                if abs(segment_delta[0]) < 2 and abs(segment_delta[1]) < 2:
                    continue

                rope[segment][0] += clamp(segment_delta[0])
                rope[segment][1] += clamp(segment_delta[1])
            visited.add((rope[-1][0], rope[-1][1]))
    return visited


def solve():
    input = open("day-09-input.txt").read().splitlines()
    print("Part one = " + str(len(simulate(input, 2))))
    print("Part two = " + str(len(simulate(input, 10))))


solve()
