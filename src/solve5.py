# Load puzzle
rules_left = {}
rules_right = {}
updates = []

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

with open("../inputs/05.txt", "r") as fid:
    nextpart = False
    print("part 1")
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

    accum = 0
    for update in updates:
        if check_order(update, rules_left, rules_right):
            print(update)
            middle = len(update) // 2
            accum += update[middle]
    print(accum)
