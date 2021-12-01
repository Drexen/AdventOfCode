def solve():
    nums = [int(n) for n in open("day-1-input.txt").readlines()]
    print("Part one = " + str(calculate(nums, 1)))
    print("Part two = " + str(calculate(nums, 3)))


def calculate(nums, step):
    count = 0
    for a, b in zip(nums, nums[step:]):
        if b > a:
            count += 1
    return count


solve()
