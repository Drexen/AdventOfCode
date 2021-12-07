def solve():
    lines = [n for n in open("day-07-input.txt").readlines()]
    positions = [int(n) for n in lines[0].split(",")]

    part_one(positions)
    part_two(positions)


def part_one(positions):
    positions.sort()
    target = positions[int(len(positions) / 2)]
    fuel = sum([abs(target - n) for n in positions])
    print("Part one = " + str(fuel))


def part_two(positions):
    target = int(sum(positions) / len(positions))
    fuel_floor = sum([(abs(target - n) + 1) * abs(target - n) / 2 for n in positions])
    target += 1
    fuel_ceil = sum([(abs(target - n) + 1) * abs(target - n) / 2 for n in positions])
    print("Part two = " + str(int(min(fuel_floor, fuel_ceil))))


solve()
