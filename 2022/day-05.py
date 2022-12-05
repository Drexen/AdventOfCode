import re

NUM_STACKS = 9
COMMANDS_START = 11


def parse_stacks(input):
    stacks = [[] for _ in range(NUM_STACKS)]
    for line in input:
        for i, d in enumerate(line):
            if d.isalpha():
                stack_index = (i - 1) // 4
                stacks[stack_index].append(d)
    [s.reverse() for s in stacks]
    return stacks


def parse_commands(input):
    commands = []
    for line in input:
        command = []
        match = re.match("move (\\d+) from (\\d+) to (\\d+)", line)
        for c in match.groups():
            command.append(int(c))
        commands.append(command)
    return commands


def apply_command(stacks, command, move_stacks_in_order):
    crane = []
    for i in range(0, command[0]):
        if len(stacks[command[1] - 1]) > 0:
            crane.append(stacks[command[1] - 1].pop())

    if move_stacks_in_order:
        crane.reverse()
    for c in crane:
        stacks[command[2] - 1].append(c)


def get_message(stacks):
    message = ""
    for s in stacks:
        message += s[len(s) - 1]
    return message


def solve():
    input = open("day-05-input.txt").read().split('\n')
    stacks = parse_stacks(input[:NUM_STACKS])
    commands = parse_commands(input[COMMANDS_START - 1:])
    for c in commands:
        apply_command(stacks, c, move_stacks_in_order=False)
    print("Part one = " + get_message(stacks))

    stacks = parse_stacks(input[:NUM_STACKS])
    for c in commands:
        apply_command(stacks, c, move_stacks_in_order=True)
    print("Part two = " + get_message(stacks))


solve()
