"""CPU functionality."""

import sys

# opcodes/names for instruction - need operands/variables to execute

HLT  = 0b00000001
LDI  = 0b10000010 # (R2, 37) two operands / pc += 3 find value 3 by shifting
PRN = 0b01000111
MUL  = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.instructions = {}
        self.reg = [0] * 8 # fixed performance storage
        self.ram = [0] * 256 # random access memory
        self.pc = 0 # program counter, address of currently executing instruction
        # self.sp = self.reg[7] 
        self.branch_table = {
                            # HLT: self.hlt,
                            LDI: self.ldi,
                            PRN: self.prn,
                            MUL: self.mul,
                            PUSH: self.push,
                            POP: self.pop
                            }
        self.reg[7] = 3 # initialize stack pointer



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        program_filename = sys.argv[1]
        print(program_filename)
        # sys.exit()

        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                line = int(line, 2)
                self.ram[address] = line
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
    
    def prn(self, operand_a,operand_b):
        print(self.reg[operand_a])

    def hlt(self):
        exit()
    
    def mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
    
    def push(self, operand_a, operand_b):
        # decrement stack pointer
        self.reg[7] -= 1 # address at the top of the stack minus 1
        # copy value from reg into mem at SP
        reg_number = operand_a
        value = self.reg[reg_number] # what we are pushing
        self.ram[self.reg[7]] = value # store the value on the stack

    def pop(self, operand_a, operand_b):
        # copy value from mem where stack pointer is into register
        self.reg[operand_a] = self.ram[self.reg[7]]
        # increment SP
        self.reg[7] += 1

    def run(self):
        """Run the CPU."""
        running = True
        while running == True:
            ir = self.ram[self.pc] # instruction register/reserved register 
            inst_len = ((ir & 0b11000000) >> 6) + 1 
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            if ir in self.branch_table:
                self.branch_table[ir](operand_a, operand_b)
            else:
                self.hlt()
            

            # if ir == HLT:
            #     self.hlt()
            # elif ir == LDI: # Set the value of a register to an integer.
            #     self.ldi(operand_a, operand_b)
            # elif ir == PRN:
            #     self.prn(operand_a)
            # elif ir == MUL:
            #     self.alu('MUL', operand_a, operand_b)
            self.pc += inst_len
            
            
            
            



            


