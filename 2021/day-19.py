import copy

scanner_offsets = [[0, 0, 0]]


def solve():
    scanners = [parse_scanner(s) for s in open("day-19-input.txt").read().split("\n\n")]

    scanners = [generate_orientations(s) for s in scanners]

    solved_scanners = [scanners[0][0]]
    unsolved_scanners = {}
    checked_pairs = set()
    for (i, s) in enumerate(scanners[1:]):
        unsolved_scanners[i] = s

    while len(unsolved_scanners) > 0:
        solve_scanner(solved_scanners, unsolved_scanners, checked_pairs)

    beacons = []
    for s in solved_scanners:
        for p in s:
            if p not in beacons:
                beacons.append(p)
    print("Part one = " + str(len(beacons)))

    max_distance = 0
    for a in range(0, len(scanner_offsets) - 1):
        for b in range(a + 1, len(scanner_offsets)):
            x = scanner_offsets[a]
            y = scanner_offsets[b]
            distance = abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
            max_distance = max(distance, max_distance)
    print("Part two = " + str(max_distance))


def solve_scanner(solved_scanners, unsolved_scanners, checked_pairs):
    for a in range(0, len(solved_scanners)):
        for b in unsolved_scanners.keys():
            if (a, b) not in checked_pairs:
                (result, offset) = check_overlap_scanners(solved_scanners[a], unsolved_scanners[b])
                checked_pairs.add((a, b))
                if result is not None:
                    solved_scanners.append(result)
                    scanner_offsets.append(offset)
                    print("Solved scanner")
                    unsolved_scanners.pop(b)
                    return


def check_overlap_scanners(scanner_a, scanner_b):
    for b in range(0, len(scanner_b)):
        (result, offset) = check_overlap_points(scanner_a, scanner_b[b])
        if result is not None:
            return (result, offset)
    return (None, None)


def check_overlap_points(points_a, points_b):
    for a in range(0, len(points_a) - 11):
        for b in range(0, len(points_b)):
            offset = subtract(points_a[a], points_b[b])
            translated_b = [add(b, offset) for b in points_b]

            if is_valid_overlap(points_a, translated_b):
                return (translated_b, offset)
    return (None, None)


def is_valid_overlap(points_a, points_b):
    num_matching = 0
    for a in points_a:
        if a in points_b:
            num_matching += 1
    return num_matching >= 12


def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def subtract(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def generate_orientations(points):
    orientations = []

    p = copy.deepcopy(points)
    for i in range(0, 4):
        rotate(p, 0)
        orientations.append(copy.deepcopy(p))

    for _ in range(0, 3):
        rotate(p, 1)

        for i in range(0, 4):
            rotate(p, 0)
            orientations.append(copy.deepcopy(p))

    rotate(p, 2)

    for i in range(0, 4):
        rotate(p, 0)
        orientations.append(copy.deepcopy(p))

    rotate(p, 2)
    rotate(p, 2)

    for i in range(0, 4):
        rotate(p, 0)
        orientations.append(copy.deepcopy(p))

    return orientations


def rotate(points, axis):
    a = (axis + 1) % 3
    b = (axis + 2) % 3
    for i in range(0, len(points)):
        x = points[i][a]
        points[i][a] = points[i][b]
        points[i][b] = -x


def parse_scanner(input):
    points_str = input.split("\n")[1:]
    points = []
    for i in range(0, len(points_str)):
        p = [int(a) for a in points_str[i].split(",")]
        points.append(p)
    return points


solve()

