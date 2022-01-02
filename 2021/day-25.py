import copy


def solve():
    board = [[x for x in y] for y in open("day-25-input.txt").read().splitlines()]
    w = len(board[0])
    h = len(board)

    i = 0
    while True:
        i += 1
        (something_moved, new_board) = step(board, w, h)
        if not something_moved:
            break
        if i % 100 == 0:
            print(i)
        board = new_board

    print("Settled at: " + str(i))


def step(board, w, h):
    something_moved = False
    new_board = copy.deepcopy(board)
    for y in range(0, h):
        for x in range(0, w):
            if board[y][x] != ">":
                continue

            new_x = (x + 1) % w
            new_y = y

            if board[new_y][new_x] == ".":
                new_board[new_y][new_x] = board[y][x]
                new_board[y][x] = "."
                something_moved = True

    board = copy.deepcopy(new_board)
    for y in range(0, h):
        for x in range(0, w):
            if board[y][x] != "v":
                continue

            new_x = x
            new_y = (y + 1) % h

            if board[new_y][new_x] == ".":
                new_board[new_y][new_x] = board[y][x]
                new_board[y][x] = "."
                something_moved = True

    return something_moved, new_board


def print_board(board):
    for y in board:
        line = ""
        for x in y:
            line += str(x)
        print(line)


solve()
