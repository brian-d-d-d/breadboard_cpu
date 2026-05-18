from utils import test_commands, serial_port

import pytest
import random
from defines import INPUT, OUTPUT

BUS_DATA_1_8 = 0

BUS_CONTROL = 3
BUS_REGISTER_1_8_CLOCK_INDEX = 0 # (22)
BUS_DATA_OE_INDEX = 1 # (24)

@pytest.fixture
def setup_control_bus(serial_port):
    commands = (
        # Set the control bus to output
        f"m {BUS_CONTROL} {OUTPUT}",

        # Disable data out on the register output bus and set clock high for register
        f"s {BUS_CONTROL} 0b00000011",
    )

    test_commands(serial_port, commands)


@pytest.mark.repeat(10)
def test_simple_rw(serial_port, setup_control_bus):
    random_data_1_8 = random.randint(0, 255)

    commands = (   
        # Set the data bus to output
        f"m {BUS_DATA_1_8} {OUTPUT}",

        # Put data on the data bus
        f"s {BUS_DATA_1_8} {hex(random_data_1_8)}",

        # Clock the register down 
        f"s {BUS_CONTROL} 0b00000010",

        # Clock the register up to shift in data to the register
        f"s {BUS_CONTROL} 0b00000011",

        # Set the data bus to something random before reading so we know for sure it works
        f"s {BUS_DATA_1_8} 0xAB",
        
        # Set the bus to input
        f"m {BUS_DATA_1_8} {INPUT}",

        # Enable the register output bus
        f"s {BUS_CONTROL} 0b00000001",

        # Check what is on the data bus
        (f"g {BUS_DATA_1_8}", random_data_1_8)
    )

    print()
    print(f"Data written: {format(random_data_1_8, "#04x")}, {format(random_data_1_8, "#010b")}")

    test_commands(serial_port, commands)
