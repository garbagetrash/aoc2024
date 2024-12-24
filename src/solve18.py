def neighbors(p, m):
    c = [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]
    output = []
    for cc in c:
        try:
            if m[cc] == 0:
                output.append(cc)
        except:
            pass
    return output


def shortest_path(p1, p2, m):
    frontier = [(p1, 0)]
    explored = set()
    while True:
        for n in neighbors(frontier[0][0], m):
            print(n)
            fpoints = [f[0] for f in frontier]
            if n not in explored and n not in fpoints:
                if n == p2:
                    return frontier[0][1] + 1
                frontier.append((n, frontier[0][1] + 1))
        explored.add(frontier[0][0])
        del frontier[0]


with open("18.txt", "r") as fid:
    coords = []
    maxval = 0
    for i, line in enumerate(fid):
        x, y = line.strip("()\n").split(',')
        x = int(x)
        y = int(y)
        if x > maxval:
            maxval = x
        if y > maxval:
            maxval = y
        coords.append((int(x), int(y)))

    print(coords)
    m = {}
    for x in range(maxval + 1):
        for y in range(maxval + 1):
            if (x, y) in coords[:1024]:
                m[(x, y)] = 1
            else:
                m[(x, y)] = 0

    # Part 1
    print(shortest_path((0, 0), (maxval, maxval), m))

    # Part 2
    accum = 0
    print(accum)
