import copy
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

    # flip it, first element is last empty space, last is first.
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
        if m >= 0:
            output += i*m
    return output


def swap2(memory, empty, file):
    for i in range(file[2]):
        memory[empty[0] + i] = memory[file[0] + i]
        memory[file[0] + i] = -1

    newstart = empty[0] + file[2]
    return (newstart, empty[1], empty[1] - newstart)


def calc_empty(memory):
    # Keep track of empty spaces. ordered, increasing.
    empty = []
    start = None
    for i, m in enumerate(memory):
        if start is not None and m >= 0:
            end = i
            empty.append((start, end, end - start))
            start = None
        if start is None and m < 0:
            start = i

    return empty


def calc_file(memory):
    files = []
    start = None
    current = None
    for i, m in enumerate(memory):
        if start is not None and m != current:
            end = i
            files.append((start, end, end - start))
            start = None
        if start is None and m >= 0:
            start = i
            current = m
    if start is not None:
        # finish last file
        end = len(memory)
        files.append((start, end, end - start))

    return files


def defrag2(memory):
    empty = calc_empty(memory)
    files = calc_file(memory)

    # starting with last file, walk backwards
    for f in files[::-1]:
        # recalculate and walk forwards in empty spaces...
        for i in range(len(empty)):
            if empty[i][0] > f[0]:
                # Bail after we're looking at empty spaces past our files
                break
            if empty[i][2] >= f[2]:
                # empty[i] is large enough to accomodate f
                # do swap
                empty[i] = swap2(memory, empty[i], f)
                break

    return truncate(memory)

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

    memory_og = truncate(memory)

    # Part 1
    mem1 = copy.deepcopy(memory_og)
    memory = defrag(mem1)
    print(calc_checksum(memory))


    # Part 2
    mem2 = copy.deepcopy(memory_og)
    memory = defrag2(mem2)
    print(calc_checksum(memory))
