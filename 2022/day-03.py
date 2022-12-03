def item_to_priority(item):
    value = ord(item) - 96
    if value < 1:
        value += 58
    return value


def calculate_rearrangement_priority(input):
    rucksack1 = input[0:int(len(input)/2)]
    rucksack2 = input[int(len(input)/2):]
    for item in rucksack1:
        if item in rucksack2:
           return item_to_priority(item)


def calculate_badge_priority(e1, e2, e3):
    for item in e1:
        if item in e2 and item in e3:
            return item_to_priority(item)


def solve():
    input = open("day-03-input.txt").readlines()
    total = sum([calculate_rearrangement_priority(i.strip()) for i in input])
    print("Part one = " + str(total))

    total = 0
    for i in range(0, len(input), 3):
        total += calculate_badge_priority(input[i], input[i+1], input[i+2])
    print("Part two = " + str(total))


solve()
