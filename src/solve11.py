import copy

cache = {}

def apply(l):
    new = []
    for n in l:
        if n == 0:
            new.append(1)
        elif len(str(n)) % 2 == 0:
            sn = str(n)
            x2 = int(len(sn) // 2)
            new.append(int(sn[:x2]))
            new.append(int(sn[x2:]))
        else:
            new.append(2024*n)
    return new


def memoize_last_n_steps(n, m):
    try:
        return len(cache[(n, m)])
    except:
        l = [n]
        for _ in range(m):
            l = apply(l)
        cache[(n, m)] = l
        return len(l)


def memoize_n_steps(n, m):
    try:
        return cache[(n, m)]
    except:
        l = [n]
        for _ in range(m):
            l = apply(l)
        cache[(n, m)] = l
        return l


def solvepart2(l):
    nsteps = 5
    mm = copy.deepcopy(l)
    for i in range(8):
        new = []
        print(nsteps*i)
        for c in mm:
            new += memoize_n_steps(c, nsteps)
        mm = new

    # mm has taken 40 steps, now get counts for 35 steps and sum
    accum = 0
    for i, c in enumerate(mm):
        print(f"{i}/{len(mm)}", end="\r", flush=True)
        accum += memoize_last_n_steps(c, 35)
    return accum


with open("../inputs/11.txt", "r") as fid:
    m = []
    for n in fid.read().split():
        m.append(int(n))

    print(m)

    # Part 1
    mm = copy.deepcopy(m)
    for i in range(25):
        print(i)
        mm = apply(mm)
    print(len(mm))

    print(memoize_n_steps(m[0], 5))
    print(memoize_n_steps(m[1], 5))

    # Part 2
    print(solvepart2(m))
