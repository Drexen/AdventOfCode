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
    spr_w = 16
    board_w = 37
    board_h = 22

    pygame.init()

    size = board_w * spr_w, board_h * spr_w
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    data = getData()
    pooter = Pooter(data)

    board = [0]*(board_h * board_w)

    colours = {
        1:(100, 100, 50),  # wall
        2:(230, 10, 0),  # block
        3:(10, 50, 200),  # paddle
        4:(255, 255, 255)  # ball
    }

    data[0] = 2

    running_game = True
    time_last = 0
    score = 0
    input = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if running_game is True:
            delta = (time.time() - time_last)
            if delta > 0:
                time_last = time.time()

                if 3 in board and 4 in board:
                    ball_pos_x = board.index(4) % board_w
                    paddle_pos_x = board.index(3) % board_w
                    target_paddle_x = ball_pos_x

                    if target_paddle_x > paddle_pos_x:
                        input = 1
                    elif target_paddle_x < paddle_pos_x:
                        input = -1
                    else:
                        input = 0

                pooter.addParams(input)

                while True:
                    result = pooter.executeProgram()
                    if result == "done":
                        running_game = False
                        print("Final score = " + str(score))
                        break
                    elif result == "input":
                        break

                    x = pooter.register
                    pooter.executeProgram()
                    y = pooter.register
                    pooter.executeProgram()
                    c = pooter.register

                    if x == -1 and y == 0:
                        score = c
                    else:
                        i = x + (y * board_w)
                        if i < len(board):
                            board[i] = c
                        else:
                            print("out of bounds - " + str(x) + " " + str(y))

        screen.fill(black)

        for i in range(0, len(board)):
            if board[i] != 0:
                x = int(i % board_w)
                y = int(i / board_w)
                pygame.draw.rect(screen, colours[board[i]], pygame.rect.Rect(x * spr_w, y * spr_w, spr_w, spr_w))

        pygame.display.flip()


def getData():
    input = open("day-13-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()