import re
import copy


def solve():
    partOne()
    partTwo()


def partOne():
    positions = getData()
    velocities = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    num_moons = len(positions)

    for _ in range(0, 1000):
        # apply gravity
        for a in range(0, num_moons):
            for b in range(a + 1, num_moons):
                if a != b:
                    for i in range(0, 3):
                        if positions[a][i] > positions[b][i]:
                            velocities[a][i] -= 1
                            velocities[b][i] += 1
                        elif positions[a][i] < positions[b][i]:
                            velocities[a][i] += 1
                            velocities[b][i] -= 1

        # apply velocity
        for a in range(0, num_moons):
            for i in range(0, 3):
                positions[a][i] = positions[a][i] + velocities[a][i]

    total_energy = 0
    for i in range(0, num_moons):
        potential = 0
        kinetic = 0
        for p in positions[i]:
            potential += abs(p)
        for k in velocities[i]:
            kinetic += abs(k)
        total_energy += (potential * kinetic)

    print("PartOne - Total system energy = " + str(total_energy))


def partTwo():
    x = getItersToMatchOriginalsOnAxis(0)
    y = getItersToMatchOriginalsOnAxis(1)
    z = getItersToMatchOriginalsOnAxis(2)

    a = x * y / gcd(x, y)
    b = a * z / gcd(a, z)

    print("PartTwo: Num iters to original = " + str(int(b)))


def gcd(a, b):
    while b > 0:
        temp = b
        b = a % b
        a = temp

    return a


def getItersToMatchOriginalsOnAxis(axis):
    positions = getData()
    velocities = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    num_moons = len(positions)

    positions_original = copy.deepcopy(positions)
    velocities_original = copy.deepcopy(velocities)

    iter = 0
    while True:
        iter += 1
        # apply gravity
        for a in range(0, num_moons):
            for b in range(a + 1, num_moons):
                if a != b:
                    i = axis
                    if positions[a][i] > positions[b][i]:
                        velocities[a][i] -= 1
                        velocities[b][i] += 1
                    elif positions[a][i] < positions[b][i]:
                        velocities[a][i] += 1
                        velocities[b][i] -= 1

        # apply velocity
        for a in range(0, num_moons):
            i = axis
            positions[a][i] = positions[a][i] + velocities[a][i]

        if positions == positions_original and velocities == velocities_original:
            break

    return iter


def getData():
    input = open("day-12-input.txt").readlines()
    pattern = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'
    positions = []
    for i in input:
        position = []
        matches = re.match(pattern, i)
        position.append(int(matches.group(1)))
        position.append(int(matches.group(2)))
        position.append(int(matches.group(3)))
        positions.append(position)

    return positions


solve()