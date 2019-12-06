def solve():
    input = (123257, 647015)
    partOne(input)
    partTwo(input)


def partOne(input):
    possibles = []
    for i in range(input[0], input[1] + 1):
        if validatePartOne(i):
            possibles.append(i)

    print("PartOne - num possibles = " + str(len(possibles)))


def partTwo(input):
    possibles = []
    for i in range(input[0], input[1] + 1):
        if validatePartTwo(i):
            possibles.append(i)

    print("PartTwo - num possibles = " + str(len(possibles)))


def validatePartOne(i):
    prev = -1
    double = False
    for c in str(i):
        if int(c) < prev:
            return False
        if int(c) == prev:
            double = True

        prev = int(c)

    return double


def validatePartTwo(i):
    prev = -1
    digits = [0]*10
    for c in str(i):
        if int(c) < prev:
            return False

        digits[int(c)] += 1
        prev = int(c)

    return 2 in digits


solve()