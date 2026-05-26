from utils import test_commands, serial_port

import pytest

@pytest.mark.parametrize(
    "commands",
    [
        ([
            "m 0 1",
            "s 0 0d2",
            "s 0 0d4",
            "s 0 0d6",

            "m 0 0",
            ("g 0", 0x14),

            "m 0 1",
            "s 0 0b10101010"
        ])
    ]
)
def test_simple(serial_port, commands):
    test_commands(serial_port, commands)