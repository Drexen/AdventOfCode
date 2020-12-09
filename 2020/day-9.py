import itertools


def solve():
    lines = open("day-9-input.txt").readlines()
    input = [int(line) for line in lines]

    target = part_one(input)
    part_two(input, target)


def part_one(input):
    for i in range(25, len(input)):
        results = [(input[c] + input[d]) for c, d in itertools.combinations(range(i - 25, i), 2)]
        if input[i] not in results:
            print("Part one = " + str(input[i]))
            return input[i]


def part_two(input, target):
    for i in range(0, len(input) - 1):
        for j in range(i + 1, len(input)):
            _sum = sum(input[i:j + 1])
            if _sum == target:
                print("Part two = " + str(min(input[i:j + 1]) + max(input[i:j + 1])))
                return
            if _sum > target:
                break


solve()
