def solve():
    input = open("day-13-input.txt").read().split("\n\n")
    dots = set([(int(n.split(",")[0]), int(n.split(",")[1])) for n in input[0].split("\n")])
    folds = [(n.split("=")[0][-1], int(n.split("=")[1])) for n in input[1].split("\n")]

    new_dots = fold(folds[0], dots)
    print("Part one = " + str(len(new_dots)))

    for f in folds[1:]:
        new_dots = fold(f, new_dots)

    print("Part two = ")
    dimensions = (max([d[0] for d in new_dots]), max([d[1] for d in new_dots]))
    for y in range(0, dimensions[1] + 1):
        line = ""
        for x in range(0, dimensions[0] + 1):
            line += "█" if (x, y) in new_dots else " "
        print(line)


def fold(instruction, dots):
    new_dots = set()
    for d in dots:
        if instruction[0] == 'y':
            new_dots.add((d[0], min(d[1], instruction[1] - (d[1] - instruction[1]))))
        else:
            new_dots.add((min(d[0], instruction[1] - (d[0] - instruction[1])), d[1]))
    return new_dots


solve()
