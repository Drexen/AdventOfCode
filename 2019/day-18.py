import copy
import sys, pygame, time


class Pather:
    def __init__(self, board):
        self.board = board
        self.path = []
        self.collected_keys = []
        self.steps = 0


    def givePath(self, path):
        self.path = path


    def walkPath(self):
        target_pos = self.path[0]
        player_pos = getObjectPosition(self.board, '@')

        self.board[player_pos[1]][player_pos[0]] = '.'

        target_object = self.board[target_pos[1]][target_pos[0]]
        if target_object.isalpha() and target_object.islower():
            door = target_object.upper()
            door_pos = getObjectPosition(self.board, door)
            if door_pos is not None:
                self.board[door_pos[1]][door_pos[0]] = ''
            self.collected_keys.append(target_object)
        else:
            print("Expected a key here")

        self.board[target_pos[1]][target_pos[0]] = '@'
        self.steps += len(self.path)
        self.path = []



def solve():
    spr_w = 16
    board_w = 100
    board_h = 100

    pygame.init()

    font = pygame.font.Font("consola.ttf", spr_w)

    board = generateBoard()
    pathers = []
    pather = Pather(board)
    pathers.append(pather)

    while True:
        new_pathers = []
        key_remaining = False
        for p in pathers:
            player_pos = getObjectPosition(p.board, '@')
            key_locations = getKeyLocations(p.board)
            if len(key_locations) > 0:
                key_remaining = True
            bounds = (len(p.board[0]), len(p.board))

            for k in key_locations:
                result, path = getPathToTarget(p.board, bounds, player_pos, k)
                if result:
                    new_pather = copy.deepcopy(p)
                    new_pather.givePath(path)
                    new_pathers.append(new_pather)
        if not key_remaining:
            break
        pathers = new_pathers

        for p in pathers:
            p.walkPath()

        bla = len(pathers)
        for xi, x in enumerate(pathers):
            for yi, y in enumerate(pathers):
                if x is not y and x is not None and y is not None:
                    if x.collected_keys[-1] == y.collected_keys[-1]:
                        if set(x.collected_keys) == set(y.collected_keys):
                            if x.steps > y.steps:
                                pathers[xi] = None
                            else:
                                pathers[yi] = None

        pathers = list(filter(lambda i: i is not None, pathers))
        dupes = bla - len(pathers)
        print("Num pathers = " + str(len(pathers)) + " removed dupes: " + str(dupes))

    print("DONE")
    print("Steps = " + str(pathers[0].steps))
    print(pathers[0].collected_keys)
    return

















    size = board_w * spr_w, board_h * spr_w
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    board_surface = pygame.Surface(size)
    #drawBoardBase(board_surface, board, spr_w, font)

    time_last = 0
    path = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        delta = (time.time() - time_last)
        if delta > 0:
            time_last = time.time()

            player_pos = getObjectPosition(board, '@')
            if len(path) == 0:
                path = calculatePath(board, player_pos)

            if len(path) > 0:
                target_pos = path.pop()
                target_object = board[target_pos[1]][target_pos[0]]
                if target_object.isalpha() and target_object.islower():
                    door = target_object.upper()
                    door_pos = getObjectPosition(board, door)
                    board[door_pos[1]][door_pos[0]] = ''

                board[player_pos[1]][player_pos[0]] = '.'
                board[target_pos[1]][target_pos[0]] = '@'

        screen.fill(black)
        screen.blit(board_surface, (0, 0))
        drawBoardObjects(screen, board, spr_w, font)
        pygame.display.flip()


# def calculatePath(board, player_pos):
#     key_locations = getKeyLocations(board)
#     bounds = (len(board[0]), len(board))
#     for k in key_locations:
#         result,path = getPathToTarget(board, bounds, player_pos, k)
#         if result:
#             return path
#     return []


def getPathToTarget(board, bounds, start, target):
    closed_set = {}
    open_set = {}
    started_pathing = False
    found_target = False
    while len(open_set) > 0 or not started_pathing:
        if not started_pathing:
            pos = (start, 0)
            started_pathing = True
        else:
            p = next(iter(open_set))
            pos = (p, open_set.pop(next(iter(open_set))))
        closed_set[pos[0]] = pos[1]
        adjacents = getValidAdjacents(board, bounds, pos[0], target)
        for a in adjacents:
            if a not in closed_set and a not in open_set:
                open_set[a] = pos[1] + 1
                if a == target:
                    found_target = True
                    break

    if found_target:
        path = [target]
        i = closed_set[target]
        current_pos = target
        while i > 1:
            adjacents = getValidAdjacents(board, bounds, current_pos, target)
            found_next = False
            for a in adjacents:
                if a in closed_set:
                    if closed_set[a] < i:
                        found_next = True
                        current_pos = a
                        i = closed_set[a]
                        path.append(a)
            if not found_next:
                print("Failed to walk back the path from the target")
                break

        return True,path
    else:
        return False,[]


def getValidAdjacents(board, bounds, current, target):
    adjacents = []
    if current[0] - 1 > 0:
        adjacents.append((current[0] - 1, current[1]))
    if current[1] - 1 > 0:
        adjacents.append((current[0], current[1] - 1))
    if current[0] + 1 < bounds[0]:
        adjacents.append((current[0] + 1, current[1]))
    if current[1] + 1 < bounds[1]:
        adjacents.append((current[0], current[1] + 1))

    output = []
    for a in adjacents:
        key = (board[a[1]][a[0]].isalpha() and board[a[1]][a[0]].islower())
        if key and a != target:
            continue

        empty = (board[a[1]][a[0]] == '.' or board[a[1]][a[0]] == '')
        if key or empty:
            output.append(a)
    return output


def getObjectPosition(board, target):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == target:
                return (x, y)
    # print("Failed to get the target object position")


def getKeyLocations(board):
    key_locations = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x].isalpha() and board[y][x].islower():
                key_locations.append((x, y))
    return key_locations


def generateBoard():
    input = open("day-18-input.txt").readlines()
    board = []
    for line in range(0, len(input)):
        board.append([])
        for c in range(0, len(input[line])):
            char = input[line][c]
            if char != '\n':
                board[line].append(char)
    return board


def drawBoardBase(surface, board, spr_w, font):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            xpos = int((x + 4) * spr_w)
            ypos = int((y + 4) * spr_w)

            tile_type = board[y][x]
            if tile_type == '#':
                pygame.draw.rect(
                    surface,
                    (200, 200, 200),
                    pygame.rect.Rect(xpos, ypos, spr_w, spr_w))
            elif tile_type == '.':
                text = font.render(tile_type, False, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (xpos + int(spr_w / 2), ypos + int(spr_w / 2))
                surface.blit(text, text_rect)


def drawBoardObjects(screen, board, spr_w, font):
    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            xpos = int((x + 4) * spr_w)
            ypos = int((y + 4) * spr_w)

            tile_type = board[y][x]
            if tile_type == '@':
                pygame.draw.rect(
                    screen,
                    (255, 50, 80),
                    pygame.rect.Rect(xpos, ypos, spr_w, spr_w))
            elif tile_type.isalpha():
                text = font.render(tile_type, False, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = (xpos + int(spr_w / 2), ypos + int(spr_w / 2))
                screen.blit(text, text_rect)


solve()