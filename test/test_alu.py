from utils import run_commands, run_command, get_serial_port

import pytest
import random
from defines import INPUT, OUTPUT

# Flag register should be clocked after c register is clocked

# All registers share the same control bus
BUS_REGISTER_CONTROL = 3

### Register A
BUS_DATA_A_1_8 = 2

BUS_REGISTER_A_1_8_CLOCK_INDEX = 0 # (22)
BUS_REGISTER_A_DATA_OE_INDEX = 1 # (24)

### Register B
BUS_DATA_B_1_8 = 1

BUS_REGISTER_B_1_8_CLOCK_INDEX = 2 # (26)
BUS_REIGSTER_B_DATA_OE_INDEX = 3 # (28)

### Register C and Flag register
BUS_DATA_C_1_8 = 0
BUS_DATA_FLAG = BUS_DATA_C_1_8

BUS_REGISTER_C_1_8_CLOCK_INDEX = 4 # (30)
BUS_REGISTER_C_DATA_OE_INDEX = 5 # (32)

BUS_REGISTER_FLAG_1_8_CLOCK_INDEX = 6 # (34)
BUS_REGISTER_FLAG_OE_INDEX = 7 # (36)

# ALU Control gets its own control bus
BUS_ALU_CONTROL = 4

# ALU Control
BUS_ALU_ARITHMETIC_OE = 0 # (38)
BUS_ALU_LOGIC_OE = 1 # (40)

BUS_ALU_OE = 2 # (42)
BUS_ALU_FLAG_OE = 3 # (44)

# Flags setup
# Carry out, overflow, zero, negative
# CO OV Z N


serial_port = get_serial_port()

def setup_control_bus():
    commands = [
        # Set the control buses to output
        f"m {BUS_REGISTER_CONTROL} {OUTPUT}",
        f"m {BUS_ALU_CONTROL} {OUTPUT}",

        # Disable data out on the registers output bus and set clock high for registers
        f"s {BUS_REGISTER_CONTROL} 0b11111111",

        # Disable all outputs on the alu
        f"s {BUS_ALU_CONTROL} 0b11111111",

        # Clear the flag register
        f"m {BUS_DATA_C_1_8} {OUTPUT}",
        f"s {BUS_DATA_C_1_8} 0b00000000",
        f"s {BUS_REGISTER_CONTROL} 0b10111111",
        f"s {BUS_REGISTER_CONTROL} 0b11111111"
    ]

    return commands

def store_value_register(bus_num: int, register: str, value: int | None = None):
    commands = []
    
    # Storing from the arduino
    if value is not None:
        commands.extend([
            f"m {bus_num} {OUTPUT}",
            f"s {bus_num} {hex(value)}",
            # Make sure that the alu is not outputting to the input for the register
            f"s {BUS_ALU_CONTROL} 0b11111111"
        ]) 
    # Storing from the output of the alu
    else:
        commands.extend([
            f"m {bus_num} {INPUT}"
        ])

    if register == "A":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11111110")
    elif register == "B":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11111011")
    elif register == "C":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11101111")
    elif register == "F":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b10111111")
    
    commands.append(f"s {BUS_REGISTER_CONTROL} 0b11111111")

    return commands
        

def get_value_bus(bus_num: int, register: str, expected_result: int | None = None):
    commands = [
        f"m {bus_num} {INPUT}",
    ]

    if register == "A":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11111101")
    elif register == "B":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11110111")
    elif register == "C":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b11011111")
    elif register == "F":
        commands.append(f"s {BUS_REGISTER_CONTROL} 0b01111111")

    if expected_result is not None:
        commands.append((f"g {bus_num}", expected_result))

    return commands

def alu_output_arithmetic_result():
    commands = [
        f"s {BUS_ALU_CONTROL} 0b11111010"
    ]

    return commands

def alu_output_logic_result():
    commands = [
        f"s {BUS_ALU_CONTROL} 0b11111001"
    ]

    return commands


def alu_output_flags_result():
    commands = [
        f"s {BUS_ALU_CONTROL} 0b11110110"
    ]

    return commands

def alu_disable_output():
    commands = [
        f"s {BUS_ALU_CONTROL} 0b11111111"
    ]

    return commands

