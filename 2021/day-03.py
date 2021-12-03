WIDTH = 12


def solve():
    lines = [n for n in open("day-03-input.txt").readlines()]
    part_one(lines)
    part_two(lines)


def part_one(lines):
    gamma_arr = get_popular_digits(lines)

    gamma = 0
    for i in range(0, WIDTH):
        gamma *= 2
        gamma += gamma_arr[i]

    epsilon = pow(2, WIDTH) - gamma - 1

    power_consumption = gamma * epsilon
    print("Part one = " + str(power_consumption))


def part_two(lines):
    a = lines.copy()
    for i in range(0, WIDTH):
        popular_digits = get_popular_digits(a)
        a = [l for l in a if l[i] == str(popular_digits[i])]
        if (len(a) == 1):
            break

    oxygen_generator_rating = int(a[0], 2)

    for i in range(0, WIDTH):
        popular_digits = get_popular_digits(lines)
        lines = [l for l in lines if l[i] != str(popular_digits[i])]
        if (len(lines) == 1):
            break

    c02_scrubber_rating = int(lines[0], 2)

    life_support_rating = oxygen_generator_rating * c02_scrubber_rating
    print("Part two = " + str(life_support_rating))


def get_popular_digits(lines):
    gamma_arr = [0] * WIDTH
    for line in lines:
        for i in range(0, WIDTH):
            if line[i] == '1':
                gamma_arr[i] += 1

    for i in range(0, WIDTH):
        if gamma_arr[i] / len(lines) >= 0.5:
            gamma_arr[i] = 1
        else:
            gamma_arr[i] = 0
    return gamma_arr


solve()
