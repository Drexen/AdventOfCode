def part_one(trees, height, width):
    visibles = [[0 for x in range(0, width)] for y in range(0, height)]

    # rows left->right
    for y in range(1, height-1):
        current_tree_height = trees[y][0]
        for x in range(1, width-1):
            if trees[y][x] > current_tree_height:
                visibles[y][x] = 1
                current_tree_height = trees[y][x]

    # rows right->left
    for y in range(1, height - 1):
        current_tree_height = trees[y][-1]
        for x in range(width - 2, 0, -1):
            if trees[y][x] > current_tree_height:
                visibles[y][x] = 1
                current_tree_height = trees[y][x]

    # columns top->bottom
    for x in range(1, width - 1):
        current_tree_height = trees[0][x]
        for y in range(1, height-1):
            if trees[y][x] > current_tree_height:
                visibles[y][x] = 1
                current_tree_height = trees[y][x]

    # columns bottom->top
    for x in range(1, width - 1):
        current_tree_height = trees[-1][x]
        for y in range(height - 2, 0, -1):
            if trees[y][x] > current_tree_height:
                visibles[y][x] = 1
                current_tree_height = trees[y][x]

    num_visible = sum([sum(v) for v in visibles]) + height + height + width + width - 4
    print("Part one = " + str(num_visible))


def calculate_scenic_score(trees, height, width, xt, yt):
    target_tree = trees[yt][xt]
    scenic_score = 1

    # left
    for x in range(xt - 1, -1, -1):
        if trees[yt][x] >= target_tree:
            break
    scenic_score *= (xt - x)

    # right
    for x in range(xt + 1, width):
        if trees[yt][x] >= target_tree:
            break
    scenic_score *= (x - xt)

    # up
    for y in range(yt - 1, -1, -1):
        if trees[y][xt] >= target_tree:
            break
    scenic_score *= (yt - y)

    # down
    for y in range(yt + 1, height):
        if trees[y][xt] >= target_tree:
            break
    scenic_score *= (y - yt)

    return scenic_score


def part_two(trees, height, width):
    scenic_scores = [[0 for x in range(0, width)] for y in range(0, height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            scenic_scores[y][x] = calculate_scenic_score(trees, height, width, x, y)

    max_scenic_score = max(max(x) for x in scenic_scores)
    print("Part two = " + str(max_scenic_score))


def solve():
    trees = [[int(c) for c in line] for line in open("day-08-input.txt").read().splitlines()]
    height = len(trees)
    width = len(trees[0])
    part_one(trees, height, width)
    part_two(trees, height, width)


solve()
