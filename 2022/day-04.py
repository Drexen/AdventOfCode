def is_fully_contained(d):
    if d[0] >= d[2] and d[1] <= d[3]:
        return True
    if d[2] >= d[0] and d[3] <= d[1]:
        return True
    return False


def does_overlap(d):
    if d[2] <= d[1] and d[3] >= d[0]:
        return True
    if d[0] <= d[3] and d[1] >= d[2]:
        return True
    return False


def solve():
    input = open("day-04-input.txt").read().split('\n')
    data = [[int(j) for j in i.replace(',', '-').split('-')] for i in input]
    num_fully_contained = sum(is_fully_contained(d) for d in data)
    print("Part one = " + str(num_fully_contained))

    num_overlaps = sum(is_fully_contained(d) or does_overlap(d) for d in data)
    print("Part two = " + str(num_overlaps))


solve()
