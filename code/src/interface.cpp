#include "interface.hpp"
#include "pins.hpp"

#include <string.h>

#include "Arduino.h"

void serial_receive() {
    while (1) {
        if (Serial.available() > 0) {
            char command[READ_BUFFER_SIZE];
        
            int bytes_read = Serial.readBytesUntil(COMMAND_DELIMITER, command, READ_BUFFER_SIZE);
            command[bytes_read] = '\0';

            handle_command(command);
        }
    }
}

void serial_transmit(uint8_t value) {
    Serial.write(value);
}

void handle_command(char command[]) {
    switch (command[0]) {
        //Mode command
        case 'm':
            handle_mode_command(command);
            break;
        //Get command
        case 'g':
            handle_get_command(command);
            break;
        //Set command
        case 's':
            handle_set_command(command);
            break;
        default:
            break;
    }
}

//Mode command is in the format m <bus_num> <mode>
//Example for input: m 0 0
//Example for output: m 0 1
//Example for pull up: m 0 2
void handle_mode_command(char command[]) {
    int bus_num = command[2] - '0';

    bus_set_mode(command[4] - '0', BUSES[bus_num], BUS_LENS[bus_num]);
}

//Get command is in the format g <bus_num>
//Example: g 0
void handle_get_command(char command[]) {
    int bus_num = command[2] - '0';

    serial_transmit(bus_get_byte_value(BUSES[bus_num], BUS_LENS[bus_num]));
}

//Set command is in the format s <bus_num> <base><value>
//Example for binary: s 0 0b111000
//Example for hex: s 0 0xFF
//Example for decimal: s 0 0d12
void handle_set_command(char command[]) {
    int bus_num = command[2] - '0';
    uint8_t value;

    //Binary (0b111000)
    if (memcmp(command + 4, "0b", 2) == 0) {
        value = strtol(command + 6, NULL, 2);
    }
    //Hex (0xFF)
    else if (memcmp(command + 4, "0x", 2) == 0) {
        value = strtol(command + 6, NULL, 16);
    }
    //Decimal number (0d12)
    else if (memcmp(command + 4, "0d", 2) == 0) {
        value = strtol(command + 6, NULL, 10);
    }
    else {
        return;
    }

    bus_set_byte_value(value, BUSES[bus_num], BUS_LENS[bus_num]);
}