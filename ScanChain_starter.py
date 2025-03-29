import copy
import cocotb
from cocotb.triggers import Timer


# Make sure to set FILE_NAME
# to the filepath of the .log
# file you are working with
CHAIN_LENGTH = 3
FILE_NAME    = "fault/fault5.sv"



# Holds information about a register
# in your design.

################
# DO NOT EDIT!!!
################
class Register:

    def __init__(self, name) -> None:
        self.name = name            # Name of register, as in .log file
        self.size = -1              # Number of bits in register

        self.bit_list = list()      # Set this to the register's contents, if you want to
        self.index_list = list()    # List of bit mappings into chain. See handout

        self.first = -1             # LSB mapping into scan chain
        self.last  = -1             # MSB mapping into scan chain


# Holds information about the scan chain
# in your design.
        
################
# DO NOT EDIT!!!
################
class ScanChain:

    def __init__(self) -> None:
        self.registers = dict()     # Dictionary of Register objects, indexed by 
                                    # register name
        
        self.chain_length = 0       # Number of FFs in chain


# Sets up a new ScanChain object
# and returns it

################     
# DO NOT EDIT!!!
################
def setup_chain(filename):

    scan_chain = ScanChain()

    f = open(filename, "r")
    for line in f:
        linelist = line.split()
        index, name, bit = linelist[0], linelist[1], linelist[2]

        if name not in scan_chain.registers:
            reg = Register(name)
            reg.index_list.append((int(bit), int(index)))
            scan_chain.registers[name] = reg

        else:
            scan_chain.registers[name].index_list.append((int(bit), int(index)))
        
    f.close()

    for name in scan_chain.registers:
        cur_reg = scan_chain.registers[name]
        cur_reg.index_list.sort()
        new_list = list()
        for tuple in cur_reg.index_list:
            new_list.append(tuple[1])
        
        cur_reg.index_list = new_list
        cur_reg.bit_list   = [0] * len(new_list)
        cur_reg.size = len(new_list)
        cur_reg.first = new_list[0]
        cur_reg.last  = new_list[-1]
        scan_chain.chain_length += len(cur_reg.index_list)

    return scan_chain


# Prints info of given Register object

################
# DO NOT EDIT!!!
################
def print_register(reg):
    print("------------------")
    print(f"NAME:    {reg.name}")
    print(f"BITS:    {reg.bit_list}")
    print(f"INDICES: {reg.index_list}")
    print("------------------")


# Prints info of given ScanChain object

################   
# DO NOT EDIT!!!
################
def print_chain(chain):
    print("---CHAIN DISPLAY---\n")
    print(f"CHAIN SIZE: {chain.chain_length}\n")
    print("REGISTERS: \n")
    for name in chain.registers:
        cur_reg = chain.registers[name]
        print_register(cur_reg)



#-------------------------------------------------------------------

# This function steps the clock once.
    
# Hint: Use the Timer() builtin function
async def step_clock(dut):
        dut.clk.value = 1
        await Timer(10, units = 'ns')
        dut.clk.value = 0
        await Timer(10, units = 'ns')

    

#-------------------------------------------------------------------

# This function places a bit value inside FF of specified index.
        
# Hint: How many clocks would it take for value to reach
#       the specified FF?
        
async def input_chain_single(dut, bit, ff_index):
        dut.scan_en.value = 1
        dut.scan_in.value = bit
        for i in range(ff_index + 1):
            if i != 0:
                dut.scan_in.value = 0
            await step_clock(dut)
        dut.scan_en.value = 0

           
    
#-------------------------------------------------------------------

# This function places multiple bit values inside FFs of specified indexes.
# This is an upgrade of input_chain_single() and should be accomplished
#   for Part H of Task 1
        
# Hint: How many clocks would it take for value to reach
#       the specified FF?
        
