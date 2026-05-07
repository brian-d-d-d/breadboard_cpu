#include "interface.hpp"
#include "pins.hpp"

#include <string.h>

#include "Arduino.h"

void serial_receive() {
    while (1) {
        if (Serial.available() > 0) {
            char command_string[Serial.available()];
            int index = 0;
            
            uint8_t data = Serial.read();
            while (Serial.available() > 0) {
                command_string[index] = data;
                data = Serial.read();

                index++;
            }

            handle_command_string(command_string, index);
        }
    }
}

void serial_transmit(uint8_t value) {
    Serial.write(value);
}

void handle_command_string(char command_string[], int len) {
    switch (command_string[0]) {
        //Get command
        case 'g':
            handle_get_command(command_string, len);
            break;
        //Set command
        case 's':
            handle_set_command(command_string, len);
            break;
        default:
            break;
    }
}

void handle_get_command(char command_string[], int len) {
    int bus_num = command_string[2] - '0';

    serial_transmit(bus_get_byte_value(BUSES[bus_num], BUS_LENS[bus_num]));
}

//Set command is in the format s <bus_num> <base><value>
//Example for binary: s 1 0b111000
//Example for hex: s 1 0xFFDD
//Example for decimal: s 1 0d12
void handle_set_command(char command_string[], int len) {
    int bus_num = command_string[2] - '0';
    uint8_t value;

    //Binary (0b111000)
    if (memcmp(command_string + 4, "0b", 2) == 0) {
        value = strtoul(command_string + 5, NULL, 2);
    }
    //Hex (0xFFDD)
    else if (memcmp(command_string + 4, "0x", 2) == 0) {
        value = strtoul(command_string + 5, NULL, 16);
    }
    //Decimal number (0d12)
    else if (memcmp(command_string + 4, "0d", 2) == 0) {
        value = strtoul(command_string + 5, NULL, 10);
    }
    else {
        return;
    }

    bus_set_byte_value(value, BUSES[bus_num], BUS_LENS[bus_num]);
}