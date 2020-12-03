def solve():
    lines = open("day-3-input.txt").readlines()
    board = []
    for line in lines:
        row = []
        for c in line:
            if c == '.':
                row.append(False)
            if c == '#':
                row.append(True)
        board.append(row)
    board_w = len(row)

    one_one = get_num_trees(board, board_w, 1, 1)
    three_one = get_num_trees(board, board_w, 3, 1)
    five_one = get_num_trees(board, board_w, 5, 1)
    seven_one = get_num_trees(board, board_w, 7, 1)
    one_two = get_num_trees(board, board_w, 1, 2)

    print("Part one = " + str(three_one))
    print("Part two = " + str(one_one * three_one * five_one * seven_one * one_two))


def get_num_trees(board, board_w, dx, dy):
    num_trees = 0
    for y, row in enumerate(board):
        if y % dy == 0:
            x = (int(y / dy) * dx) % board_w
            if row[x]:
                num_trees = num_trees + 1
    return num_trees


solve()
