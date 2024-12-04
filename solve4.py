# Load puzzle
xmax = 140
ymax = 140
xword = {}
with open("04.txt", "r") as fid:
    print("part 1")
    for y, line in enumerate(fid):
        for x, c in enumerate(line):
            xword[(x, y)] = c

cntr = 0

# Search horizontal
for y in range(ymax):
    for x in range(xmax - 3):
        word = ""
        for i in range(4):
            word += xword[(x+i, y)]
        if word == "XMAS" or word == "SAMX":
            cntr += 1

# Search vertical
for x in range(xmax):
    for y in range(ymax - 3):
        word = ""
        for i in range(4):
            word += xword[(x, y+i)]
        if word == "XMAS" or word == "SAMX":
            cntr += 1

# Search diagonal down to right
for y in range(ymax - 3):
    for x in range(xmax - 3):
        word = ""
        for i in range(4):
            word += xword[(x+i, y+i)]
        if word == "XMAS" or word == "SAMX":
            cntr += 1

# Search diagonal up to right
for y in range(3, ymax):
    for x in range(xmax - 3):
        word = ""
        for i in range(4):
            word += xword[(x+i, y-i)]
        if word == "XMAS" or word == "SAMX":
            cntr += 1

print(cntr)


print("part 2")
cntr = 0

def check_xmas(x, y):
    # Search diagonal down to right
    dr_fwd = True
    word = ""
    for i in range(3):
        word += xword[(x+i, y+i)]
    if word == "MAS":
        dr_fwd = True
    elif word == "SAM":
        dr_fwd = False
    else:
        return False

    # Search diagonal up to right
    ur_fwd = True
    word = ""
    for i in range(3):
        word += xword[(x+i, y-i+2)]
    if word == "MAS":
        ur_fwd = True
    elif word == "SAM":
        ur_fwd = False
    else:
        return False

    return True

# Check upper left corner
for x in range(xmax - 2):
    for y in range(ymax - 2):
        if check_xmas(x, y):
            cntr += 1

print(cntr)
