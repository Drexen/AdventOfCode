results_p1 = {
    'A': {
        "X": 4,
        "Y": 8,
        "Z": 3
    },
    "B": {
        "X": 1,
        "Y": 5,
        "Z": 9
    },
    "C": {
        "X": 7,
        "Y": 2,
        "Z": 6
    }
}

results_p2 = {
    'A': {
        "X": 3,
        "Y": 4,
        "Z": 8
    },
    "B": {
        "X": 1,
        "Y": 5,
        "Z": 9
    },
    "C": {
        "X": 2,
        "Y": 6,
        "Z": 7
    }
}


def solve():
    input = [x.strip().split(' ') for x in open("day-02-input.txt").readlines()]
    print("Part one = " + str(sum(map(lambda i: results_p1[i[0]][i[1]], input))))
    print("Part two = " + str(sum(map(lambda i: results_p2[i[0]][i[1]], input))))


solve()
