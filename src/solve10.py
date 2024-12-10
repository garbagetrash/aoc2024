import copy
import numpy as np


north = (0, -1)
east = (1, 0)
south = (0, 1)
west = (-1, 0)


def get_neighbors(point, m):
    neighbors = []
    for d in [north, east, south, west]:
        newp = (point[0] + d[0], point[1] + d[1])
        if newp in m:
            neighbors.append(newp)
    return neighbors


def count_tails(head, m):
    # Initialize
    levels = [set() for _ in range(10)]
    levels[0].add(head)

    # step up
    for l in range(9):
        for point in levels[l]:
            n = get_neighbors(point, m)
            for neighbor in n:
                if m[neighbor] == l + 1:
                    levels[l + 1].add(neighbor)
    return len(levels[9])


def trail_rating(head, m):
    # Initialize
    levels = [[] for _ in range(10)]
    levels[0].append([head])

    # step up
    for l in range(9):
        for path in levels[l]:
            n = get_neighbors(path[-1], m)
            for neighbor in n:
                if m[neighbor] == l + 1:
                    newpath = path + [neighbor]
                    levels[l + 1].append(newpath)
    return len(levels[9])


with open("../inputs/10.txt", "r") as fid:
    m = {}
    trailheads = set()
    xmax = 0
    ymax = 0
    for y, line in enumerate(fid.read().splitlines()):
        ymax += 1
        xmax = len(line)
        for x, c in enumerate(line):
            m[(x, y)] = int(c)
            if c == '0':
                trailheads.add((x, y))

    # Part 1
    cnt = 0
    for head in trailheads:
        cnt += count_tails(head, m)
    print(cnt)

    # Part 2
    cnt = 0
    for head in trailheads:
        cnt += trail_rating(head, m)
    print(cnt)
