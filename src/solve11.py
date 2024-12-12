import sys
import copy
import numpy as np

cache = {}
size_cache = {}

def r(c, steps_left):
    c = int(c)
    try:
        return size_cache[(c, steps_left)]
    except:
        value = 0
        if steps_left == 0:
            value = 1
        else:
            if c == 0:
                value = r(1, steps_left - 1)
            elif len(str(c)) % 2 == 0:
                sn = str(c)
                x2 = int(len(sn) // 2)
                value = r(int(sn[:x2]), steps_left - 1) + r(sn[x2:], steps_left - 1)
            else:
                value = r(2024*c, steps_left - 1)
        size_cache[(c, steps_left)] = value
        return value

def apply(l):
    new = []
    for n in l:
        value = 0
        try:
            values = cache[(n, 1)]
        except:
            if n == 0:
                values = [1]
            elif len(str(n)) % 2 == 0:
                sn = str(n)
                x2 = int(len(sn) // 2)
                values = [int(sn[:x2]), int(sn[x2:])]
            else:
                values = [2024*n]
        new += values
    return new


with open("../inputs/11.txt", "r") as fid:
    m = []
    for n in fid.read().split():
        m.append(int(n))

    print(m)

    # Part 1
    mm = copy.deepcopy(m)
    for i in range(25):
        mm = apply(mm)
    print(len(mm))

    # Part 2
    accum = 0
    for c in m:
        value = r(c, 75)
        accum += value
    print(accum)
