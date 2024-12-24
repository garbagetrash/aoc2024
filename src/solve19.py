# Global pattern cache, contains achievable patterns
cache = {}
towels = []

def pattern_solver(pattern):
    #print(f"Pattern: {pattern}")
    try:
        return cache[pattern]
    except:
        # Add new pattern to cache if not already there
        cache[pattern] = 0

    nways = 0
    for t in towels:
        if t == pattern[:len(t)]:
            # Matches head
            #print(f"{t} matches head of {pattern}")
            if len(t) == len(pattern):
                nways += 1
            else:
                nways += pattern_solver(pattern[len(t):])

    # Update cache solution
    #print(f"{pattern} can be made {nways} ways")
    cache[pattern] = nways
    return nways

with open("../inputs/19.txt", "r") as fid:
    coords = []
    maxval = 0
    patterns = []
    for i, line in enumerate(fid):
        if i == 0:
            pattern_list = line.strip().split(', ')
            for p in pattern_list:
                towels.append(p)
        elif i > 1:
            patterns.append(line.strip())

    # Part 1
    accum = 0
    for p in patterns:
        if pattern_solver(p) > 0:
            accum += 1
    print(accum)

    # Part 2
    accum = 0
    for p in patterns:
        nsolves = pattern_solver(p)
        accum += nsolves
    print(accum)
