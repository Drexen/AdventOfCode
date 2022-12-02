def solve():
    input = open("day-01-input.txt").readlines()
    nums = [0]
    for i in input:
        if i == '\n':
            nums.append(0)
        else:
            nums[len(nums) - 1] += int(i)

    nums.sort(reverse=True)

    print("Part one = " + str(nums[0]))
    print("Part two = " + str(sum(nums[:3])))


solve()
