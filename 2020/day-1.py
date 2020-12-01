def solve():
    lines = open("day-1-input.txt").readlines()
    nums = set()
    for line in lines:
        nums.add(int(line))

    print("Part one = " + str(partOne(nums)))
    print("Part two = " + str(partTwo(nums)))


def partOne(nums):
    for n in nums:
        target = 2020 - n
        if target in nums:
            return n * target


def partTwo(nums):
    for x, n1 in enumerate(nums):
        for y, n2 in enumerate(nums):
            if y > x:
                target = 2020 - (n1 + n2)
                if target in nums:
                    return n1 * n2 * target


solve()
