import copy
import numpy as np
import time


def propagate(state, n, width, height):
    point, vel = state
    new_point_x = (point[0] + n*vel[0]) % width
    new_point_y = (point[1] + n*vel[1]) % height
    return ((new_point_x, new_point_y), vel)


# order: (NE, NW, SW, SE)
def quad_counts(states, width, height):
    midwidth = int(width / 2)
    midheight = int(height / 2)
    output = [0, 0, 0, 0]
    for state in states:
        p, _v = state
        if p[0] > midwidth:
            if p[1] < midheight:
                # NE
                output[0] += 1
            elif p[1] > midheight:
                # SE
                output[3] += 1
        elif p[0] < midwidth:
            if p[1] < midheight:
                # NW
                output[1] += 1
            elif p[1] > midheight:
                # SW
                output[2] += 1
    return output


def prop_all(states, n, width, height):
    output = []
    for state in states:
        output.append(propagate(state, n, width, height))
    return output


def print_states(states, width, height):
    points = [p for (p, v) in states]
    for y in range(height):
        for x in range(width):
            if (x, y) in points:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def find_min_var(states, width, height):
    vararr = []
    for i in range(10000):
        tmp = copy.deepcopy(states)
        tmp = prop_all(tmp, i, width, height)
        vararr.append(calc_var(tmp))

    minidx = np.argmin(vararr)
    print_states(prop_all(states, minidx, width, height), width, height)
    print(minidx)


def calc_var(states):
    points = [p for (p, v) in states]
    xs = np.array([x for (x, y) in points])
    ys = np.array([y for (x, y) in points])
    ps = np.array([x+1j*y for x, y in zip(xs, ys)])
    return np.var(ps)


with open("../inputs/14.txt", "r") as fid:
    states = []
    for i, line in enumerate(fid):
        point, vel = [x for x in line.split()]
        point = tuple([int(x) for x in point.split('=')[1].split(',')])
        vel = tuple([int(x) for x in vel.split('=')[1].split(',')])
        states.append((point, vel))

    print(len(states))

    width, height = 101, 103   # real dims
    #width, height = 11, 7    # example dims

    # Part 1
    accum = 0
    new_states = []
    for state in states:
        new_states.append(propagate(state, 100, width, height))
    quads = quad_counts(new_states, width, height)
    print(quads[0]*quads[1]*quads[2]*quads[3])

    # Part 2
    i = 0
    pstates = copy.deepcopy(states)
    find_min_var(states, width, height)
    """
    while True:
        pstates = prop_all(pstates, 1, width, height)
        i += 1
        print_states(pstates, width, height)
        print(f"i: {i}")
        time.sleep(0.4)
    """
