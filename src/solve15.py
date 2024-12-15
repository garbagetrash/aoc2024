import copy
import numpy as np
import time


north = np.array([0, -1], dtype=int)
east = np.array([1, 0], dtype=int)
south = np.array([0, 1], dtype=int)
west = np.array([-1, 0], dtype=int)

# position direction map
def move(pos, d, m):
    if d == '^':
        d = north
    elif d == '>':
        d = east
    elif d == 'v':
        d = south
    elif d == '<':
        d = west
    else:
        raise ValueError("Invalid direction")

    ymax, xmax = m.shape

    move_allowed = False
    boxes_moving = []
    nn = np.array(pos)
    while True:
        nn += d

        # In bounds checks
        if nn[0] < 0 or nn[0] >= xmax:
            # Out of bounds
            break
        if nn[1] < 0 or nn[1] >= ymax:
            # Out of bounds
            break

        if m[nn[1], nn[0]] == '.':
            # Empty space, move allowed
            move_allowed = True
            break
        elif m[nn[1], nn[0]] == '#':
            # Hit a wall, move not allowed
            break
        elif m[nn[1], nn[0]] == 'O':
            # Box that might get moved
            boxes_moving.append(np.array([nn[0], nn[1]]))

    if move_allowed:
        # Move the robot and boxes
        for box in boxes_moving[::-1]:
            box_to = box + d
            m[box_to[1], box_to[0]] = 'O'
        m[pos[1], pos[0]] = '.'
        bot_to = pos + d
        m[bot_to[1], bot_to[0]] = '@'
        return bot_to
    else:
        return pos


def print_map(m):
    for row in m:
        for c in row:
            print(f"{c}", end="")
        print()
    print()


def calc_boxes(m):
    output = 0
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == 'O':
                output += 100*y + x
    return output


with open("../inputs/15.txt", "r") as fid:
    mapmode = True
    m = []
    instructions = []
    pos = np.array([0, 0])
    for y, line in enumerate(fid):
        if line == '\n':
            mapmode = False
            continue
        if mapmode:
            row = []
            for x, c in enumerate(line.strip()):
                row.append(c)
                if c == '@':
                    pos = np.array([x, y])
            m.append(row)
        else:
            for c in line.strip():
                instructions.append(c)
    m = np.array(m)
    ymax, xmax = m.shape
    print(m)
    print(xmax, ymax)
    print(pos)
    print(instructions)
    print_map(m)

    # Part 1
    accum = 0
    for i in instructions:
        pos = move(pos, i, m)
    print(calc_boxes(m))

    # Part 2
    accum = 0
    print(accum)
