def neighbors(p, m):
    c = [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]
    output = []
    for cc in c:
        try:
            if m[cc] == '.':
                output.append(cc)
        except:
            pass
    return output


def build_dist_map(p1, p2, m):
    frontier = [(p1, 0)]
    explored = []
    while len(frontier) > 0:
        for n in neighbors(frontier[0][0], m):
            epoints = [e[0] for e in explored]
            fpoints = [f[0] for f in frontier]
            if n not in epoints and n not in fpoints:
                frontier.append((n, frontier[0][1] + 1))
                break
        explored.append(frontier[0])
        del frontier[0]

    # No path
    return explored


def cheat_neighbors_1layer(p, m):
    c = [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] - 1, p[1])]
    output = []
    for cc in c:
        try:
            if m[cc] == '#':
                output.append(cc)
        except:
            pass
    return output


def cheat_neighbors(point, distmap, m):
    p, pdist = point

    cheat_moves = set()
    one_layer = cheat_neighbors_1layer(p, m)
    
    # Finalize with 1 normal move
    candidates = set()
    for pp in one_layer:
        normal = neighbors(pp, m)
        candidates.update([(o, 2) for o in normal])
    
    output = []
    for (c, cost) in candidates:
        for d in distmap:
            newdist = d[1]
            if c == d[0]:
                output.append((c, newdist, cost))

    return output


def _cheat_neighbors(point, distmap, m):
    p, pdist = point

    cheat_moves = set()
    one_layer = cheat_neighbors_1layer(p, m)
    cheat_moves.update([(o, 1) for o in one_layer]) # set of (pos, cost)
    for pp in one_layer:
        two_layers = cheat_neighbors_1layer(pp, m)
        cheat_moves.update([(o, 2) for o in two_layers])
    
    # Finalize with 1 normal move
    candidates = set()
    for (pp, cost) in cheat_moves:
        normal = neighbors(pp, m)
        candidates.update([(o, cost + 1) for o in normal])
    
    output = []
    for (c, cost) in candidates:
        for d in distmap:
            newdist = d[1]
            if c == d[0]:
                output.append((c, newdist, cost))

    return output


with open("../inputs/20.txt", "r") as fid:
    xmax = 0
    ymax = 0
    start = (0, 0)
    end = (0, 0)
    m = {}
    for y, line in enumerate(fid):
        ymax += 1
        for x, c in enumerate(line.strip()):
            if y == 0:
                xmax += 1
            if c == 'S':
                start = (x, y)
                m[(x, y)] = '.'
            elif c == 'E':
                end = (x, y)
                m[(x, y)] = '.'
            else:
                m[(x, y)] = c
        
    print((xmax, ymax))

    distmap = build_dist_map(end, start, m)
    total_length = distmap[-1][1]
    print(distmap)

    # Part 1
    accum = 0
    for d in distmap:
        spent = total_length - d[1]
        #print(f"Start: {d}, Spent: {spent}")
        for (cn, newdist, cost) in cheat_neighbors(d, distmap, m):
            new_total = spent + newdist + cost
            #if total_length > new_total:
                #print(f"End: {cn}, New Total: {new_total}")
                #print(f"saved: {total_length - new_total}")
            if total_length - new_total >= 100:
                accum += 1
        #print()
    print(accum)

    # Part 2
    accum = 0
    print(accum)
