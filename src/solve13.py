def bisect(a, b, prize):
    da = a[1] / a[0]
    db = b[1] / b[0]
    less = min(da, db)
    more = max(da, db)
    dp = prize[1] / prize[0]
    max_a = int(prize[0] / a[0])
    
    acnt = max_a
    while True:
        _prize = (prize[0] - acnt*a[0], prize[1] - acnt*a[1])
        try:
            _dp = _prize[1]/_prize[0]
        except:
            # Invalid, halve acnt and try again
            acnt = int(acnt / 2)
            if acnt == 0:
                return 0, prize
            continue

        if _dp <= more and _dp >= less:
            # Valid, accept the jump
            return acnt, _prize
        else:
            # Invalid, halve acnt and try again
            acnt = int(acnt / 2)
            if acnt == 0:
                return 0, prize


def solve1(machine):
    # A button casts 3, B button costs 1
    a, b, prize = machine

    da = a[1] / a[0]
    db = b[1] / b[0]
    less = min(da, db)
    more = max(da, db)
    try:
        dp = prize[1] / prize[0]
        if dp > more or dp < less:
            return None
    except:
        pass

    cost = 0
    acnt, new_prize = bisect(a, b, prize)
    cost += 3*acnt
    prize = new_prize
    while acnt > 0:
        acnt, new_prize = bisect(a, b, prize)
        cost += 3*acnt
        prize = new_prize

    if prize[0] % b[0] == 0 and prize[1] % b[1] == 0 and prize[0] / b[0] == prize[1] / b[1]:
        cost += int(prize[0] / b[0])
        return cost
    else:
        return None

with open("13.txt", "r") as fid:
    a = (0, 0)
    b = (0, 0)
    prize = (0, 0)
    machines = []
    for i, line in enumerate(fid):
        if (i + 1) % 4 == 0:
            pass
        else:
            moves = [x.strip() for x in line.split(':')[1].split(',')]
            if (i + 1) % 4 != 3:
                vals = tuple([int(x.split('+')[1]) for x in moves])
                if (i + 1) % 4 == 1:
                    a = vals
                else:
                    b = vals
            else:
                prize = tuple([int(x.split('=')[1]) for x in moves])
                machines.append((a, b, prize))

    # Part 1
    accum = 0
    for machine in machines:
        cost = solve1(machine)
        #print(machine, cost)
        if cost:
            accum += cost
    print(accum)

    # Part 2
    accum = 0
    for machine in machines:
        a, b, prize = machine
        prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        machine = (machine[0], machine[1], prize)
        cost = solve1(machine)
        #print(machine, cost)
        if cost:
            accum += cost
    print(accum)
