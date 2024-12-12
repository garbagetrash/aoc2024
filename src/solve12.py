import copy
import numpy as np


north = np.array([0, -1], dtype=int)
east = np.array([1, 0], dtype=int)
south = np.array([0, 1], dtype=int)
west = np.array([-1, 0], dtype=int)


def get_neighbors(p, m):
    candidates = [tuple(np.array(p, dtype=int) + d) for d in [north, east, south, west]]
    output = []
    for c in candidates:
        if c in m.keys():
            output.append(c)
    return output

def get_connected(p0, m):
    ptype = m[p0]
    connected = set()
    frontier = set([p0])

    while True:
        next_frontier = set()
        for pt in frontier:
            for n in get_neighbors(pt, m):
                if n not in connected and n not in frontier and m[n] == ptype:
                    # New point
                    next_frontier.add(n)

        # Insert last frontier into output
        connected.update(frontier)

        # If next frontier empty we're done so bail
        if len(next_frontier) == 0:
            break
        else:
            frontier = next_frontier

    return connected


def count_perimeter(region, m):
    perimeter = 0
    rtype = m[list(region)[0]]
    for p in region:
        # TODO: need to count fences on outer border, get_neighbors won't return outer edges
        for n in get_neighbors(p, m):
            if m[n] != rtype:
                perimeter += 1
    return perimeter


with open("../inputs/12a.txt", "r") as fid:
    m = {}
    xmax = 0
    ymax = 0
    for y, line in enumerate(fid):
        ymax += 1
        xmax = len(line)
        for x, c in enumerate(line):
            m[(x, y)] = c

    # Part 1
    accum = 0
    explored1 = set()
    for y in range(ymax):
        for x in range(xmax):
            if (x, y) not in explored1:
                region = get_connected((x, y), m)
                perimeter = count_perimeter(region, m)
                accum += len(region) * perimeter
                print((x, y), len(region))
                explored1.update(region)
    print(accum)

    # Part 2
    print(0)
