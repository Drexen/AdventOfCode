# Brutal
# Part one done in excel in 2 minutes


def solve():
    data = [(i, int(x)) for i, x in enumerate(open("day-13-input.txt").readlines()[0].split(",")) if x != "x"]

    start = data[0][0]
    step = data[0][1]
    _iter = iter(data)
    next(_iter)
    for d in _iter:
        b_offs = d[1] - d[0]
        start = calculate_crt(step, start, d[1], b_offs)
        step *= d[1]
        start = start % step

    print("Part two = " + str(start))


# https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
def calculate_crt(a, a_offs, b, b_offs):
    x1 = get_mod_inverse(b, a)
    x2 = get_mod_inverse(a, b)

    s1 = a_offs * b * x1
    s2 = b_offs * a * x2

    return s1 + s2


# https://cp-algorithms.com/algebra/module-inverse.html
def get_mod_inverse(a, b):
    x, y = get_bézout_coefficients(a, b)
    x = ((x % b) + b) % b
    return x


# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def get_bézout_coefficients(a, b):

    old_r = a
    r = b
    old_s = 1
    s = 0
    old_t = 0
    t = 1

    while r != 0:
        quotient = (old_r // r)  # floor division

        r, old_r = old_r - quotient * r, r
        s, old_s = old_s - quotient * s, s
        t, old_t = old_t - quotient * t, t

    assert(old_r == 1)  # no solution

    return old_s, old_t


solve()
