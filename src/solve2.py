import copy

def check(nums):
    increasing = True
    if nums[1] > nums[0]:
        increasing = True
    else:
        increasing = False
    for i in range(1, len(nums)):
        if increasing:
            if nums[i] < nums[i - 1] + 1:
                return False
            elif nums[i] > 3 + nums[i - 1]:
                return False
        else:
            if nums[i] > nums[i - 1] - 1:
                return False
            elif nums[i] < nums[i - 1] - 3:
                return False
    return True

def check_all(nums):
    if check(nums):
        return True
    else:
        for i in range(len(nums)):
            temp = copy.deepcopy(nums)
            del temp[i]
            if check(temp):
                return True
        return False

with open("02.txt", "r") as fid:
    nsafe1 = 0
    nsafe2 = 0
    for line in fid:
        nums = line.strip().split()
        nums = [int(n) for n in nums]
        if check(nums):
            nsafe1 += 1
        if check_all(nums):
            nsafe2 += 1

    print(nsafe1)
    print(nsafe2)
