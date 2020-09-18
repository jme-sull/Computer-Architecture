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
    CMP = 0b10100111
    CALL = 0b01010000
    RET = 0b00010001
    ADD = 0b10100000
    JMP = 0b01010100
    JEQ = 0b01010101
    JNE = 0b01010110


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #the ls has 8 bit addressing(index)
        self.reg = [0] * 8
        self.pc = 0 #the program counter, aka address of the currently excuting instruction 
        self.running = True
        self.sp = 7
        self.fl = [0] * 8 #E = self.fl[-1], G self.fl[-2], L self.fl[-3]
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

            elif ir == self.ADD:
                self.reg[operand_a] += self.reg[operand_b]
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

            elif ir == self.RET:
                address_to_pop_from = self.reg[self.sp]
                return_address = self.ram[address_to_pop_from]
                self.reg[self.sp] += 1

                self.pc = return_address

            elif ir == self.CALL:
                return_address = self.pc + 2
                self.reg[self.sp] -= 1
                address_to_push_to = self.reg[self.sp]
                self.ram[address_to_push_to] = return_address

                subroutine_address = self.reg[operand_a]

                self.pc = subroutine_address

            elif ir == self.CMP:
                 #compare operand A and operand b
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl[-1] = 1
                    self.pc += 3
    
                #if they are equal, set the Equal E flag to 1, otherwise set it to 0
                else:
                    self.fl[-1] = 0
                    self.pc += 3
                    
            
            elif ir == self.JMP:
                #Jump to the address stored in the given register.
            
                #Set the PC to the address stored in the given register.
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                self.pc = value
                

            elif ir == self.JEQ:
                # If equal flag is set (true), 
                # jump to the address stored in the given register.
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                if self.fl[-1] == 1:
                    self.pc = value
                
                else:
                    self.pc += 2
            
            elif ir == self.JNE:
                # If E flag is clear (false, 0), jump to the 
                # address stored in the given register.
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                if self.fl[-1] == 0:
                    self.pc = value
                else:
                    self.pc += 2
                    

            else:
                print(f'Unknown instruction at {self.pc}')
                self.running = False

            #print("REG", self.reg)
            #print("RAM", self.ram)

            # offset = ir >> 6
            # self.pc += offset + 1