@pytest.mark.repeat(30)
def test_simple_a_plus_b_a_nand_b():
    data_A_1_8 = random.randint(0, 127)
    data_B_1_8 = random.randint(0, 127)

    commands = []
    commands.extend(setup_control_bus())

    commands.extend(store_value_register(BUS_DATA_A_1_8, "A", data_A_1_8))
    commands.extend(store_value_register(BUS_DATA_B_1_8, "B", data_B_1_8))

    # Store the arithmetic result in c
    commands.extend(alu_output_arithmetic_result())
    commands.extend(store_value_register(BUS_DATA_C_1_8, "C"))

    # Store then flag result
    commands.extend(alu_output_flags_result())
    commands.extend(store_value_register(BUS_DATA_C_1_8, "F"))

    # Check the c register equals a + b
    commands.extend(alu_disable_output())
    commands.extend(get_value_bus(BUS_DATA_C_1_8, "C", data_A_1_8 + data_B_1_8))

    # Store the logic result in c
    commands.extend(alu_output_logic_result())
    commands.extend(store_value_register(BUS_DATA_C_1_8, "C"))

    data_A_1_8_byte = data_A_1_8.to_bytes()[0]
    data_B_1_8_byte = data_B_1_8.to_bytes()[0]

    data_nand_byte = (1 << 8) - 1 - (data_A_1_8_byte & data_B_1_8_byte)

    # Check the c register equals nand a and b
    commands.extend(alu_disable_output())
    commands.extend(get_value_bus(BUS_DATA_C_1_8, "C", data_nand_byte))
            
    print()
    print(f"Data written to register A: {format(data_A_1_8, "#04x")}, {format(data_A_1_8, "#010b")} {data_A_1_8}")
    print(f"Data written to register B: {format(data_B_1_8, "#04x")}, {format(data_B_1_8, "#010b")} {data_B_1_8}")

    print(f"Expected arithmetic result: {format(data_A_1_8 + data_B_1_8, "#04x")}, " +
                                        f"{format(data_A_1_8 + data_B_1_8, "#010b")}, " +
                                        f"{data_A_1_8 + data_B_1_8}")
    
    
    print(f"Expected logic result     : {format(data_nand_byte, "#04x")}, " +
                                        f"{format(data_nand_byte, "#010b")}")
    
    run_commands(serial_port, commands)

@pytest.mark.repeat(1)
def test_4_byte_unsigned_add():
    # Range from 2^25 -> 2^31. This means both numbers will be 4 bytes
    data_A_1_8 = random.randint(33554432, 2147483647)
    data_B_1_8 = random.randint(33554432, 2147483647)
    
    bytes_A = [data_A_1_8 & 0xff,
               (data_A_1_8 >> 8) & 0xff, 
               (data_A_1_8 >> 16) & 0xff, 
               (data_A_1_8 >> 24) & 0xff, 
    ]
    bytes_B = [data_B_1_8 & 0xff, 
               (data_B_1_8 >> 8) & 0xff, 
               (data_B_1_8 >> 16) & 0xff, 
               (data_B_1_8 >> 24) & 0xff, 
    ]

    print()
    print("A" + str([hex(x) for x in bytes_A]))
    print("B" + str([hex(x) for x in bytes_B]))

    bytes_C = []

    commands = []
    commands.extend(setup_control_bus())

    run_commands(serial_port, commands)

    for i in range(0, 4):
        sub_commands = []

        sub_commands.extend(store_value_register(BUS_DATA_A_1_8, "A", bytes_A[i]))
        sub_commands.extend(store_value_register(BUS_DATA_B_1_8, "B", bytes_B[i]))

        # Store the arithmetic result in c
        sub_commands.extend(alu_output_arithmetic_result())
        sub_commands.extend(store_value_register(BUS_DATA_C_1_8, "C"))

        # Store the flags
        sub_commands.extend(alu_output_flags_result())
        sub_commands.extend(store_value_register(BUS_DATA_C_1_8, "F"))

        # Run the above commands
        run_commands(serial_port, sub_commands)

        # Get the result
        sub_commands = []
        sub_commands.extend(alu_disable_output())
        sub_commands.extend(get_value_bus(BUS_DATA_C_1_8, "C"))
        run_commands(serial_port, sub_commands)

        bytes_C.append(hex(run_command(serial_port, f"g {BUS_DATA_C_1_8}")))

    print("Result in hex: " + str(bytes_C))

    result_int = 0
    result_int |= int(bytes_C[0], 16)
    result_int |= int(bytes_C[1], 16) << 8
    result_int |= int(bytes_C[2], 16) << 16
    result_int |= int(bytes_C[3], 16) << 24

    print("Result in decimal: " + str(result_int))
    print("Result should be: " + str(data_A_1_8 + data_B_1_8))

    # assert result_int == data_A_1_8 + data_B_1_8
        
    