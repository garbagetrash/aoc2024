import copy
import numpy as np
from enum import Enum




class Program:
    def __init__(self, instructions, a, b, c):
        self.instructions = instructions
        self.a = a
        self.b = b
        self.c = c
        self.instruction_pointer = 0
        self.output = []

    def execute(self):
        while self.instruction_pointer < len(self.instructions):
            opcode = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            print(f"Opcode: {opcode}, Operand: {operand}")
            self._execute(opcode, operand)

    def _execute(self, opcode, operand):
        if opcode == 0:
            print("Division - > A")
            self.a = int(self.a / (2 ** self.combo(operand)))
            self.instruction_pointer += 2
        elif opcode == 1:
            print("Bitwise XOR: B and literal")
            self.b ^= operand
            self.instruction_pointer += 2
        elif opcode == 2:
            print("Modulo 8")
            self.b = self.combo(operand) % 8
            self.instruction_pointer += 2
        elif opcode == 3:
            print("Jump non-zero")
            if self.a != 0:
                self.instruction_pointer = operand
            else:
                # is this right?
                self.instruction_pointer += 2
        elif opcode == 4:
            print("Bitwise XOR: B and C")
            self.b ^= self.c
            self.instruction_pointer += 2
        elif opcode == 5:
            print("Modulo 8 and output")
            tmp = self.combo(operand) % 8
            self.output.append(tmp)
            self.instruction_pointer += 2
        elif opcode == 6:
            print("Division -> B")
            self.b = int(self.a / (2 ** self.combo(operand)))
            self.instruction_pointer += 2
        elif opcode == 7:
            print("Division -> C")
            self.c = int(self.a / (2 ** self.combo(operand)))
            self.instruction_pointer += 2

    def combo(self, literal):
        if literal < 4:
            return literal
        elif literal == 4:
            return self.a
        elif literal == 5:
            return self.b
        elif literal == 6:
            return self.c
        elif literal == 7:
            raise ValueError("Invalid combo literal 7")

with open("../inputs/17.txt", "r") as fid:
    a = int(fid.readline().split()[-1])
    b = int(fid.readline().split()[-1])
    c = int(fid.readline().split()[-1])
    fid.readline()
    program = [int(x) for x in fid.readline().split(':')[1].strip().split(',')]

    print(a, b, c, program)

    # Part 1
    p = Program(program, a, b, c)
    p.execute()
    print(f"Part 1: {p.output}")

    # Part 2
    print(f"Part 2: {0}")
