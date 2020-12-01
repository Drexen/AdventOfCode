import sys, pygame, time


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
    spr_w = 8
    board_w = 20
    board_h = 15

    pygame.init()

    size = board_w * spr_w * 2, board_h * spr_w * 2
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    running_game = True
    time_last = 0

    data = getData()
    #board = []
    pooter = Pooter(data)
    i = 0
    output = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if running_game is True:
            delta = (time.time() - time_last)
            if delta > 0.5:
                time_last = time.time()

                last_output_was_newline = False
                while True:
                    result = pooter.executeProgram()
                    if result == "output":
                        output.append(pooter.register)
                    else:
                        if len(output) > 0:
                            string = ASCIIToText(output)
                            print(string)
                            output = []

                        if result == "input":
                            commands = getCommandASCII(input())
                            for c in commands:
                                pooter.addParams(c)
                            i += 1
                            break
                        elif result == "done":
                            running_game = False
                            print("done")
                            break


        screen.fill(black)
        # drawBoard(screen, board, spr_w)
        pygame.display.flip()


def ASCIIToText(input):
    return ''.join(chr(i) for i in input)


def getCommandASCII(commands):
    output = []
    for c in commands:
        if c == '-':
            output.append(10)
        else:
            output.append(ord(c))
    output.append(10)
    return output


def generateBoard(data):
    pooter = Pooter(data)
    board = [[]]
    y = 0

    while True:
        result = pooter.executeProgram()
        if result == "done":
            break
        elif result == "output":
            if pooter.register == 10:
                board.append([])
                y += 1
            else:
                board[y].append(pooter.register)

    return board


def drawBoard(screen, board, spr_w):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            xpos = int((x + 4) * (spr_w + 1))
            ypos = int((y + 4) * (spr_w + 1))

            tile_type = board[y][x]
            if tile_type == 35:  # floor
                colour = (230, 230, 230)
            elif tile_type == 46:  # empty
                colour = (50, 50, 50)
            elif tile_type == 64:  # player
                colour = (255, 20, 50)
            else:
                colour = (0, 0, 0)
                print("Bad tile type: " + str(tile_type) + " at " + str(x) + " " + str(y))

            pygame.draw.rect(
                screen,
                colour,
                pygame.rect.Rect(xpos, ypos, spr_w, spr_w))


def isValidDrawableTile(tile):
    if tile == 35 or tile == 46 or tile == 64:
        return True
    return False


def getData():
    input = open("day-25-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()
