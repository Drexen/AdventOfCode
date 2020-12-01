from PIL import Image


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
            elif opcode == 9:
                var1 = self.readData(param_mode_data, 1, self.i + 1)
                self.relative_base += var1
                self.i += 2
            else:
                print("Bad op code " + str(opcode))
                return True

        return True


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
    data = getData()
    pooter = Pooter(data)

    pos = (0, 0)
    orientation = 0
    steps = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    grid = {(0, 0): 1}

    while True:
        if pos in grid:
            pooter.addParams(grid[pos])
        else:
            pooter.addParams(0)

        result = pooter.executeProgram()
        if result is True:
            break

        grid[pos] = pooter.register

        pooter.executeProgram()
        if pooter.register == 1:
            orientation = (orientation + 1) % 4
        else:
            orientation = (orientation + 3) % 4

        pos = (pos[0] + steps[orientation][0], pos[1] + steps[orientation][1])

    print("PartOne: Painted tiles = " + str(len(grid)))

    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for i in grid:
        if i[0] < xmin:
            xmin = i[0]
        if i[0] > xmax:
            xmax = i[0]
        if i[1] < ymin:
            ymin = i[1]
        if i[1] > ymax:
            ymax = i[1]

    img = Image.new('RGB', (xmax - xmin, ymax - ymin + 1))
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            i = (x + xmin, y + ymin)
            v = 0 if i not in grid else grid[i] * 255
            pixels[x, y] = (v, v, v)

    img.save("day-11-output.bmp")


def getData():
    input = open("day-11-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()