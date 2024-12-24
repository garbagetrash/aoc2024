# Global pattern cache, contains achievable patterns
cache = {}

def pattern_solver(pattern, layer=0):
    try:
        return cache[pattern]
    except:
        pass
    for split_point in range(1, len(pattern)):
        #print(f"splitting at index: {split_point}")
        if pattern_solver(pattern[:split_point], layer=layer+1):
            # only bother with right if left was solvable.
            if pattern_solver(pattern[split_point:], layer=layer+1):
                # left and right solvable so pattern can be constructed
                cache[pattern] = True
                return True
    cache[pattern] = False
    return False

with open("../inputs/19.txt", "r") as fid:
    coords = []
    maxval = 0
    pattern_list = []
    patterns = []
    for i, line in enumerate(fid):
        if i == 0:
            pattern_list = line.strip().split(', ')
            for p in pattern_list:
                cache[p] = True
        elif i > 1:
            patterns.append(line.strip())
    
    print(patterns)

    # Part 1
    accum = 0
    for p in patterns:
        if pattern_solver(p):
            print(f"Desired: {p} has solution")
            accum += 1
    print(accum)

    # Part 2
    print(0)
