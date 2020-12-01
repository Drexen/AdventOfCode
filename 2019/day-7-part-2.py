import itertools


class Pooter:
    def __init__(self, data):
        self.data = data
        self.i = 0
        self.register = 0
        self.parameters = []
        self.param_idx = 0


    def addParams(self, parameters):
        self.parameters.append(parameters)


    def executeProgram(self):
        while True:
            input = str((self.data[self.i]))
            opcode = int(input[len(input) - 2:])
            param_mode_data = input[0:len(input) - 2][::-1]

            if opcode == 99:
                break

            if opcode == 1:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                var2 = self.readData(param_mode_data, 2, self.i + 2)
                output = var1 + var2
                self.writeData(param_mode_data, 3, self.i + 3, output)
                self.i += 4
            elif opcode == 2:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                var2 = self.readData(param_mode_data, 2, self.i + 2)
                output = var1 * var2
                self.writeData(param_mode_data, 3, self.i + 3, output)
                self.i += 4
            elif opcode == 3:
                self.writeData(param_mode_data, 1, self.i + 1, self.parameters[self.param_idx])
                self.param_idx += 1
                self.i += 2
            elif opcode == 4:
                self.register = self.readData(param_mode_data, 1, self.i + 1)
                self.i += 2
                return False
            elif opcode == 5:
                var = self.readData(param_mode_data, 1, self.i + 1)
                if var == 0:
                    self.i += 3
                else:
                    self.i = self.readData(param_mode_data, 2, self.i + 2)
            elif opcode == 6:
                var = self.readData(param_mode_data, 1, self.i + 1)
                if var != 0:
                    self.i += 3
                else:
                    self.i = self.readData(param_mode_data, 2, self.i + 2)
            elif opcode == 7:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                var2 = self.readData(param_mode_data, 2, self.i + 2)
                output = 1 if var1 < var2 else 0
                self.writeData(param_mode_data, 3, self.i + 3, output)
                self.i += 4
            elif opcode == 8:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                var2 = self.readData(param_mode_data, 2, self.i + 2)
                output = 1 if var1 == var2 else 0
                self.writeData(param_mode_data, 3, self.i + 3, output)
                self.i += 4
            else:
                print("Bad op code " + str(opcode))
                return True

        return True


    def readData(self, parameter_mode_data, param_num, i):
        param_mode = self.getParamMode(parameter_mode_data, param_num)

        if param_mode == 0:
            return self.data[self.data[i]]
        elif param_mode == 1:
            return self.data[i]
        else:
            print("Bad param mode " + str(param_mode))


    def writeData(self, parameter_mode_data, param_num, i, output):
        param_mode = self.getParamMode(parameter_mode_data, param_num)

        if param_mode == 0:
            self.data[self.data[i]] = output
        elif param_mode == 1:
            self.data[i] = output
        else:
            print("Bad param mode " + str(param_mode))


    @staticmethod
    def getParamMode(parameter_mode_data, param_num):
        param_mode = 0
        if len(parameter_mode_data) >= param_num:
            param_mode = int(parameter_mode_data[param_num - 1])

        return param_mode


def solve():
    best = [0]*5
    best_val = 0
    for x in list(itertools.permutations([5, 6, 7, 8, 9])):
        pooters = []
        for d in range(0,5):
            pooters.append(Pooter(getData()))
            pooters[d].addParams(x[d])

        pooters[0].addParams(0)
        pooter_idx = 0
        while True:
            result = pooters[pooter_idx].executeProgram()
            if result is True and pooter_idx == 4:
                break
            else:
                input = pooters[pooter_idx].register
                pooter_idx = (pooter_idx + 1) % 5
                pooters[pooter_idx].addParams(input)

        if pooters[4].register > best_val:
            best_val = pooters[4].register
            best = x

    print("PartTwo = " + str(best) + " Val = " + str(best_val))


def getData():
    input = open("day-7-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()
