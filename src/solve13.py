import copy
import numpy as np


def solve1(machine):
    # A button casts 3, B button costs 1
    a, b, prize = machine

    da = a[1] / a[0]
    db = b[1] / b[0]

    cost = 0
    while prize[0] > 0 and prize[1] > 0:
        if prize[0] % b[0] == 0 and prize[1] % b[1] == 0 and prize[0] / b[0] == prize[1] / b[1]:
            cost += int(prize[0] / b[0])
            return cost
        else:
            prize = (prize[0] - a[0], prize[1] - a[1])
            cost += 3
    return None

with open("../inputs/13.txt", "r") as fid:
    a = (0, 0)
    b = (0, 0)
    prize = (0, 0)
    machines = []
    for i, line in enumerate(fid):
        if (i + 1) % 4 == 0:
            machines.append((a, b, prize))
        else:
            moves = [x.strip() for x in line.split(':')[1].split(',')]
            if (i + 1) % 4 != 3:
                vals = tuple([int(x.split('+')[1]) for x in moves])
                if (i + 1) % 4 == 1:
                    a = vals
                else:
                    b = vals
                #print(f"BTN: {vals}")
            else:
                prize = tuple([int(x.split('=')[1]) for x in moves])
                #print(f"Prize: {prize}")


    # Part 1
    accum = 0
    for machine in machines:
        cost = solve1(machine)
        print(machine, cost)
        if cost:
            accum += cost
    print(accum)

    # Part 2
    accum = 0
    for machine in machines:
        a, b, prize = machine
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        machine = (machine[0], machine[1], prize)
        cost = solve1(machine)
        print(machine, cost)
        if cost:
            accum += cost
    print(accum)
