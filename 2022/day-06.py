def find_marker(data, marker_length):
    for i in range(0, len(data) - marker_length + 1):
        found_marker = True
        working_data = data[i:i+marker_length]
        working_data.sort()
        for x in range(0, marker_length - 1):
            if working_data[x] == working_data[x + 1]:
                found_marker = False
                break
        if found_marker:
            return i + marker_length
    return -1


def solve():
    input = list(open("day-06-input.txt").read())

    start_of_packet_index = find_marker(input, 4)
    print("Part one = " + str(start_of_packet_index))

    start_of_message_index = find_marker(input, 14)
    print("Part two = " + str(start_of_message_index))


solve()
