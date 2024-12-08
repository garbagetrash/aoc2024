import math

def calc_antinodes(p1, p2, xmax, ymax):
    x1 = locarr[i1][0]
    y1 = locarr[i1][1]
    x2 = locarr[i2][0]
    y2 = locarr[i2][1]
    dx = x2 - x1
    dy = y2 - y1
    # Reduce dxdy by dividing by gcd
    g = math.gcd(dx, dy)
    dx /= g
    dy /= g
    # start at p1, go in negative dx direction first, then positive
    outputs = set()
    t = 0
    while True:
        xx = x1 - t*dx
        if xx < 0 or xx >= xmax:
            break
        yy = y1 - t*dy
        if yy < 0 or yy >= ymax:
            break
        outputs.add((xx, yy))
        t += 1
    t = 0
    while True:
        xx = x1 + t*dx
        if xx < 0 or xx >= xmax:
            break
        yy = y1 + t*dy
        if yy < 0 or yy >= ymax:
            break
        outputs.add((xx, yy))
        t += 1
    return outputs


with open("../inputs/08.txt", "r") as fid:
    m = {}
    xmax = 0
    ymax = 0
    freqs = {}
    for y, line in enumerate(fid):
        ymax += 1
        xmax = len(line) - 1
        for x, c in enumerate(line):
            m[(x, y)] = c
            if c != '.' and c != '\n':
                try:
                    freqs[c].append((x, y))
                except:
                    freqs[c] = [(x, y)]

    print(freqs)
    print(xmax, ymax)

    # Part 1
    output = set()
    for locarr in freqs.values():
        for i1 in range(len(locarr)):
            for i2 in range(i1 + 1, len(locarr)):
                x1 = locarr[i1][0]
                y1 = locarr[i1][1]
                x2 = locarr[i2][0]
                y2 = locarr[i2][1]
                dx = x2 - x1
                dy = y2 - y1
                out1 = (y2 + dy, x2 + dx)
                out2 = (y1 - dy, x1 - dx)
                if 0 <= out1[0] and out1[0] < xmax and 0 <= out1[1] and out1[1] < ymax:
                    output.add(out1)
                if 0 <= out2[0] and out2[0] < xmax and 0 <= out2[1] and out2[1] < ymax:
                    output.add(out2)

    print(len(output))

    # Part 2
    output = set()
    for locarr in freqs.values():
        for i1 in range(len(locarr)):
            for i2 in range(i1 + 1, len(locarr)):
                newouts = calc_antinodes(locarr[i1], locarr[i2], xmax, ymax)
                output.update(newouts)
    print(len(output))
