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
        output += i*m
    return output


def swap2(memory, empty, file):
    for i in range(file[2]):
        memory[empty[0] + i] = memory[file[0] + i]
        memory[file[0] + i] = -1
    return memory


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

    # flip it, first element is last empty space, last is first.
    empty = empty[::-1]
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

    # flip files around
    files = files[::-1]
    return files


def defrag2(memory):
    empty = calc_empty(memory)
    files = calc_file(memory)

    print("files: ", files)

    # starting with last file, walk backwards
    for j, f in enumerate(files):
        # recalculate and walk forwards in empty spaces...
        empty = calc_empty(memory)
        print("empty: ", empty)
        for e in empty[::-1]:
            if e[2] >= f[2]:
                # e is large enough to accomodate f
                # do swap
                print(j, "large enough")
                memory = swap2(memory, e, f)
                break

    return truncate(memory)

with open("../inputs/09a.txt", "r") as fid:
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
    print_memory(memory_og)

    # Part 1
    mem1 = copy.deepcopy(memory_og)
    memory = defrag(mem1)
    print_memory(memory)
    print(calc_checksum(memory))


    # Part 2
    mem2 = copy.deepcopy(memory_og)
    print_memory(mem2)
    memory = defrag2(mem2)
    print_memory(memory)
    print(calc_checksum(memory))
