import copy

# Load puzzle
rules_left = {}
rules_right = {}
updates = []

# rules_left contains list of things that the key is to the left of. IE the list
# for a given key has the things to the right of that key. rules_right is the
# opposite.

# For example using alphabetical ordering on the set {a, b, c, d}:
# rules_left[a] = [b, c, d]
# rules_left[c] = [d]
# rules_right[c] = [a, b]

def check_order(update, rules_left, rules_right):
    for i, current in enumerate(update):
        try:
            for right in rules_left[current]:
                try:
                    if i > update.index(right):
                        return False
                except:
                    pass
        except KeyError:
            pass

        try:
            for left in rules_right[current]:
                try:
                    if i < update.index(left):
                        return False
                except:
                    pass
        except KeyError:
            pass

    return True

def swap(x, i1, i2):
    x[i1], x[i2] = x[i2], x[i1]
    return x

def find_swap_idxs(x, rules_left, rules_right):
    for i, xx in enumerate(x):
        try:
            for right in rules_left[xx]:
                if right in x:
                    ridx = x.index(right)
                    if i > ridx:
                        # swap
                        return i, ridx
            for left in rules_right[xx]:
                if left in x:
                    lidx = x.index(left)
                    if i < lidx:
                        # swap
                        return i, lidx
        except:
            pass
    return None

def dosort(line, rules_left, rules_right):
    x = copy.deepcopy(line)
    while True:
        idxs = find_swap_idxs(x, rules_left, rules_right)
        if idxs:
            x = swap(x, idxs[0], idxs[1])
        else:
            return x

with open("../inputs/05.txt", "r") as fid:
    nextpart = False
    for y, line in enumerate(fid):
        if line == "\n":
            nextpart = True
        else:
            if not nextpart:
                # Read first part
                s = line.split('|')
                if int(s[0]) in rules_left.keys():
                    rules_left[int(s[0])].append(int(s[1]))
                else:
                    rules_left[int(s[0])] = [int(s[1])]
                if int(s[1]) in rules_right.keys():
                    rules_right[int(s[1])].append(int(s[0]))
                else:
                    rules_right[int(s[1])] = [int(s[0])]
            else:
                # Now read second part
                updates.append([int(x) for x in line.split(',')])

    # Part 1
    accum = 0
    for update in updates:
        if check_order(update, rules_left, rules_right):
            middle = len(update) // 2
            accum += update[middle]
    print(accum)

    # Part 2
    accum = 0
    for update in updates:
        if not check_order(update, rules_left, rules_right):
            new_line = dosort(update, rules_left, rules_right)
            middle = len(new_line) // 2
            accum += new_line[middle]
    print(accum)
