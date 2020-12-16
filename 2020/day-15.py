def solve():
    data = [int(i) for i in (open("day-15-input.txt").readlines()[0].split(","))]

    print("Part one = " + str(process(data, 2020)))
    print("Part two = " + str(process(data, 30000000)))


def process(data, num_iters):
    data_size = len(data)

    hist = {}
    last_spoken = 0
    for i in range(0, data_size):
        target = data[i]
        if i > 0:
            hist[last_spoken] = i - 1
        last_spoken = target

    for i in range(data_size, num_iters):
        last_spoken_existed = last_spoken in hist
        a = last_spoken
        if last_spoken_existed:
            last_spoken = i - hist[last_spoken] - 1
        else:
            last_spoken = 0
        hist[a] = i - 1

    return last_spoken


solve()
