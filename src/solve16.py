import copy
import numpy as np
import time


north = np.array([0, -1], dtype=int)
east = np.array([1, 0], dtype=int)
south = np.array([0, 1], dtype=int)
west = np.array([-1, 0], dtype=int)


def print_map(m, xmax, ymax):
    for y in range(ymax):
        for x in range(xmax):
            print(f"{m[(x, y)]}", end="")
        print()
    print()


def print_path(m, path, xmax, ymax):
    for y in range(ymax):
        for x in range(xmax):
            if (x, y) in path:
                print("X", end="")
            else:
                print(f"{m[(x, y)]}", end="")
        print()
    print()


def get_neighbors(p, m):
    candidates = [(int(p[0] + d[0]), int(p[1] + d[1])) for d in [north, east, south, west]]
    output = []
    for c in candidates:
        if c in m.keys() and m[c] != '#':
            output.append(c)
    return output


"""
Idea:
    Create structure (tuple?) that has (score, dir, path). After each path
    update, do a .sort() by the score. Then we'll naturally explore the lowest
    score paths first and should find our solution quickly at which point we
    just bail instead of exploring all paths possible.
"""

class Path:
    def __init__(self, path):
        self.path = path
        self.score = self.score()

    def score(self):
        return path_score(self.path)


def path_to_finish(start, end, m):
    paths = []
    paths.append(Path([start]))
    output_paths = []
    while len(paths) > 0:
        path = paths[0]
        frontier = []
        for n in get_neighbors(path.path[-1], m):
            # Never optimal for a given path to retread ground
            if n not in path.path:
                # New point
                if m[n] == 'E':
                    # If win, record it and allow path to be culled
                    return path.path + [n]
                else:
                    frontier.append(n)
        for newpoint in frontier:
            # This should only iterate through new non-winning steps
            paths.append(Path(path.path + [newpoint]))

        # Don't revisit this path
        paths.remove(path)

        # Sort paths by score so we explore promising routes first
        paths = sorted(paths, key=lambda path: path.score)

    return output_paths


def path_score(path):
    direction = east
    score = 0
    for i in range(1, len(path)):
        last_point = path[i-1]
        point = path[i]
        if point[0] != last_point[0] + direction[0] or point[1] != last_point[1] + direction[1]:
            #print(f"Turn at {last_point}")
            score += 1000
            newdir = np.array(np.array(point) - np.array(last_point), dtype=int)
            if np.abs(newdir[0] + newdir[1]) != 1:
                raise ValueError(f"{newdir} is not compass direction...")
            direction = newdir
        score += 1
    return score


with open("../inputs/16.txt", "r") as fid:
    m = {}
    start = (0, 0)
    end = (0, 0)
    xmax = 0
    ymax = 0
    for y, line in enumerate(fid):
        ymax += 1
        for x, c in enumerate(line.strip()):
            m[(x, y)] = c
            if y == 0:
                xmax += 1
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)

    print(xmax, ymax)
    print_map(m, xmax, ymax)

    # Part 1
    path = path_to_finish(start, end, m)
    """
    scores = [path_score(path) for path in paths]
    for i in range(len(paths)):
        print(f"i: {i}")
        print(f"score: {scores[i]}")
        print_path(m, paths[i], xmax, ymax)

    minidx = np.argmin(scores)
    """
    print(f"Part 1: {path_score(path)}")

    # Part 2
    accum = 0
    print(0)
