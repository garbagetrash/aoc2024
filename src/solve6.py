import copy
import numpy as np


north = np.array([0, -1], dtype=int)
east = np.array([1, 0], dtype=int)
south = np.array([0, 1], dtype=int)
west = np.array([-1, 0], dtype=int)

def simulate(obs_loc, mm, guard, gdir):
    # set our obstruction
    m = copy.deepcopy(mm)
    m[tuple(obs_loc)] = 1
    state = set()
    state.add((tuple(guard), tuple(gdir)))
    while True:
        nextpos = guard + gdir
        #print(guard, gdir, nextpos)
        try:
            tile = m[tuple(nextpos)]
            #print(tile)
            if tile == 0:
                # open
                guard = nextpos
                newstate = (tuple(guard), tuple(gdir))
            else:
                # blocked - rotate right
                if gdir[1] == north[1]:
                    gdir = east
                elif gdir[0] == east[0]:
                    gdir = south
                elif gdir[1] == south[1]:
                    gdir = west
                else:
                    gdir = north
                newstate = (tuple(guard), tuple(gdir))
            #print(newstate)
            if newstate in state:
                return True
            else:
                state.add(newstate)
        except:
            # left the area
            return False

with open("../inputs/06.txt", "r") as fid:
    m = {}
    visited = set()
    guard_init = np.array([0, 0], dtype=int)
    gdir = north # North direction
    xmax = 0
    ymax = 0
    for y, line in enumerate(fid):
        ymax += 1
        xmax = len(line)
        for x, c in enumerate(line):
            if c == '^':
                guard_init = np.array([x, y], dtype=int)
                visited.add((x, y))
                m[(x, y)] = 0
            elif c == '#':
                m[(x, y)] = 1
            else:
                m[(x, y)] = 0

    # Part 1
    accum = 0
    guard = copy.deepcopy(guard_init)
    while True:
        nextpos = guard + gdir
        #print(guard, gdir, nextpos)
        try:
            tile = m[tuple(nextpos)]
            if tile == 0:
                # open
                guard = nextpos
                visited.add((nextpos[0], nextpos[1]))
            else:
                # blocked - rotate right
                if gdir[1] == north[1]:
                    gdir = east
                elif gdir[0] == east[0]:
                    gdir = south
                elif gdir[1] == south[1]:
                    gdir = west
                else:
                    gdir = north
        except:
            # left the area
            break
    print(len(visited))

    # Part 2
    accum = 0
    for (x, y) in visited:
        if simulate((x, y), m, guard_init, north):
            print(x, y)
            accum += 1
    print(accum)
