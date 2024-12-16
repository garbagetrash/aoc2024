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


def print_moving(moving, m):
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if (x, y) in moving:
                print("X", end="")
            else:
                print(f"{c}", end="")
        print()
    print()


def calc_boxes(m):
    output = 0
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == 'O' or c == '[':
                output += 100*y + x
    return output


# Recursive check if movement possible
def can_move(pos, direction, m):
    nn = np.array(pos) + np.array(direction)
    ymax, xmax = m.shape

    # In bounds checks
    if nn[0] < 0 or nn[0] >= xmax:
        # Out of bounds
        return None
    if nn[1] < 0 or nn[1] >= ymax:
        # Out of bounds
        return None

    moving = []
    if m[nn[1], nn[0]] == '.':
        return moving
    elif m[nn[1], nn[0]] == '#':
        return None 
    elif m[nn[1], nn[0]] == '[':
        moving.append(tuple(nn))
        moving.append(tuple(nn + east))

        # A box - left side
        if direction is east or direction is west:
            newboxes = can_move(nn, direction, m)
            if newboxes is not None:
                moving += newboxes
                return moving
            else:
                return None
        else:
            # 2x as wide
            newboxes_l = can_move(nn, direction, m)
            newboxes_r = can_move(nn + east, direction, m)
            if newboxes_l is not None and newboxes_r is not None:
                moving += newboxes_l
                moving += newboxes_r
                return moving
            else:
                return None

    elif m[nn[1], nn[0]] == ']':
        moving.append(tuple(nn))
        moving.append(tuple(nn + west))

        # A box - right side
        if direction is east or direction is west:
            newboxes = can_move(nn, direction, m)
            if newboxes is not None:
                moving += newboxes
                return moving
            else:
                return None
        else:
            # 2x as wide
            newboxes_l = can_move(nn, direction, m)
            newboxes_r = can_move(nn + west, direction, m)
            if newboxes_l is not None and newboxes_r is not None:
                moving += newboxes_l
                moving += newboxes_r
                return moving
            else:
                return None


def move_boxes(pos, direction, m):
    nn = np.array(pos) + np.array(direction)

    if m[pos[1], pos[0]] == '[':
        if direction is east:
            nnn = np.array(pos) + 2*east
            if m[nnn[1], nnn[0]] != '.':
                move_boxes(nnn, direction, m)
            m[nnn[1], nnn[0]] = ']'
            m[nn[1], nn[0]] = '['
            m[pos[1], pos[0]] = '.'
        else:
            # North or South
            nn_l = nn
            nn_r = nn + east
            if m[nn_l[1], nn_l[0]] != '.':
                move_boxes(nn_l, direction, m)
            m[nn_l[1], nn_l[0]] = '['
            m[pos[1], pos[0]] = '.'
            if m[nn_r[1], nn_r[0]] != '.':
                move_boxes(nn_r, direction, m)
            m[nn_r[1], nn_r[0]] = ']'
            m[pos[1], pos[0] + 1] = '.'

    elif m[pos[1], pos[0]] == ']':
        if direction is west:
            nnn = np.array(pos) + 2*west
            if m[nnn[1], nnn[0]] != '.':
                move_boxes(nnn, direction, m)
            m[nnn[1], nnn[0]] = '['
            m[nn[1], nn[0]] = ']'
            m[pos[1], pos[0]] = '.'
        else:
            # North or South
            nn_l = nn + west
            nn_r = nn
            if m[nn_r[1], nn_r[0]] != '.':
                move_boxes(nn_r, direction, m)
            m[nn_r[1], nn_r[0]] = ']'
            m[pos[1], pos[0]] = '.'
            if m[nn_l[1], nn_l[0]] != '.':
                move_boxes(nn_l, direction, m)
            m[nn_l[1], nn_l[0]] = '['
            m[pos[1], pos[0] - 1] = '.'


def move2(pos, d, m):
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

    nn = np.array(pos) + d

    boxes_moving = can_move(pos, d, m)
    if boxes_moving is not None:
        # Move the robot and boxes
        move_boxes(nn, d, m)

        m[nn[1], nn[0]] = '@'
        m[pos[1], pos[0]] = '.'

        # Return where we moved bot to
        return nn
    else:
        # If we can't move, then just return current position
        return pos


def doubleit(m):
    output = []
    for row in m:
        newrow = []
        for c in row:
            if c == '.':
                newrow.append('.')
                newrow.append('.')
            elif c == '#':
                newrow.append('#')
                newrow.append('#')
            elif c == 'O':
                newrow.append('[')
                newrow.append(']')
            elif c == '@':
                newrow.append('@')
                newrow.append('.')
        output.append(newrow)
    return np.array(output)


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

    mm = np.array(copy.deepcopy(m))
    ymax, xmax = mm.shape

    # Part 1
    accum = 0
    p = copy.deepcopy(pos)
    for i in instructions:
        p = move(p, i, mm)
    print(calc_boxes(mm))

    # Part 2
    mm = doubleit(m)
    p = np.array([2*pos[0], pos[1]])
    print_map(mm)
    accum = 0
    for i in instructions:
        p = move2(p, i, mm)
        #print_map(mm)
    print(calc_boxes(mm))
