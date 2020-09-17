"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    LDI = 0b10000010
    PRN = 0b01000111
    HLT = 0b00000001
    MLT = 0b10100010
    PUSH = 0b01000101
    POP = 0b01000110
    NOP = 0b00000000


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #the ls has 8 bit addressing(index)
        self.reg = [0] * 8
        self.pc = 0 #the program counter, aka address of the currently excuting instruction 
        self.running = True
        self.sp = 7
        self.reg[self.sp] = 0xF4 

    def ram_read(self, MAR): #MAR contains the address that is being read or written to
        return self.ram[MAR]

    def ram_write(self, MDR, MAR): #contains the data that was read or the data to write
        self.ram[MDR] = MAR
    
    
    def load(self, filename):
        """Load a program into memory."""
        address = 0 
        with open(filename) as fp:
            for line in fp:
                comment_split = line.split('#')
                num = comment_split[0].strip()
                if num == '':
                    continue
                val = int(num, 2)
                self.ram[address] = val
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""

        while self.running:
           
            ir = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2] #instruction register, copy of currently excuting instruction

            if ir == self.LDI: 
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == self.PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == self.MLT:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            
            elif ir == self.HLT:
                self.running = False

            elif ir == self.PUSH:

                #Decrement SP
                self.reg[self.sp] -=1
                # self.reg[self.sp] &= 0xFF

                #get the reg num to push
                reg_num = operand_a

                #get the value to push
                value = self.reg[operand_a]
                


                #copy the value to the SP address
                top_of_stack_address = self.reg[self.sp]
                self.ram_write(top_of_stack_address, value)
               
        

                self.pc += 2 

            
            elif ir == self.POP:

                #get reg to pop into
                reg_num = operand_a

                #get the top of stack addr
                top_of_stack_address = self.reg[self.sp]

                #get the value at the top of the stack
                value = self.ram[top_of_stack_address]

                #store the value in the register 
                self.reg[reg_num] = value
            
                


                #increment the SP
                self.reg[self.sp] += 1 
                self.pc += 2

            elif ir == self.NOP:
                continue

            else:
                print(f'Unknown instruction')

            #print("REG", self.reg)
            #print("RAM", self.ram)

            # offset = ir >> 6
            # self.pc += offset + 1

