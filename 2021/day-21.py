ROLLS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


def solve():
    p1_wins, p2_wins = turn(5, 0, 6, 0, 1, {})
    print("Part two = " + str(max(p1_wins, p2_wins)))


def turn(p1_pos, p1_score, p2_pos, p2_score, player, states):
    if (p1_pos, p1_score, p2_pos, p2_score, player) in states:
        return states[(p1_pos, p1_score, p2_pos, p2_score, player)]

    p1_wins = 0
    p2_wins = 0
    for roll, occurence in ROLLS.items():
        (a, b) = turn_internal(p1_pos, p1_score, p2_pos, p2_score, player, states, roll)

        p1_wins += a * occurence
        p2_wins += b * occurence

    states[(p1_pos, p1_score, p2_pos, p2_score, player)] = (p1_wins, p2_wins)

    return p1_wins, p2_wins


def turn_internal(p1_pos, p1_score, p2_pos, p2_score, player, states, roll):
    if player == 1:
        p1_pos = ((p1_pos + roll - 1) % 10) + 1
        p1_score += p1_pos
        if p1_score >= 21:
            return 1, 0
    else:
        p2_pos = ((p2_pos + roll - 1) % 10) + 1
        p2_score += p2_pos
        if p2_score >= 21:
            return 0, 1

    return turn(p1_pos, p1_score, p2_pos, p2_score, (player % 2) + 1, states)


solve()

