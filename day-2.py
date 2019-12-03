def solve():
    input = open("day-2-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    # replace position 1 with the value 12 and replace position 2 with the value 2
    data[1] = 12
    data[2] = 2

    i = 0
    # lets begin
    while True:
        opcode = (data[i])
        if opcode == 99:
            print("Done!")
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

    # What value is left at position 0 after the program halts?
    print("Value at idx 0 is " + str(data[0]))


solve()
