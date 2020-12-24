def solve():
    inputs = [int(cup) - 1 for cup in open("day-23-input.txt").readline()]

    part_one(inputs)
    part_two(inputs)


def part_one(inputs):
    cups = []
    for i in range(0, 9):
        current_value_pos = inputs.index(i)
        next_value_pos = (current_value_pos + 1) % 9
        next_value = inputs[next_value_pos]
        cups.append(next_value)

    result = run_game(cups.copy(), inputs[0], 100)
    result = to_game_state(result, 1)
    one_index = result.index(1)
    answer = "".join(str(x) for x in result[one_index + 1:] + result[0:one_index])
    print(f"Part one = {answer}")


def part_two(inputs):
    cups = []
    for i in range(0, 9):
        current_value_pos = inputs.index(i)
        next_value_pos = (current_value_pos + 1) % 9
        next_value = inputs[next_value_pos]
        cups.append(next_value)

    last_value = inputs[len(inputs) - 1]
    cups[last_value] = 9
    cups.extend(range(10, 1_000_000))
    cups.append(inputs[0])

    result = run_game(cups.copy(), inputs[0], 10_000_000)
    first_adjacent = result[0]
    second_adjacent = result[first_adjacent]
    answer = (first_adjacent + 1) * (second_adjacent + 1)
    print(f"Part two = {answer}")


def run_game(cups, current, iterations):
    total_cups = len(cups)

    for x in range(0, iterations):
        first_to_remove = cups[current]
        second_to_remove = cups[first_to_remove]
        third_to_remove = cups[second_to_remove]
        first_to_keep = cups[third_to_remove]

        cups[current] = first_to_keep

        target = current
        while 1:
            target = (target + total_cups - 1) % total_cups
            if target != first_to_remove and target != second_to_remove and target != third_to_remove:
                break

        first_after_target = cups[target]
        cups[target] = first_to_remove
        cups[third_to_remove] = first_after_target
        current = first_to_keep

    return cups


def to_game_state(cups, first_value):
    game_state = [first_value]
    for _ in range(1, len(cups)):
        last_value = game_state[len(game_state) - 1]
        game_state.append(cups[last_value - 1] + 1)
    return game_state


solve()
