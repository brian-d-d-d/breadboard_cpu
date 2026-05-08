from defines import (ARDUINO_PORT, 
                     ARDUINO_BAUD_RATE, 
                     COMMAND_DELIMITER, 
                     CLOCK_SPEED)

import time
import pytest
import serial

@pytest.fixture()
def serial_port() -> serial.Serial:
    ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE)
    time.sleep(1)

    return ser

@pytest.mark.skip()
def test_commands(serial_port, commands):
    index = 0

    for command in commands:
        if isinstance(command, tuple):
            serial_port.write((command[0] + COMMAND_DELIMITER).encode())       
            try:
                value = int.from_bytes(serial_port.read(1))
                assert(value == command[1])
            except AssertionError:
                raise AssertionError("\n" f"Failed command: {command[0]}, index: {index}"
                                     "\n" f"Read {value} != {command[1]} Expected"
                                     "\n" f"Read {format(value, "#010b")} != {format(command[1], "#010b")} Expected"
                                     "\n" f"Read {format(value, "#04x")} != {format(command[1], "#04x")} Expected")
        else:
            serial_port.write((command + COMMAND_DELIMITER).encode())

        index += 1
        time.sleep(CLOCK_SPEED)
