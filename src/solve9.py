import math
import numpy as np


def print_memory(memory):
    for c in memory:
        if c == -1:
            print('.', end="")
        else:
            print(int(c), end="")
    print()


def truncate(memory):
    tcnt = 0
    for m in memory[::-1]:
        if m < 0:
            tcnt += 1
        else:
            break
    return memory[:-tcnt]


def defrag(memory):
    # Keep track of empty spaces. ordered, increasing.
    empty_idxs = []
    for i, m in enumerate(memory):
        if m < 0:
            empty_idxs.append(i)

    # flip is, first element is last empty space, last is first.
    empty_idxs = empty_idxs[::-1]

    for j, m in enumerate(memory[::-1]):
        midx = len(memory) - 1 - j
        if empty_idxs[-1] < midx:
            # if this empty index is pointed into our valid memory
            if m >= 0:
                # do swap
                memory[empty_idxs[-1]] = m
                memory[len(memory)-1-j] = -1
                empty_idxs = empty_idxs[:-1]

    return truncate(memory)


def calc_checksum(memory):
    output = 0
    for i, m in enumerate(memory):
        output += i*m
    return output


with open("../inputs/09.txt", "r") as fid:
    inputs = fid.read()
    memory = -np.ones(len(inputs) * 10, dtype=int)

    isfile = True
    fcntr = 0
    blkcntr = 0
    for c in inputs:
        if c == '\n':
            break
        if isfile:
            for i in range(int(c)):
                memory[blkcntr] = fcntr
                blkcntr += 1
            fcntr += 1
        else:
            for _ in range(int(c)):
                blkcntr += 1
        isfile ^= 1

    memory = truncate(memory)
    print_memory(memory)
    memory = defrag(memory)
    print_memory(memory)

    # Part 1
    print(calc_checksum(memory))

    # Part 2
    output = set()
    print(len(output))
