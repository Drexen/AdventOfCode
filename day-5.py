def solve():
    data = getData()
    output = executeProgram(data, 1)
    print("PartOne - Register = " + str(output))

    data = getData()
    output = executeProgram(data, 5)
    print("PartTwo - Register = " + str(output))


def getData():
    input = open("day-5-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


def executeProgram(data, initial_register):
    i = 0
    register = initial_register
    while True:

        input = str((data[i]))
        opcode = int(input[len(input)-2:])
        param_mode_data = input[0:len(input)-2][::-1]

        if opcode == 99:
            break

        if opcode == 1:
            var1 = readData(data, param_mode_data, 1, i + 1)
            var2 = readData(data, param_mode_data, 2, i + 2)
            output = var1 + var2
            writeData(data, param_mode_data, 3, i + 3, output)
            i += 4
        elif opcode == 2:
            var1 = readData(data, param_mode_data, 1, i + 1)
            var2 = readData(data, param_mode_data, 2, i + 2)
            output = var1 * var2
            writeData(data, param_mode_data, 3, i + 3, output)
            i += 4
        elif opcode == 3:
            writeData(data, param_mode_data, 1, i + 1, register)
            i += 2
        elif opcode == 4:
            register = readData(data, param_mode_data, 1, i + 1)
            i += 2
        elif opcode == 5:
            var = readData(data, param_mode_data, 1, i + 1)
            if var == 0:
                i += 3
            else:
                i = readData(data, param_mode_data, 2, i + 2)
        elif opcode == 6:
            var = readData(data, param_mode_data, 1, i + 1)
            if var != 0:
                i += 3
            else:
                i = readData(data, param_mode_data, 2, i + 2)
        elif opcode == 7:
            var1 = readData(data, param_mode_data, 1, i + 1)
            var2 = readData(data, param_mode_data, 2, i + 2)
            output = 1 if var1 < var2 else 0
            writeData(data, param_mode_data, 3, i + 3, output)
            i += 4
        elif opcode == 8:
            var1 = readData(data, param_mode_data, 1, i + 1)
            var2 = readData(data, param_mode_data, 2, i + 2)
            output = 1 if var1 == var2 else 0
            writeData(data, param_mode_data, 3, i + 3, output)
            i += 4
        else:
            print("Bad op code " + str(opcode))
            return

    return register


def readData(data, parameter_mode_data, param_num, i):
    param_mode = getParamMode(parameter_mode_data, param_num)

    if param_mode == 0:
        return data[data[i]]
    elif param_mode == 1:
        return data[i]
    else:
        print("Bad param mode " + str(param_mode))


def writeData(data, parameter_mode_data, param_num, i, output):
    param_mode = getParamMode(parameter_mode_data, param_num)

    if param_mode == 0:
        data[data[i]] = output
    elif param_mode == 1:
        data[i] = output
    else:
        print("Bad param mode " + str(param_mode))


def getParamMode(parameter_mode_data, param_num):
    param_mode = 0
    if len(parameter_mode_data) >= param_num:
        param_mode = int(parameter_mode_data[param_num - 1])

    return param_mode


solve()
