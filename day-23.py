class Pooter:
    def __init__(self, data):
        self.data = data
        self.i = 0
        self.register = 0
        self.parameters = []
        self.param_idx = 0
        self.relative_base = 0


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

                if len(self.parameters) <= self.param_idx:
                    return "input"

                self.writeData(param_mode_data, 1, self.i + 1, self.parameters[self.param_idx])
                self.param_idx += 1
                self.i += 2
            elif opcode == 4:
                self.register = self.readData(param_mode_data, 1, self.i + 1)
                self.i += 2
                return "output"
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
            elif opcode == 9:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                self.relative_base += var1
                self.i += 2
            else:
                print("Bad op code " + str(opcode))
                return "done"

        return "done"


    def readData(self, parameter_mode_data, param_num, i):
        address = self.getAddress(parameter_mode_data, param_num, i)
        return self.data[address]


    def writeData(self, parameter_mode_data, param_num, i, output):
        address = self.getAddress(parameter_mode_data, param_num, i)
        self.data[address] = output


    def getAddress(self, parameter_mode_data, param_num, i):
        param_mode = self.getParamMode(parameter_mode_data, param_num)

        if param_mode == 0:
            if i >= len(self.data):
                diff = (i + 1) - len(self.data)
                self.data.extend([0] * diff)

            address = self.data[i]
        elif param_mode == 1:
            address = i
        elif param_mode == 2:
            if i >= len(self.data):
                diff = (i + 1) - len(self.data)
                self.data.extend([0] * diff)
            address = self.relative_base + self.data[i]
        else:
            print("Bad param mode " + str(param_mode))
            return 0

        if address >= len(self.data):
            diff = (address + 1) - len(self.data)
            self.data.extend([0] * diff)

        return address


    @staticmethod
    def getParamMode(parameter_mode_data, param_num):
        param_mode = 0
        if len(parameter_mode_data) >= param_num:
            param_mode = int(parameter_mode_data[param_num - 1])

        return param_mode


def solve():
    partOne()
    partTwo()


def partOne():

    pooters = []
    for i in range(0, 50):
        data = getData()
        pooter = Pooter(data)
        pooter.addParams(i)
        pooters.append(pooter)

    running = True
    while running:
        for p in pooters:
            result = p.executeProgram()
            if result == "input":
                p.addParams(-1)
            elif result == "output":
                a = p.register
                p.executeProgram()
                x = p.register
                p.executeProgram()
                y = p.register

                if a == 255:
                    print("PartOne: Y = " + str(y))
                    running = False
                else:
                    pooters[a].addParams(x)
                    pooters[a].addParams(y)


def partTwo():

    pooters = []
    for i in range(0, 50):
        data = getData()
        pooter = Pooter(data)
        pooter.addParams(i)
        pooters.append(pooter)

    nat_prev_y = None
    running = True
    ignore_first_idle = True
    while running:
        idle = 0
        for p in pooters:
            result = p.executeProgram()
            if result == "input":
                p.addParams(-1)
                idle += 1
            elif result == "output":
                a = p.register
                p.executeProgram()
                x = p.register
                p.executeProgram()
                y = p.register

                if a == 255:
                    nat = (x, y)
                else:
                    pooters[a].addParams(x)
                    pooters[a].addParams(y)

        if idle == 50:
            if ignore_first_idle:
                ignore_first_idle = False
            else:
                pooters[0].addParams(nat[0])
                pooters[0].addParams(nat[1])
                if nat[1] == nat_prev_y:
                    running = False
                    print("PartTwo: Nat previous y = " + str(nat_prev_y))
                nat_prev_y = nat[1]


def getData():
    input = open("day-23-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()