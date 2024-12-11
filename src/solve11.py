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
    nsteps = 15
    mm = copy.deepcopy(l)
    for i in range(int(75/nsteps)):
        new = []
        print(nsteps*i)
        for c in mm:
            new += memoize_n_steps(c, nsteps)
        mm = new
    return mm


with open("../inputs/11a.txt", "r") as fid:
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
    cnt = 0
    mm = solvepart2(m)
    print(len(mm))
