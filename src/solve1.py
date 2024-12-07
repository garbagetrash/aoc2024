with open("01.txt", "r") as fid:
    n1 = []
    n2 = []
    for line in fid:
        nums = line.strip().split()
        n1.append(int(nums[0]))
        n2.append(int(nums[1]))
    n1.sort()
    n2.sort()

    dist = [abs(_n1 - _n2) for _n1, _n2 in zip(n1, n2)]
    print(sum(dist))

    nn1 = {}
    for num in n1:
        if num in nn1:
            nn1[num] += 1
        else:
            nn1[num] = 1
    nn2 = {}
    for num in n2:
        if num in nn2:
            nn2[num] += 1
        else:
            nn2[num] = 1

    accum = 0
    for num in n1:
        try:
            accum += nn2[num]*num
        except:
            pass
    print(accum)
