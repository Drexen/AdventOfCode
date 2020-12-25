def solve():
    card_pub_key = 12092626

    door_pub_key = 4707356
    door_loop_size = get_loop_size_from_public_key(door_pub_key, 7)

    enc_key = get_encryption_key(card_pub_key, door_loop_size)
    print(f"Part one = {enc_key}")


def get_loop_size_from_public_key(public_key, subject_number):
    value = 1
    loop_size = 1
    while 1:
        value *= subject_number
        value = value % 20201227
        if value == public_key:
            return loop_size
        loop_size += 1


def get_encryption_key(public_key, loop_size):
    value = 1
    subject_number = public_key
    for _ in range(0, loop_size):
        value *= subject_number
        value = value % 20201227
    return value


solve()
