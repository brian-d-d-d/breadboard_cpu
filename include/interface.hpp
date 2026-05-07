#ifndef INTERFACE_HPP
#define INTERFACE_HPP

#include <stdint.h>

void serial_receive();

void serial_transmit(uint8_t value);

void handle_command_string(char command_string[]);

void handle_get_command(char command_string[]);

void handle_set_command(char command_string[]);

#endif