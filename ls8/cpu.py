"""CPU functionality."""

import sys

# opcodes/names for instruction - need operands/variables to execute

HLT  = 0b00000001
LDI  = 0b10000010 # (R2, 37) two operands / pc += 3 find value 3 by shifting
PRN = 0b01000111
MUL  = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.instructions = {}
        self.reg = [0] * 8 # fixed performance storage
        self.ram = [0] * 256 # random access memory
        self.pc = 0 # program counter, address of currently executing instruction



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # with open(program_filename) as f:
        #     for line in f:
        #         line = line.split('#')
        #         line = line[0].strip()
        #         if line == '':
        #             continue
        #         line = int(line, 2)
        #         self.ram[address] = line
        #         address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # takes Memory Address Register AKA the address we are reading/writing and returns value therein
    def ram_read(self, MAR):
        # return MDR, Memory Data Register, value just read
        MDR = self.ram[MAR]
        return MDR

    # takes MAR memory address register and MDR memory data register (value to write)
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
    
    def prn(self, operand):
        print(self.reg[operand])

    def hlt(self):
        exit()

    def run(self):
        """Run the CPU."""
        running = True
        while running == True:
            ir = self.ram[self.pc] # instruction register/reserved register 
            inst_len = ((ir & 0b11000000) >> 6) + 1 
            self.pc += inst_len
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            if ir == HLT:
                self.hlt()
            elif ir == LDI: # Set the value of a register to an integer.
                self.ldi(0, 8)
            elif ir == PRN:
                self.prn(0)
            
            
            
            



            


