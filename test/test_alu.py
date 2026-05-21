from utils import run_commands, get_serial_port

import pytest
import random
from defines import INPUT, OUTPUT

# MAKE SURE TO CHECK IF CARRY IN IS FLOATING

# Both registers share the same control bus
BUS_CONTROL = 3

### Register A
BUS_DATA_A_1_8 = 0

BUS_REGISTER_A_1_8_CLOCK_INDEX = 0 # (22)
BUS_DATA_A_OE_INDEX = 1 # (24)
### Register A

### Register B
BUS_DATA_B_1_8 = 1

BUS_REGISTER_B_1_8_CLOCK_INDEX = 2 # (26)
BUS_DATA_OE_B_INDEX = 3 # (28)
### Register B

serial_port = get_serial_port()

@pytest.fixture
def setup_control_bus():
    commands = (
        # Set the control buses to output
        f"m {BUS_CONTROL} {OUTPUT}",

        # Disable data out on the registers output bus and set clock high for registers
        f"s {BUS_CONTROL} 0b00001111",
    )

    run_commands(serial_port, commands)


@pytest.mark.repeat(100)
def test_simple(setup_control_bus):
    data_A_1_8 = random.randint(0, 127)
    data_B_1_8 = random.randint(0, 127)

    commands = (   
        # Set the data bus to output
        f"m {BUS_DATA_A_1_8} {OUTPUT}",
        f"m {BUS_DATA_B_1_8} {OUTPUT}",
        
        # Put data on the data bus
        f"s {BUS_DATA_A_1_8} {hex(data_A_1_8)}",
        f"s {BUS_DATA_B_1_8} {hex(data_B_1_8)}",

        # Clock the registers down 
        f"s {BUS_CONTROL} 0b00001010",

        # Clock the registers up to shift in data to the registers
        f"s {BUS_CONTROL} 0b00001111",
    )

    print()
    print(f"Data written to register A: {format(data_A_1_8, "#04x")}, {format(data_A_1_8, "#010b")} {data_A_1_8}")
    print(f"Data written to register B: {format(data_B_1_8, "#04x")}, {format(data_B_1_8, "#010b")} {data_B_1_8}")

    print(f"Expected arithmetic result: {format(data_A_1_8 + data_B_1_8, "#04x")}, " +
                                        f"{format(data_A_1_8 + data_B_1_8, "#010b")}, " +
                                        f"{data_A_1_8 + data_B_1_8}")
    
    data_A_1_8_byte = data_A_1_8.to_bytes()[0]
    data_B_1_8_byte = data_B_1_8.to_bytes()[0]

    data_nand_byte = (1 << 8) - 1 - (data_A_1_8_byte & data_B_1_8_byte)

    print(f"Expected logic result     : {format(data_nand_byte, "#04x")}, " +
                                        f"{format(data_nand_byte, "#010b")}")

    run_commands(serial_port, commands)


