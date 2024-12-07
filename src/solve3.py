import re

with open("03.txt", "r") as fid:
    r = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    accum = 0
    for line in fid:
        m = r.findall(line)
        for match in m:
            print(match)
            accum += int(match[0]) * int(match[1])

    print(accum)


with open("03.txt", "r") as fid:
    print("part 2")
    enabled = True
    r2 = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|(do\(\))|(don't\(\))")
    accum = 0
    for line in fid:
        m = r2.finditer(line)
        for match in m:
            print(match.groups())
            if match.groups()[2]:
                enabled = True
            elif match.groups()[3]:
                enabled = False
            print(enabled)
            if match.groups()[0] and enabled:
                accum += int(match.groups()[0]) * int(match.groups()[1])
    print(accum)
