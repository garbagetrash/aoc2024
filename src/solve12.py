import copy
import numpy as np


north = np.array([0, -1], dtype=int)
east = np.array([1, 0], dtype=int)
south = np.array([0, 1], dtype=int)
west = np.array([-1, 0], dtype=int)


def get_neighbors(p, m):
    candidates = [(int(p[0] + d[0]), int(p[1] + d[1])) for d in [north, east, south, west]]
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
        candidates = [tuple(np.array(p, dtype=int) + d) for d in [north, east, south, west]]
        for n in candidates:
            try:
                if m[n] != rtype:
                    perimeter += 1
            except KeyError:
                perimeter += 1
    return perimeter

def print_hedges(edges, xmax, ymax):
    for y in range(ymax+1):
        for x in range(xmax+1):
            if (x, y-1) in edges:
                print('_', end="")
            else:
                print('.', end="")
        print()
    print()

def print_vedges(edges, xmax, ymax):
    for y in range(ymax+1):
        for x in range(xmax+1):
            if (x-1, y) in edges:
                print('|', end="")
            else:
                print('.', end="")
        print()
    print()

def count_perimeter2(region, m, xmax, ymax):
    rtype = m[list(region)[0]]
    hedges = set() # y represents the Northern grid point along the edge
    vedges = set() # x represents the Western grid point along the edge
    for p in region:
        for d in [north, east, south, west]:
            n = (int(p[0] + d[0]), int(p[1] + d[1]))
            try:
                if m[n] != rtype:
                    if n[0] > p[0]:
                        # Larger x implies vertical edge, along East side of p.
                        vedges.add(p)
                    elif n[0] < p[0]:
                        # Smaller x implies vertical edge, along West side of
                        # p.
                        vedges.add(n)
                    elif n[1] > p[1]:
                        # Larger y implies horizontal edge, along South side of
                        # p.
                        hedges.add(p)
                    elif n[1] < p[1]:
                        # Smaller y implies horizontal edge, along North side
                        # of p.
                        hedges.add(n)
            except KeyError:
                if d is north:
                    hedges.add((p[0], -1))
                elif d is south:
                    hedges.add(p)
                elif d is west:
                    vedges.add((-1, p[1]))
                elif d is east:
                    vedges.add(p)

    # We now have all edges in hedges and vedges, count sides and account for
    # edges as we go.
    hedges = list(hedges)
    vedges = list(vedges)
    hedges.sort()
    vedges.sort()
    #print(f"Horiz. Edges: {hedges}")
    #print(f"Vert. Edges : {vedges}")
    #print_hedges(hedges, xmax, ymax)
    #print_vedges(hedges, xmax, ymax)

    # Walk down rows
    nsides = 0
    seen = set()
    for y in range(-1, ymax):
        for x in range(-1, xmax):
            p = (x, y)
            if p in hedges and p not in seen:
                if p in region:
                    ptype = True
                else:
                    ptype = False
                seen.add(p)
                nsides += 1
                for xx in range(x + 1, xmax):
                    p2 = (xx, y)
                    if p2 in hedges:
                        if p2 in region:
                            p2type = True
                        else:
                            p2type = False
                        if ptype != p2type:
                            nsides += 1
                            ptype = p2type
                        seen.add(p2)
                    else:
                        # This indicates end of fence side
                        break

    # Walk down columns
    seen = set()
    for x in range(-1, xmax):
        for y in range(-1, ymax):
            p = (x, y)
            if p in vedges and p not in seen:
                if p in region:
                    ptype = True
                else:
                    ptype = False
                seen.add(p)
                nsides += 1
                for yy in range(y + 1, ymax):
                    p2 = (x, yy)
                    if p2 in vedges:
                        if p2 in region:
                            p2type = True
                        else:
                            p2type = False
                        if ptype != p2type:
                            nsides += 1
                            ptype = p2type
                        seen.add(p2)
                    else:
                        # This indicates end of fence side
                        break

    return nsides


with open("../inputs/12.txt", "r") as fid:
    m = {}
    xmax = 0
    ymax = 0
    for y, line in enumerate(fid):
        ymax += 1
        xmax = len(line) - 1
        for x, c in enumerate(line):
            m[(x, y)] = c

    print(xmax, ymax)

    # Part 1
    accum = 0
    explored1 = set()
    for y in range(ymax):
        for x in range(xmax):
            if (x, y) not in explored1:
                region = get_connected((x, y), m)
                perimeter = count_perimeter(region, m)
                accum += len(region) * perimeter
                print((x, y), len(region), perimeter)
                explored1.update(region)
    print(accum)

    # Part 2
    accum = 0
    explored2 = set()
    for y in range(ymax):
        for x in range(xmax):
            if (x, y) not in explored2:
                region = get_connected((x, y), m)
                perimeter = count_perimeter2(region, m, xmax, ymax)
                accum += len(region) * perimeter
                #print((x, y), len(region), perimeter)
                explored2.update(region)
    print(accum)
