def solve():
    partOne()
    partTwo()


def partTwo():
    # Lets just brute force this
    x = 0
    y = 0
    while x < 100 or y < 100:
        data = getData()
        data[1] = x
        data[2] = y
        data = executeProgram(data)
        if data[0] == 19690720: # our target
            solution = 100 * x + y
            print("PartTwo - Found our target! noun = " + str(x) + " verb = " + str(y) + ". Solution = " + str(solution))
            break

        x += 1
        if x >= 100:
            x = 0
            y += 1


def partOne():
    data = getData()

    # replace position 1 with the value 12 and replace position 2 with the value 2
    data[1] = 12
    data[2] = 2

    data = executeProgram(data)

    # What value is left at position 0 after the program halts?
    print("PartOne - Value at idx 0 is " + str(data[0]))


def getData():
    input = open("day-2-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


def executeProgram(data):
    i = 0
    # lets begin
    while True:
        opcode = (data[i])
        if opcode == 99:
            break

        var1 = data[data[i+1]]
        var2 = data[data[i+2]]
        target = data[i+3]
        output = 0
        if opcode == 1:
            output = var1 + var2
        elif opcode == 2:
            output = var1 * var2
        else:
            print("Bad op code")
            break

        data[target] = output
        i += 4

    return data


solve()
