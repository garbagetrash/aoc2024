def apply(values, n):
    # each n will correspond to a series of ops in binary form. + = 0 and * = 1
    # so n = 12 = 0b1100 = _ * _ * _ + _ + _
    nops = len(values) - 1
    accum = values[0]
    for i in range(nops):
        op = (n >> (nops - 1 - i)) & 0x0001
        if op:
            # multiply
            accum *= values[i + 1]
        else:
            accum += values[i + 1]
    return accum

def checkall(goal, values):
    nops = len(values) - 1
    for i in range(2 ** nops):
        test = apply(values, i)
        if test == goal:
            return True
    return False

def checkall2(goal, values):
    nops = len(values) - 1
    accums = [values[0]]
    for i in range(nops):
        accum_next = []
        # +
        for accum in accums:
            accum_next.append(accum + values[i + 1])
        # *
        for accum in accums:
            accum_next.append(accum * values[i + 1])
        # ||
        for accum in accums:
            accum_next.append(int(str(accum) + str(values[i + 1])))
        accums = accum_next

    for value in accums:
        if value == goal:
            return True

    return False

with open("../inputs/07.txt", "r") as fid:
    test_pairs = []
    for y, line in enumerate(fid):
        # Read first part
        s = line.split(':')
        test_value = int(s[0])
        values = [int(x) for x in s[1].split()]
        test_pairs.append((test_value, values))

    # Part 1
    accum = 0
    for pair in test_pairs:
        if checkall(pair[0], pair[1]):
            accum += pair[0]
    print(accum)

    # Part 2
    accum = 0
    for pair in test_pairs:
        if checkall2(pair[0], pair[1]):
            accum += pair[0]
    print(accum)
