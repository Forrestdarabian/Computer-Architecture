"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 8
        self.register = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""

        # address = 0

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
        IR = self.pc
        running = True

        while running:
            opcode = self.ram_read(IR)
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)
            if opcode == LDI:
                self.reg[operand_a] = operand_b
                IR += 3
            elif opcode == PRN:
                print(self.reg[operand_a])
                IR += 2
            elif opcode == MUL:
                self.alu(opcode, operand_a, operand_b)
                IR += 3
            elif opcode == HLT:
                sys.exit(0)
            else:
                print("OPCODE not recognized.")
                sys.exit(1)



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

    def ram_read(self, address):
        return self.ram[int(str(address), 2)]

    def ram_write(self, address, value):
        self.ram[int(str(address), 2)] = value
