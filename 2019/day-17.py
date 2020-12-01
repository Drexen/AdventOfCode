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


class PathPooter:
    def __init__(self, pooter, pos, dir):
        self.pooter = pooter
        self.pos = pos
        self.dir = dir


def solve():
    partOne()
    partTwo()


def partTwo():
    spr_w = 16
    board_w = 40
    board_h = 30

    pygame.init()

    size = board_w * spr_w * 2, board_h * spr_w * 2
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    running_game = True
    time_last = 0

    data = getData()
    data[0] = 2
    board = []
    pooter = Pooter(data)

    main_movement = "B,C,B,A,C,A,B,C,B,A"
    movement_a = "L,6,R,12,R,12,R,10"
    movement_b = "R,10,L,8,R,10,R,4"
    movement_c = "L,6,L,6,R,10"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if running_game is True:
            delta = (time.time() - time_last)
            if delta > 0:
                time_last = time.time()

                x = 0
                y = 0
                i = 0
                last_output_was_newline = False
                while True:
                    result = pooter.executeProgram()
                    if result == "input":
                        commands = []
                        if i == 0:
                            commands = getCommandASCII(main_movement)
                        elif i == 1:
                            commands = getCommandASCII(movement_a)
                        elif i == 2:
                            commands = getCommandASCII(movement_b)
                        elif i == 3:
                            commands = getCommandASCII(movement_c)
                        elif i == 4:
                            commands = getCommandASCII("y")
                        for c in commands:
                            pooter.addParams(c)
                        i += 1
                    elif result == "done":
                        running_game = False
                        print("PartTwo: Dust collected = " + str(pooter.register))
                        break
                    elif result == "output":
                        if pooter.register == 10:
                            y += 1
                            x = 0
                            if last_output_was_newline:
                                break
                            last_output_was_newline = True
                        else:
                            last_output_was_newline = False
                            if len(board) > 47:
                                break
                            if isValidDrawableTile(pooter.register):
                                while len(board) <= y:
                                    board.append([])
                                while len(board[y]) <= x:
                                    board[y].append(0)
                                board[y][x] = pooter.register
                                x += 1

        screen.fill(black)
        drawBoard(screen, board, spr_w)
        pygame.display.flip()


def partOne():
    data = getData()
    board = generateBoard(data)
    intersections = getIntersections(board)
    alignment_sum = sum([pos[0] * pos[1] for pos in intersections])
    print("PartOne: Alignment sum = " + str(alignment_sum))


def getCommandASCII(commands):
    output = []
    for c in commands:
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


def isValidDrawableTile(tile):
    if tile == ord('v') or \
            tile == ord('^') or \
            tile == ord('<') or \
            tile == ord('>') or \
            tile == 35 or \
            tile == 30 or \
            tile == 46 or \
            tile == 88:
        return True
    return False


def drawBoard(screen, board, spr_w):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            xpos = int((x + 4) * (spr_w + 1))
            ypos = int((y + 4) * (spr_w + 1))

            tile_type = board[y][x]
            if tile_type == ord('v'):
                points = [(xpos, ypos), (xpos + int(spr_w / 2), ypos + spr_w), (xpos + spr_w, ypos)]
                pygame.draw.polygon(screen, (50, 255, 100), points)
            elif tile_type == ord('^'):
                points = [(xpos, ypos + spr_w), (xpos + spr_w, ypos + spr_w), (xpos + int(spr_w / 2), ypos)]
                pygame.draw.polygon(screen, (50, 255, 100), points)
            elif tile_type == ord('<'):
                points = [(xpos + spr_w, ypos), (xpos, ypos + int(spr_w / 2)), (xpos + spr_w, ypos + spr_w)]
                pygame.draw.polygon(screen, (50, 255, 100), points)
            elif tile_type == ord('>'):
                points = [(xpos, ypos), (xpos, ypos + spr_w), (xpos + spr_w, ypos + int(spr_w / 2))]
                pygame.draw.polygon(screen, (50, 255, 100), points)
            else:
                if tile_type == 35:  # scaffold
                    colour = (220, 220, 220)
                elif tile_type == 30:  # scaffold on intersection
                    colour = (255, 80, 20)
                elif tile_type == 46:  # empty
                    colour = (50, 50, 50)
                elif tile_type == 88:  # dead
                    colour = (255, 20, 50)
                else:
                    colour = (0, 0, 0)
                    print("Bad tile type: " + str(tile_type) + " at " + str(x) + " " + str(y))

                pygame.draw.rect(
                    screen,
                    colour,
                    pygame.rect.Rect(xpos, ypos, spr_w, spr_w))


def getIntersections(board):
    intersections = []
    for y in range(1, len(board) - 3):
        for x in range(1, len(board[y]) - 1):
            if board[y][x] == 35:
                if board[y - 1][x] == 35 and \
                        board[y + 1][x] == 35 and \
                        board[y][x - 1] == 35 and \
                        board[y][x + 1] == 35:
                    intersections.append((x, y))
    return intersections


def getData():
    input = open("day-17-input.txt").read().split(",")
    data = []
    for i in input:
        data.append(int(i))

    return data


solve()
