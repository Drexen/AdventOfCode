from lark import Lark


def solve():
    grammar = "start:r0\n"
    inputs = []
    for line in open("day-19-input.txt").readlines():
        split = line.split(":")
        if len(split) == 2:
            rule_name = "r" + str(split[0])
            rule = split[1]
            if rule[1] != "\"":
                rule = rule.replace(" ", " r").replace("r|", "|")
            grammar += rule_name + " :" + rule
        else:
            input = split[0].strip("\n")
            if len(input) > 0:
                inputs.append(input)

    print(f"Part one = {exec(grammar, inputs)}")

    grammar = grammar.replace("r8 : r42", "r8 : r42 | r42 r8")
    grammar = grammar.replace("r11 : r42 r31", "r11 : r42 r31 | r42 r11 r31")

    print(f"Part two = {exec(grammar, inputs)}")


def exec(grammar, inputs):

    lark = Lark(grammar)

    count = 0
    for input in inputs:
        try:
            lark.parse(input)
        except:
            continue
        count += 1

    return count


solve()
