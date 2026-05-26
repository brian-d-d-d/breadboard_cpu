from utils import test_commands, serial_port

import pytest
import random

BUS_DATA_1_8 = 0
BUS_ADDRESS_1_8 = 1
BUS_ADDRESS_9_16 = 2

BUS_CONTROL = 3
BUS_CONTROL_WE_INDEX = 0
BUS_CONTROL_OE_INDEX = 1

random_address_1_8 = random.randint(0, 255)
random_address_9_16 = random.randint(0, 255)
random_data_1_8 = random.randint(0, 255)

@pytest.mark.parametrize(
    "commands",
    [
        (
            # Set the address buses to outputs
            f"m {BUS_ADDRESS_1_8} 1",
            f"m {BUS_ADDRESS_9_16} 1",

            # Set the control bus to output
            f"m {BUS_CONTROL} 1",

            # Set the data bus to output to write data
            f"m {BUS_DATA_1_8} 1",

            # Set control bits to disable read and write
            # WE 1 and OE 1
            # Not needed for this test just showing how to do it
            f"s {BUS_CONTROL} 0b00000011",

            # Set address as 2 random hex bytes
            f"s {BUS_ADDRESS_1_8} {hex(random_address_1_8)}",
            f"s {BUS_ADDRESS_9_16} {hex(random_address_9_16)}",

            # Set the data bus as a random hex byte
            f"s {BUS_DATA_1_8} {hex(random_data_1_8)}",

            # Set the control bits to write
            # WE 0 and OE can be anything
            f"s {BUS_CONTROL} 0b00000010",

            # Data should be written to the address at this point

            # Set the control bits to read
            # WE 1 and OE 0
            f"s {BUS_CONTROL} 0b00000001",

            # Set the bits on the data bus and addresses to something random before reading
            # So we know for sure the data is being read properly
            f"s {BUS_DATA_1_8} 0d22",
            f"s {BUS_ADDRESS_1_8} 0d33",
            f"s {BUS_ADDRESS_9_16} 0d44",

            # Set the address buses back to the correct address
            f"s {BUS_ADDRESS_1_8} {hex(random_address_1_8)}",
            f"s {BUS_ADDRESS_9_16} {hex(random_address_9_16)}",

            # Set the data bus to input to read data
            f"m {BUS_DATA_1_8} 0",

            # Read the data on the data bus and check it is equal to the written data
            (f"g {BUS_DATA_1_8}", random_data_1_8)
        )
    ]
)
def test_simple_rw(serial_port, commands):
    print()
    print(f"Address: {hex(random_address_1_8)}{hex(random_address_9_16)[2:]}")
    print(f"Data written: {hex(random_data_1_8)}")

    test_commands(serial_port, commands)