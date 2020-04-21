import sys
program_filename = sys.argv[1]
print(program_filename)
sys.exit()

PRINT_SOMETHING = 1
HALT = 2
SAVE_REG = 3 # store value in a register (called LDI in LS8)
PRINT_REG = 4 # corresponds to PRN in LS8

memory = [PRINT_SOMETHING,
SAVE_REG, # opcode, save R0,37, store 37 in R0 
0, # R0 operand ("arguements")
37, # 37 operand 
PRINT_SOMETHING,
PRINT_REG,
0,
HALT]

# like variables R0-R7, represents physical limitation of hardware
register = [0] * 8 
memory = [0] * 256

address = 0

with open(program_filename) as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()
        if line == '':
            continue
        line = int(line, 2)
        memory[address] = line
        address += 1


# address of the current instruction
program_counter = 0 

running = True

while running:

    instruction = memory[program_counter]

    if instruction == PRINT_SOMETHING:
        print('Printing something')
        program_counter += 1 # 1 byte instruction, move by one
    elif instruction == SAVE_REG:
        reg_num = memory[program_counter + 1]
        value = memory[program_counter + 2]
        register[reg_num] = value
        program_counter += 3 # 3 byte instrution, move by three
    elif instruction == PRINT_REG:
        reg_num = memory[program_counter+1]
        value = register[reg_num]
        print(value)
        program_counter += 2
    elif instruction == HALT:
        running = False
    else:
        print("Unknown instruction")
        running = False