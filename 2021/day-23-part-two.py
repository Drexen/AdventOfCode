import sys, time

MOVE_COSTS = [1, 1, 1, 1, 10, 10, 10, 10, 100, 100, 100, 100, 1000, 1000, 1000, 1000]

AMPHIPOD_INDEX_TO_TYPE = [
    "A",
    "A",
    "A",
    "A",
    "B",
    "B",
    "B",
    "B",
    "C",
    "C",
    "C",
    "C",
    "D",
    "D",
    "D",
    "D",
]


def solve():
    board = [list(l) for l in open("day-23-part-two-input.txt").read().splitlines()[1:-1]]

    amphipods = get_amphipods_from_board(board)

    cost = find_solution(amphipods, sys.maxsize)
    print("Part two = " + str(cost))


def get_amphipods_from_board(board):
    amphipods = [(-1, -1) for _ in range(0, 16)]
    ai = 0
    bi = 4
    ci = 8
    di = 12

    for y, line in enumerate(board):
        for x, c in enumerate(line):
            if c == "A":
                amphipods[ai] = (x - 1, y)
                ai += 1
            if c == "B":
                amphipods[bi] = (x - 1, y)
                bi += 1
            if c == "C":
                amphipods[ci] = (x - 1, y)
                ci += 1
            if c == "D":
                amphipods[di] = (x - 1, y)
                di += 1

    assert (ai == 4)
    assert (bi == 8)
    assert (ci == 12)
    assert (di == 16)

    return amphipods


def find_solution(amphipods, current_best):
    possible_boards_data = generate_all_new_possible_boards(amphipods, 0)

    start = time.perf_counter()

    previous_states = {}

    i = 0
    while len(possible_boards_data) > 0:
        possible_board, cost = possible_boards_data.pop()
        hash = get_board_hash(possible_board)
        if hash in previous_states:
            previous_cost = previous_states[hash]
            if cost >= previous_cost:
                continue
        previous_states[hash] = cost

        if cost >= current_best:
            continue
        if board_completed_state(possible_board):
            current_best = cost
            continue

        a = generate_all_new_possible_boards(possible_board, cost)
        possible_boards_data.extend(a)

        if i % 10_000 == 0 and i > 0:
            elapsed = time.perf_counter() - start
            iter_sec = elapsed / (i / 10_000)
            print("{:.2f}".format(iter_sec) + "s per 10k iterations. " + str(len(previous_states)) + " previous states. Best = " + str(current_best))
        i += 1

    return current_best


def get_board_hash(amphipods):
    r = 0
    for i in range(0, 16):
        r += amphipods[i][0] << (i * 4)
    return r


def generate_all_new_possible_boards(amphipods, cost):
    possible_boards_data = []
    for i in range(0, len(amphipods)):
        new_possible_boards = generate_possible_boards(amphipods, i, cost)
        possible_boards_data.extend(new_possible_boards)
    return possible_boards_data


def board_completed_state(amphipods):
    for i, a in enumerate(amphipods):
        if a[0] != 2 + (int(i / 4) * 2):
            return False
    return True


def generate_possible_boards(amphipods, amphipod_index, cost):
    output = []
    valid_tiles = get_valid_tiles(amphipods, amphipod_index)
    for tile_pos in valid_tiles.keys():
        new_cost = cost + valid_tiles[tile_pos]
        new_amphipods = amphipods.copy()
        new_amphipods[amphipod_index] = tile_pos
        output.append((new_amphipods, new_cost))
    return output


def get_valid_tiles(amphipods, amphipod_index):
    valid_tiles = {}
    open_set = {}
    closed_set = set()
    open_set[amphipods[amphipod_index]] = 0
    move_cost = MOVE_COSTS[amphipod_index]
    current_pos = amphipods[amphipod_index]
    amphipod_type = AMPHIPOD_INDEX_TO_TYPE[amphipod_index]

    while len(open_set) > 0:
        test_pos = next(iter(open_set))
        new_cost = open_set[test_pos] + move_cost
        open_set.pop(test_pos)

        if test_pos[1] == 0:
            if test_pos[0] > 0:
                new_pos = (test_pos[0] - 1, test_pos[1])
                try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                                  valid_tiles)
            if test_pos[0] < 10:
                new_pos = (test_pos[0] + 1, test_pos[1])
                try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                                  valid_tiles)
            if test_pos[0] == 2 or test_pos[0] == 4 or test_pos[0] == 6 or test_pos[0] == 8:
                new_pos = (test_pos[0], test_pos[1] + 1)
                try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                                  valid_tiles)
        elif test_pos[1] == 1 or test_pos[1] == 2 or test_pos[1] == 3:
            new_pos = (test_pos[0], test_pos[1] + 1)
            try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                              valid_tiles)
            new_pos = (test_pos[0], test_pos[1] - 1)
            try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                              valid_tiles)
        else:
            new_pos = (test_pos[0], test_pos[1] - 1)
            try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set,
                              valid_tiles)

    return valid_tiles


def try_add_neighbour(amphipods, amphipod_type, current_pos, new_pos, new_cost, open_set, closed_set, valid_tiles):
    if new_pos not in open_set and \
            new_pos not in closed_set and \
            is_empty_tile(amphipods, new_pos):
        open_set[new_pos] = new_cost
        closed_set.add(new_pos)

        # prevent moving out of locked in correct place in a room
        if amphipod_type == "A" and current_pos[0] == 2:
            if does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, current_pos):
                return
        if amphipod_type == "B" and current_pos[0] == 4:
            if does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, current_pos):
                return
        if amphipod_type == "C" and current_pos[0] == 6:
            if does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, current_pos):
                return
        if amphipod_type == "D" and current_pos[0] == 8:
            if does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, current_pos):
                return

        if new_pos[1] == 0:
            # block positions directly outside of side rooms
            if new_pos[0] == 2 or new_pos[0] == 4 or new_pos[0] == 6 or new_pos[0] == 8:
                return

            # prevent moving from hallway to hallway
            if current_pos[1] == 0 and new_pos[1] == 0:
                return
        else:
            # prevent moving from room to incorrect room
            if amphipod_type == "A" and new_pos[0] != 2:
                return
            if amphipod_type == "B" and new_pos[0] != 4:
                return
            if amphipod_type == "C" and new_pos[0] != 6:
                return
            if amphipod_type == "D" and new_pos[0] != 8:
                return

            # prevent moving into room with other type of amphipod inside
            if not does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, new_pos):
                return

        valid_tiles[new_pos] = new_cost


def does_side_room_contain_only_matching_amphipod_type(amphipods, amphipod_type, current_pos):
    for i in range(current_pos[1] + 1, 5):
        if amphipod_type != get_amphipod_type_from_position(amphipods, (current_pos[0], i)):
            return False
    return True


def is_empty_tile(amphipods, pos):
    for a in amphipods:
        if a == pos:
            return False
    return True


def get_amphipod_type_from_position(amphipods, pos):
    for i, a in enumerate(amphipods):
        if a == pos:
            return AMPHIPOD_INDEX_TO_TYPE[i]
    return None


solve()
