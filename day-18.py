import sys, pygame, time


def solve():
    spr_w = 8
    board_w = 100
    board_h = 100

    pygame.init()

    font = pygame.font.Font("consola.ttf", spr_w)

    board = generateBoard()

    size = board_w * spr_w, board_h * spr_w
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    board_surface = pygame.Surface(size)
    drawBoardBase(board_surface, board, spr_w, font)

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


def calculatePath(board, player_pos):
    key_locations = getKeyLocations(board)
    bounds = (len(board[0]), len(board))
    for k in key_locations:
        result,path = getPathToTarget(board, bounds, player_pos, k)
        if result:
            return path
    return []


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
        adjacents = getValidAdjacents(board, bounds, pos[0])
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
            adjacents = getValidAdjacents(board, bounds, current_pos)
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


def getValidAdjacents(board, bounds, target):
    adjacents = []
    if target[0] - 1 > 0:
        adjacents.append((target[0] - 1, target[1]))
    if target[1] - 1 > 0:
        adjacents.append((target[0], target[1] - 1))
    if target[0] + 1 < bounds[0]:
        adjacents.append((target[0] + 1, target[1]))
    if target[1] + 1 < bounds[1]:
        adjacents.append((target[0], target[1] + 1))

    output = []
    for a in adjacents:
        key = (board[a[1]][a[0]].isalpha() and board[a[1]][a[0]].islower())
        empty = (board[a[1]][a[0]] == '.' or board[a[1]][a[0]] == '')
        if key or empty:
            output.append(a)
    return output


def getObjectPosition(board, target):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == target:
                return (x, y)
    print("Failed to get the target object position")


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