def solve():
    lines = open("day-15-input.txt").readlines()
    board = []
    for line in lines:
        board.append([int(x) for x in line.strip("\n")])

    print("Part one = " + str(get_path_risk(board)))

    width = len(board[0])
    height = len(board)
    for y in range(0, height):
        for i in range(1, 5):
            for j in range(0, width):
                board[y].append(((board[y][j] + i - 1) % 9) + 1)

    for i in range(1, 5):
        for y in range(0, height):
            board.append([((x + i - 1) % 9) + 1 for j, x in enumerate(board[y])])

    print("Part two = " + str(get_path_risk(board)))


def get_path_risk(board):
    width = len(board[0])
    height = len(board)

    open_set = set()
    open_set.add((0, 0))
    g_scores = {(0, 0):0}
    f_scores = {(0, 0):get_f_score(0, 0, width, height, g_scores[(0, 0)])}

    while len(open_set) > 0:
        current = min([(x, y, f_scores[(x, y)]) for (x, y) in open_set], key=lambda k: k[2])
        current = (current[0], current[1])
        open_set.remove(current)

        if current == (width - 1, height - 1):
            return g_scores[(current[0], current[1])]

        current_g_score = g_scores[current]
        try_add_neighbour(board, width, height, current[0] - 1, current[1], current_g_score, open_set, g_scores, f_scores)
        try_add_neighbour(board, width, height, current[0] + 1, current[1], current_g_score, open_set, g_scores, f_scores)
        try_add_neighbour(board, width, height, current[0], current[1] - 1, current_g_score, open_set, g_scores, f_scores)
        try_add_neighbour(board, width, height, current[0], current[1] + 1, current_g_score, open_set, g_scores, f_scores)

    return g_scores[(width - 1, height - 1)]


def try_add_neighbour(board, w, h, x, y, current_g_score, open_set, g_scores, f_scores):
    if 0 <= x < w and 0 <= y < h:
        new_g_score = current_g_score + board[y][x]
        if (x, y) in g_scores and new_g_score >= g_scores[(x, y)]:
            return

        open_set.add((x, y))
        g_scores[(x, y)] = new_g_score

        new_f_score = get_f_score(x, y, w, h, new_g_score)
        f_scores[(x, y)] = new_f_score


def get_f_score(x, y, w, h, g_score):
    return (w - x) + (h - y) + g_score


solve()