async def input_chain(dut, bit_list, ff_index):
        length_bit_list = len(bit_list)
        dut.scan_en.value = 1
        for i in range(ff_index + length_bit_list):
            if i < length_bit_list:
                  dut.scan_in.value = bit_list[length_bit_list - i - 1]
            else:
                  dut.scan_in.value = 0
            await step_clock(dut)
        dut.scan_en.value = 0
        

#-----------------------------------------------

# This function retrieves a single bit value from the
# chain at specified index 
        
async def output_chain_single(dut, ff_index):
        dut.scan_en.value = 1
        for i in range(CHAIN_LENGTH - ff_index -1):
            await step_clock(dut)       
        output = dut.scan_out.value
        dut.scan_en.value = 0
        return output 

#-----------------------------------------------

# This function retrieves a single bit value from the
# chain at specified index 
# This is an upgrade of input_chain_single() and should be accomplished
#   for Part H of Task 1
        
async def output_chain(dut, ff_index, output_length):
        output_list = []
        dut.scan_en.value = 1
        for i in range(CHAIN_LENGTH - ff_index):
             if i >= CHAIN_LENGTH -ff_index - output_length:
                  output_list.insert(0, dut.scan_out.value)
             await step_clock(dut)
        dut.scan_en.value = 0
        return output_list


#-----------------------------------------------

# Your main testbench function

@cocotb.test()
async def test(dut):

    global CHAIN_LENGTH
    global FILE_NAME        # Make sure to edit this guy
                            # at the top of the file

    # Setup the scan chain object
    # chain = setup_chain(FILE_NAME)
    # print_chain(chain)

    ######################
    # TODO: YOUR CODE HERE 
    ######################
    # Test adder
    # await input_chain(dut,[1,0,0,0,1,0,0,0],5)
    # await step_clock(dut)
    # output_list = (await output_chain(dut, 0, 13))
    # print(output_list)

    # await input_chain(dut,[1,1,0,0,1,1,0,0],5)
    # await step_clock(dut)
    # output_list = (await output_chain(dut, 0, 13))
    # print(output_list)

    # await input_chain(dut,[1,1,1,1,1,0,0,0],5)
    # await step_clock(dut)
    # output_list = (await output_chain(dut, 0, 13))
    # print(output_list)



    #FSM testting
    # for state in range(8):
    #     for i in range(2):
    #         bits = [int(b) for b in f"{state:03b}"]
    #         await input_chain(dut, bits, 0)
    #         dut.data_avail.value = i
    #         await step_clock(dut)
    #         print("state: "+ str(state))
    #         print("data_avail:" + str(i))
    #         print("buf_en: " + str(dut.buf_en.value))
    #         print("out_writing: " + str(dut.out_writing.value))
    #         print("out_sel: " + str(dut.out_sel.value))
    #         output_list = (await output_chain(dut,0,3))
    #         print("next state:", output_list)
    #         print("\n")

    #Fault Model
    test_vectors = [[0, 0, 0, 0],[1, 1, 0, 0],[0, 0, 1, 0],[1, 0, 1, 1], [1, 1, 1, 1]]
    for i in range(len(test_vectors)):
        test = test_vectors[i]
        dut.a.value  = test[0]
        dut.b.value  = test[1]
        dut.c.value  = test[2]
        dut.d.value  = test[3]
        await Timer(1, units='ns')
        output = dut.x.value
        if output != 1 and i == 0:
            print("faults may be f/0,c/1,e/0,a/1,x/0,g/0,h/0\n")
        elif i == 1 and output != 1:
            print("faults may be f/0,c/1,e/1,a/0,x/0,g/0,h/0\n")
        elif i == 2 and output != 0:
            print("faults may be h/1,x/1,f/1,d/1,c/0\n")
        elif i ==3 and output != 0:
            print("faults may be b/1,g/1,x/1,e/1,a/0\n")
        elif i ==4 and output != 1:
            print("faults may be d/0,e/1,a/0,b/0,x/0,g/0,h/0")

   

