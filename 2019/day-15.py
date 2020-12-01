import copy
import sys, pygame, time

directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]


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


class PathPooter:
    def __init__(self, pooter, pos, dir):
        self.pooter = pooter
        self.pos = pos
        self.dir = dir


def solve():
    spr_w = 16
    board_w = 50
    board_h = 50

    pygame.init()

    size = board_w * spr_w, board_h * spr_w
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    data = getData()

    board = [0]*(board_h * board_w)

    running_game = True
    time_last = 0

    path_pooters = []

    for dir in range(0, 4):
        pooter = PathPooter(Pooter(data), (0, 0), dir)
        path_pooters.append(pooter)

    board = {}
    steps = 0
    explored = False
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if running_game is True:
            delta = (time.time() - time_last)
            if delta > 0:
                time_last = time.time()

                if not explored:
                    steps += 1
                    new_path_pooters = getNewPooters(steps, path_pooters, board)
                    if len(new_path_pooters) == 0:
                        explored = True
                        steps = 0
                    else:
                        path_pooters = new_path_pooters
                elif not done:
                    filled_tiles = list(filter(lambda x: x[1] == 2, board.items()))
                    filled_a_tile = False
                    for filled_tile in filled_tiles:
                        for i in range(0, 4):
                            target_pos = (filled_tile[0][0] + directions[i][0],
                                          filled_tile[0][1] + directions[i][1])
                            if board[target_pos] == 0:
                                board[target_pos] = 2
                                filled_a_tile = True

                    if not filled_a_tile:
                        print("PartTwo = Steps = " + str(steps))
                        done = True

                    steps += 1


        screen.fill(black)

        for tile in board.items():
            x = int((tile[0][0] + (board_w / 2)) * spr_w)
            y = int((tile[0][1] + (board_h / 2)) * spr_w)

            if tile[1] == 1:  # wall
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    pygame.rect.Rect(x, y, spr_w, spr_w))
            elif tile[1] == 0:  # empty
                pygame.draw.rect(
                    screen,
                    (150, 20, 0),
                    pygame.rect.Rect(x, y, spr_w, spr_w))
            elif tile[1] == 2:  # target
                pygame.draw.rect(
                    screen,
                    (50, 100, 255),
                    pygame.rect.Rect(x, y, spr_w, spr_w))

        pygame.display.flip()


def getNewPooters(steps, path_pooters, board):
    new_path_pooters = []
    for pooter in path_pooters:
        pooter.pooter.addParams(pooter.dir + 1)

        while True:
            result = pooter.pooter.executeProgram()
            if result == "done":
                break
            elif result == "input":
                break

        code = pooter.pooter.register
        if code == 0:
            wall_pos = (pooter.pos[0] + directions[pooter.dir][0],
                        pooter.pos[1] + directions[pooter.dir][1])
            board[wall_pos] = 1
        elif code == 1:
            empty_pos = (pooter.pos[0] + directions[pooter.dir][0],
                         pooter.pos[1] + directions[pooter.dir][1])
            board[empty_pos] = 0

            for i in range(0, 4):
                target_pos = (empty_pos[0] + directions[i][0],
                              empty_pos[1] + directions[i][1])
                if target_pos not in board:
                    new_path_pooter = copy.deepcopy(pooter)
                    new_path_pooter.dir = i
                    new_path_pooter.pos = empty_pos
                    new_path_pooters.append(new_path_pooter)

        elif code == 2:
            target_pos = (pooter.pos[0] + directions[pooter.dir][0],
                          pooter.pos[1] + directions[pooter.dir][1])
            board[target_pos] = 2
            print("PartOne = Steps = " + str(steps))

    return new_path_pooters


def getData():
    input = open("day-15-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()