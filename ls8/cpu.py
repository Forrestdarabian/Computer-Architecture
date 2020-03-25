"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.running = True
        self.branch_table = {
            HLT: self.HLT_op,
            LDI: self.LDI_op,
            PRN: self.PRN_op,
            MUL: self.MUL_op,
            PUSH: self.PUSH_op,
            POP: self.POP_op
        }

    def HLT_op(self, oper_a, oper_b):
        self.running = False

    def LDI_op(self, oper_a, oper_b):
        self.reg[oper_a] = oper_b
        self.pc += 3

    def PRN_op(self, oper_a, oper_b):
        print(self.reg[oper_a])
        self.pc += 2

    def MUL_op(self, oper_a, oper_b):
        self.alu('MUL', oper_a, oper_b)
        self.pc += 3

    def PUSH_op(self, oper_a, oper_b):
        self.push(self.reg[oper_a])
        self.pc += 2

    def POP_op(self, oper_a, oper_b):
        self.reg[oper_a] = self.pop()
        self.pc += 2

    def push(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[7])

    def pop(self):
        value = self.ram_read(self.reg[7])
        self.reg[SP] += 1
        return value

    def ram_read(self, address):
        return self.ram[int(str(address), 2)]

    def ram_write(self, address, value):
        self.ram[int(str(address), 2)] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            address = 0
            # open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # multiply
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            return self.reg[reg_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            oper_a = self.ram_read(self.pc + 1)
            oper_b = self.ram_read(self.pc + 2)
            if int(bin(IR), 2) in self.branch_table:
                self.branch_table[IR](oper_a, oper_b)
            else:
                raise Exception(
                    f'Invalid {IR}, not in branch table \t {list(self.branch_table.keys())}')

            # # LDI
            # if self.ram[self.pc] == 0b10000010:
            #     self.register[int(str(self.ram[self.pc + 1]), 2)
            #                   ] = self.ram[self.pc + 2]
            #     self.pc += 3

            # # PRN
            # elif self.ram[self.pc] == 0b01000111:
            #     print(self.register[int(str(self.ram[self.pc + 1]), 2)])
            #     self.pc += 2

            # # HLT
            # elif self.ram[self.pc] == 0b00000001:
            #     self.pc = 0
            #     running = False
